# Imports
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from tqdm import tqdm
import pickle
import src.utils.preprocess as preprocess
# import src.utils.sigmoid as sigmoid
from scipy.io import savemat, loadmat
from scipy.signal import convolve2d
import re
import visionloader as vl
import sta_utils as su
from scipy.spatial import ConvexHull
import src.utils.cellmap as cellmap
import src.utils.encoding_decoding_simulation_pooled as edsp
from scipy.ndimage import gaussian_filter
from matplotlib.patches import Ellipse
from PIL import Image
import multiprocessing
from multiprocessing import Pool
import warnings

import sys
sys.path.append('/Volumes/Lab/Users/ajphillips/greedy/src/')
import sigmoid

piece = '2024-10-02-2' # CHANGE ME
analysis_base = f"/Volumes/Stream/Analysis/RETINA/{piece}"
pp_base = analysis_base
gsort_base = analysis_base
vstim_base = analysis_base
espont_base = analysis_base
pickle_path_base = "gsort_single_v2"
label = "_2" # CHANGE ME


frame_nos = np.arange(105) # CHANGE ME
spike_trains = np.load(f"{analysis_base}/dictionary/spike_trains{label}.npz", allow_pickle=True)
response_nos = spike_trains['response_indices']

# read the randomized direction contents of the moving bar
# directions = []
# with open(f"/Volumes/Data/{piece}/Visual/s2024_07_18_0_data003.txt") as f:
#     for line in f:
#         directions.append(line.strip())
# directions = np.array(directions[1:])


for frame_no, response_no in tqdm(zip(frame_nos, response_nos), total=frame_nos.size):

    if frame_no == 0:
        select_response_nos = np.arange(0,30,2) # UPDATE ME
    elif frame_no < 101:
        modulo_no = (response_no-30) % 100 # UPDATE ME
        select_response_nos = np.arange(modulo_no+30, 1530, 100) # UPDATE ME
    else:
        rolling_e_no = frame_no - 101 # UPDATE ME
        rolling_e = np.array([3, 2, 3, 2, 1, 1, 2, 0, 3, 2, 2, 0, 0, 3, 1, 3, 0, 1, 1, 3, 0, 0, 1, 1, 3, 0, 1, 1, 0, 1, 3, 0, 1, 3, 2, 3, 0, 2, 1, 2, 2, 3, 2, 0, 3, 1, 3, 1, 3, 1, 3, 3, 2, 3, 0, 0, 1, 0, 0, 2, 1, 0, 1, 2, 3, 3, 1, 3, 0, 2, 0, 2, 2, 2, 2, 2, 1, 0, 2, 0])
        select_response_nos = np.where(rolling_e == rolling_e_no)[0] + 1530 # UPDATE ME

    vstim_responses = [[] for _ in range(select_response_nos.size)]

    estim = f"data008/frame_{frame_no}"
    espont = "data008_from_data002"
    vstim = "data005_from_data002"
    wnoise = "data002"
    cell_types = ['ON parasol', 'OFF parasol']

    wnoise_path = os.path.join(analysis_base, wnoise)
    pp_path = os.path.join(pp_base, estim)
    gsort_path = os.path.join(gsort_base, "gsort", estim, wnoise)
    vstim_path = os.path.join(vstim_base, vstim)
    espont_path = os.path.join(espont_base, espont)

    wn1 = 'data002'
    estim1 = 'data003'
    wn2 = 'data002'
    estim2 = 'data010'


    # The dictionary and associated data is stored in this directory
    # Much of the data/analysis associated with the experiment exists in the parent directory
    dict_path = os.path.join(analysis_base, "dictionary")

    # Load relevant data from .npz files
    with np.load(os.path.join(dict_path,f"selective_stimuli{label}.npz")) as data:
        selective_stimuli = data["selective_stimuli"]


    vstim_vcd = vl.load_vision_data(vstim_path,vstim,
                                    include_neurons=True)

    selective_cells_of_interest = np.unique(selective_stimuli[:,1]).astype(int)
    # print(f"Total selective cells of type {cell_types}: {selective_cells_of_interest.size}")


    spike_times = np.array([vstim_vcd.get_spike_times_for_cell(c) for c in selective_cells_of_interest], dtype=object) / 20 # convert to ms

    ttl_times = vstim_vcd.ttl_times / 20 # convert to ms

    responses = []
    for j in range(len(ttl_times)-1):
        if j == 1529: # CHANGE ME
            low = ttl_times[j]
            high = ttl_times[j] + 500
            filtered_spike_times = np.array([spike_time[(low < spike_time) & (spike_time < high)] for spike_time in spike_times], dtype=object)
            responses.append(filtered_spike_times)
        else:
            low = ttl_times[j]
            high = ttl_times[j+1]
            filtered_spike_times = np.array([spike_time[(low < spike_time) & (spike_time < high)] for spike_time in spike_times], dtype=object)
            responses.append(filtered_spike_times)
    low = ttl_times[-1]
    high = ttl_times[-1] + 500
    filtered_spike_times = np.array([spike_time[(low < spike_time) & (spike_time < high)] for spike_time in spike_times], dtype=object)
    responses.append(filtered_spike_times)


    for i, select_response_no in enumerate(select_response_nos):
        response = responses[select_response_no]


        # Align response rasters in time (the very first attempted estim is aligned with the very first rounded recorded vstim spike)
        bin_size_ms = 2.5
        rounded_response = np.array([np.round(cell_spike_times / bin_size_ms) * bin_size_ms for cell_spike_times in response], dtype=object)

        response_reference_candidates = []
        for c in range(len(rounded_response)):
            if len(rounded_response[c]) > 0:
                response_reference_candidates.append(rounded_response[c][0])
        try:
            response_reference = np.min(response_reference_candidates)
        except:
            print(f"no spikes in response {select_response_no}")
            response_reference = 0
        # print(f"response reference time: {response_reference}")


        global_reference = response_reference - ttl_times[select_response_no]

        if response.size > 0:
            vstim_responses[i] = response - response_reference + global_reference


        plt.figure(figsize=(20, 10))

        # Create a spike raster plot
        if select_response_no == response_no:
            plt.eventplot(response-response_reference+global_reference, linelengths=0.5, colors='red')
        else:
            plt.eventplot(response-response_reference+global_reference, linelengths=0.5, colors='black')

        # Set the y-axis ticks and labels
        plt.yticks(range(len(selective_cells_of_interest)), selective_cells_of_interest)
        plt.ylabel('Cell ID')

        # Set the x-axis label
        plt.xlabel('Time (ms)')

        # Set the plot title
        plt.title('Visually Evoked Spike Trains')

        # Restrict the x axis
        plt.xlim(0, 500)

        # Save the plot
        plt.savefig(f"/Volumes/Scratch/iko/Users/ajphillips/tmp/{piece}/figs{label}/frame_{frame_no}_vtrial_{i}.png")

        # Close the plot
        plt.close()


    # Save the numpy array
    np.save(f"/Volumes/Stream/Analysis/RETINA/{piece}/spikes{label}/frame_{frame_no}_vstim_responses.npy", np.array(vstim_responses, dtype=object), allow_pickle=True)