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

piece = '2024-07-18-0'
analysis_base = f"/Volumes/Analysis/{piece}/RETINA"
pp_base = analysis_base
gsort_base = analysis_base
vstim_base = analysis_base
espont_base = analysis_base
pickle_path_base = "gsort_single_v2"

# Used response indices 8, 10, 12, 14 (second trial of moving bar in each direction) and 39-58 (first trial of jittered natural scenes for the first 20 images)
# Response index 39 is before the first image of the first trial of jittered natural scenes
frame_nos = np.concatenate((np.arange(4), np.arange(5,24)))
response_nos = np.concatenate((np.array([8,10,12,14]), np.arange(40,59)))

# read the randomized direction contents of the moving bar
directions = []
with open(f"/Volumes/Data/{piece}/Visual/s2024_07_18_0_data003.txt") as f:
    for line in f:
        directions.append(line.strip())
directions = np.array(directions[1:])


for frame_no, response_no in tqdm(zip(frame_nos, response_nos), total=frame_nos.size):

    # select_response_nos = [[0,8,16,24,32],
    #                        [2,10,18,26,34],
    #                        [4,12,20,28,36],
    #                        [6,14,22,30,38],
    #                        [40,90,140,190,240,290,340,390,440,490],
    #                        [41,91,141,191,241,291,341,391,441,491],
    #                        ...

    if response_no < 40:
        # find all the indices of matching directions in the array
        indices = np.where(directions == directions[response_no//2])[0]
        select_response_nos = indices * 2
    else:
        modulo_no = (response_no-40) % 50
        select_response_nos = np.arange(modulo_no+40, 540, 50)

    vstim_responses = [[] for _ in range(select_response_nos.size)]

    label = ""
    estim = f"data004/frame_{frame_no}{label}"
    espont = "data004_from_data001"
    vstim = "data003_from_data001"
    wnoise = "data001"
    cell_types = ['ON alpha', 'OFF alpha']

    wnoise_path = os.path.join(analysis_base, wnoise)
    pp_path = os.path.join(pp_base, estim)
    gsort_path = os.path.join(gsort_base, "gsort", estim, wnoise)
    vstim_path = os.path.join(vstim_base, vstim)
    espont_path = os.path.join(espont_base, espont)

    wn1 = 'data001'
    estim1 = 'data002'
    wn2 = 'data001'
    estim2 = 'data005'


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
        response_reference = np.min(response_reference_candidates)
        # print(f"response reference time: {response_reference}")


        global_reference = response_reference - ttl_times[select_response_no]


        vstim_responses[i] = response - response_reference + global_reference


        plt.figure(figsize=(20, 10))

        # Create a spike raster plot
        plt.eventplot(response-response_reference+global_reference, linelengths=0.5, colors='black')

        # Set the y-axis ticks and labels
        plt.yticks(range(len(selective_cells_of_interest)), selective_cells_of_interest)
        plt.ylabel('Cell ID')

        # Set the x-axis label
        plt.xlabel('Time (ms)')

        # Set the plot title
        plt.title('Visually Evoked Spike Trains')

        # Restrict the x axis
        # plt.xlim(2000, 3000)

        # Save the plot
        plt.savefig(f"/Volumes/Scratch/Users/ajphillips/tmp/{piece}/figs/frame_{frame_no}_vtrial_{i}.png")

        # Close the plot
        plt.close()


    # Save the numpy array
    np.save(f"/Volumes/Stream/Analysis/RETINA/{piece}/spikes/frame_{frame_no}_vstim_responses.npy", np.array(vstim_responses, dtype=object), allow_pickle=True)