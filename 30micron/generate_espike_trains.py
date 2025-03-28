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

piece = '2024-09-25-3' # CHANGE ME
analysis_base = f"/Volumes/Stream/Analysis/RETINA/{piece}"
pp_base = analysis_base
gsort_base = analysis_base
vstim_base = analysis_base
espont_base = analysis_base
pickle_path_base = "gsort_single_v2"
label = "" # CHANGE ME


frame_nos = np.arange(105) # CHANGE ME
spike_trains = np.load(f"{analysis_base}/dictionary/spike_trains{label}.npz", allow_pickle=True)
response_nos = spike_trains['response_indices']
estim_trials = 15 # CHANGE ME

for frame_no, response_no in tqdm(zip(frame_nos, response_nos), total=frame_nos.size):

    estim_espont_responses = [[] for _ in range(estim_trials)]

    for estim_trial in tqdm(np.arange(estim_trials)):

        estim = f"data007/frame_{frame_no}"
        espont = "data007_from_data003"
        vstim = "data005_from_data003"
        wnoise = "data003"
        cell_types = ['ON parasol', 'OFF parasol']

        wnoise_path = os.path.join(analysis_base, wnoise)
        pp_path = os.path.join(pp_base, estim)
        gsort_path = os.path.join(gsort_base, "gsort", estim, wnoise)
        vstim_path = os.path.join(vstim_base, vstim)
        espont_path = os.path.join(espont_base, espont)

        wn1 = 'data003'
        estim1 = 'data004'
        wn2 = 'data003'
        estim2 = 'data009'


        # The dictionary and associated data is stored in this directory
        # Much of the data/analysis associated with the experiment exists in the parent directory
        dict_path = os.path.join(analysis_base, "dictionary")

        # Load relevant data from .npz files
        with np.load(os.path.join(dict_path,f"selective_stimuli{label}.npz")) as data:
            selective_stimuli = data["selective_stimuli"]
        with np.load(os.path.join(dict_path,f"{wnoise}_bundle_thresholds.npz")) as data:
            bundle_thresholds = data["bundle_thresholds"]


        vcd = vl.load_vision_data(wnoise_path,wn1,
                                include_neurons=True,
                                include_ei=True,
                                include_params=True,
                                include_runtimemovie_params=True)

        all_cells_of_interest = []
        for cell_type in cell_types:
            all_cells_of_interest += vcd.get_all_cells_similar_to_type(cell_type)
        all_cells_of_interest = np.array(all_cells_of_interest)


        # The electrical stimulation scans are stored in this directory
        # Much of the data/analysis associated with the experiment exists in the parent directory
        path = os.path.join(analysis_base, "estim")

        # Read in .mat file
        ppinfo = loadmat(os.path.join(path,f"preprocessing_info{label}.mat"))
        experiment_boundaries, experiment_names = ppinfo["experimentBoundaries"], ppinfo["experimentNames"]

        with open(os.path.join(path,f"spike_trains{label}.sef"), "rb") as f:
            sef = np.fromfile(f, dtype=np.int32)
            sef = np.reshape(sef, (int(len(sef)/3), 3), order='F')

        sef_of_interest = sef[experiment_boundaries[frame_no,estim_trial*2+0]-1:experiment_boundaries[frame_no,estim_trial*2+1],:] # Assume 2D matrix called 'experimentBoundaries' of size |nExperiments|x|2*nBoundaries|

        unique_stimuli, count_stimuli = np.unique(sef_of_interest[:,1:], axis=0, return_counts=True)
        unique_times, count_times = np.unique(sef_of_interest[:,0], return_counts=True)


        def flip(cell, pattern, amp, flip_prob=0.9, plot=False, suppress_warnings=False):

            gsort_path_base1 = os.path.join(gsort_base, "gsort", estim1)
            gsort_path_base2 = os.path.join(gsort_base, "gsort", estim2)

            patterns = sigmoid.find_activating_patterns(gsort_path_base1, cell)
            patterns = np.sort(patterns)
            pattern_nos = [int(p.split('p')[-1]) for p in patterns]
            
            if pattern not in pattern_nos:
                # raise Exception("Pattern not found in gsort_path_base1")
                if not suppress_warnings:
                    warnings.warn("Pattern not gsorted during single-electrode stimulation, can't disambiguate") # Note this will only show once if the issue occurs repeatedly
                return False

            pattern = f"p{pattern}"

            try:
                if plot:
                    fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5,5))

                amps1, probs1, slp1, thr1, std1, success1 = sigmoid.compute_sigmoid(gsort_path_base1, pickle_path_base, cell, pattern, plot=False)
                
                if plot:
                    sigmoid.plot_sigmoid(ax, amps1, probs1, slp1, thr1, 'k')

                try:
                    amps2, probs2, slp2, thr2, std2, success2 = sigmoid.compute_sigmoid(gsort_path_base2, pickle_path_base, cell, pattern) # mapping['forward'][cell]

                    if plot:
                        sigmoid.plot_sigmoid(ax, amps2, probs2, slp2, thr2, 'b')

                except Exception as e:
                    if plot:
                        ax.text(0.1,0.9,str(e))
                    else:
                        raise e

            except Exception as ex:
                if plot:
                    ax.text(0.1,0.1,str(ex))
                else:
                    raise ex
            
            if plot:
                ax.set_xlim(0,4)
                ax.set_ylim(0,1)
                ax.set_xlabel('Stimulation Amplitude (uA)')
                ax.set_ylabel('Activation Probability')
                ax.set_title(f"{piece} cell {cell} electrode {pattern[1:]}")
                plt.show()

            # Perform disambiguation
            # print(f"calibration prob {probs1[amp-1]}, bookend prob {probs2[amp-1]}, flipping {probs2[amp-1] > flip_prob}")
            if probs2[amp-1] > flip_prob:
                return True
            else:
                return False
            

        def amps_to_indices(amps):
            AMPS = np.array([0.09375, 0.1875, 0.28125, 0.375, 0.46875, 0.5625, 0.65625, 0.75, 0.84375, 0.9375,
                1.03125, 1.125, 1.21875, 1.3125, 1.40625, 1.5, 1.59375, 1.6875, 1.78125, 1.875, 1.96875,
                2.0625, 2.15625, 2.25, 2.34375, 2.4375, 2.53125, 2.625, 2.71875, 2.8125, 2.90625, 3.0,
                3.09375, 3.1875, 3.28125, 3.375, 3.46875, 3.5625, 3.65625, 3.75, 3.84375, 3.9375])
            return np.array([np.argmin(np.abs(AMPS - amp)) + 1 for amp in amps]) # 1-indexed

        def boolean_spikes(gsort_path_base, pickle_path_base, cell, pattern, k):
            # Set the random number seed for reproducibility of edge case behavior
            np.random.seed(cell+int(pattern[1:]))

            gsort_path = f"{gsort_path_base}/{pattern}/"
        
            pickle_path = f"{pickle_path_base}_n{cell}_{pattern}_k{k}.pkl"
            with open(gsort_path + pickle_path, 'rb') as f:
                prob_dict = pickle.load(f)
                
                cosine_prob, prob, initial_clustering_with_virtual, final_clustering, graph_info = prob_dict['cosine_prob'], prob_dict['prob'], prob_dict['initial_clustering_with_virtual'], prob_dict['final_clustering'], prob_dict['graph_info']

                cosine_prob = cosine_prob[0]
                graph_info = graph_info[2]
                final_clustering = final_clustering[0]

                # print(cosine_prob)
                # print(prob)
                # print(graph_info)
                # print(initial_clustering_with_virtual)

                if np.isclose(cosine_prob, 0, rtol=0, atol=1e-5):
                    bool_spikes = [False for _ in initial_clustering_with_virtual]
                    # print(bool_spikes)
                    # print(sum(bool_spikes)/len(bool_spikes))
                    return bool_spikes

                # get index of dictionary entry with the value cell
                edges = [*graph_info]
                edge = get_key(graph_info, cell)
                # print(edge)
                # print(edges)
                path = []
                for e in edge:
                    path.extend(get_path(edges, edges.index(e)))

                # print(path)

                if np.isclose(cosine_prob, prob, rtol=0, atol=1e-5):
                    bool_spikes = [spike in path for spike in initial_clustering_with_virtual]
                    # print(bool_spikes)
                    # print(sum(bool_spikes)/len(bool_spikes))
                    return bool_spikes
                

                all_possible_edges = []
                difference = np.round(np.abs(cosine_prob - prob)*len(initial_clustering_with_virtual)).astype(int)
                # print(difference)

                for e in edge:
                    _ = find_cosine_path(edges, edges.index(e), initial_clustering_with_virtual, all_possible_edges, difference)
                # print(all_possible_edges)

                if len(all_possible_edges) > 1:
                    warnings.warn("Ambiguous cosine similarity single path removal") # we cannot infer which edge was removed, arbitrarily guess the first one
                elif len(all_possible_edges) == 0:
                    warnings.warn("No valid cosine similarity single path removal") # indicating multiple edges have been removed, randomly assign the spikes
                    
                    # Build a randomly shuffled list of booleans corresponding to the cosine probability
                    bool_spikes = [True if i < np.round(cosine_prob*len(initial_clustering_with_virtual)).astype(int) else False for i in range(len(initial_clustering_with_virtual))]
                    np.random.shuffle(bool_spikes)

                    # print(bool_spikes)
                    # print(sum(bool_spikes)/len(bool_spikes))
                    return bool_spikes
                
                removal_path = get_path(edges, edges.index(all_possible_edges[0]))
                # print(removal_path)

                bool_spikes = [spike in path and spike not in removal_path for spike in initial_clustering_with_virtual]
                # print(bool_spikes)
                # print(sum(bool_spikes)/len(bool_spikes))
                
                return bool_spikes


        def get_key(my_dict, val):
            keys = []
        
            for key, value in my_dict.items():
                if val == value:
                    keys.append(key)

            if len(keys) == 0:
                raise ValueError("Cell not assigned to any edge")

            return keys

        def get_path(edges, start_index):
            path = []
            path.append(edges[start_index][1])

            for i in range(len(edges)):
                if edges[i][0] == edges[start_index][1]:
                    path.extend(get_path(edges, i))

            return path
            
        def find_cosine_path(edges, start_index, initial_clustering_with_virtual, all_possible_edges, difference):

            count = 0
            for i in range(len(edges)):
                if edges[i][0] == edges[start_index][1]:
                    count += find_cosine_path(edges, i, initial_clustering_with_virtual, all_possible_edges, difference)
            
            total = np.sum(edges[start_index][1] == initial_clustering_with_virtual) + count
            if total == difference:
                all_possible_edges.append(edges[start_index])
            return total

        def transform_to_519(electrode):
            skip_elecs = np.array([1, 130, 259, 260, 389, 390, 519])
            elecs = np.arange(1, 520)
            elecs = elecs[~np.isin(elecs, skip_elecs)]
            return elecs[electrode-1]

        def process_time_pattern(t):
            """Process a single time pattern."""
            local_initial_spikes = {}
            local_initial_probabilities = {}
            local_spikes = {}
            local_probabilities = {}
            local_off_target_counter = 0

            # Set up nested dictionaries
            local_initial_spikes[t] = {}
            local_initial_probabilities[t] = {}
            local_spikes[t] = {}
            local_probabilities[t] = {}

            # Identify all electrical stimuli delivered simultaneously at time t
            stim = sef_of_interest[np.where(sef_of_interest[:, 0] == unique_times[t])[0], 1:]

            target_cells = []
            for s in stim:
                # Find the row of selective_stimuli corresponding to each electrical stimulus
                selective_stimulus = selective_stimuli[np.where((selective_stimuli[:, 0] == transform_to_519(s[0])) & (amps_to_indices(selective_stimuli[:, 2]) == s[1]))[0][0]]

                # Look for electrical spike sorting results at the time-pattern for each targeted cell (only ever one movie per time-pattern)
                c = int(selective_stimulus[1])
                bs = boolean_spikes(gsort_path, pickle_path_base, c, f"p{t+1}", 0)

                local_initial_spikes[t][c] = bs
                local_initial_probabilities[t][c] = np.mean(bs)

                # If the selective stimulus was pure (we expected the cell to spike with ~100% probability) and gsort returns ~0% probability,
                # cross reference with the bookend single-electrode scan to decide how to disambiguate
                # Assumes that multi-electrode stimulation does not significantly alter the single-electrode activation curve
                # Ask Amrith about explanation for 0.1
                if int(selective_stimulus[3]) and (np.mean(bs) < 0.2): 
                    if flip(c, transform_to_519(s[0]), s[1], flip_prob=0.8, plot=False): 
                        bs = [not b for b in bs]

                local_spikes[t][c] = bs
                local_probabilities[t][c] = np.mean(bs)

                target_cells.append(c)

            # Look for electrical spike sorting results at the time-pattern for each other gsorted cell (only ever one movie per time-pattern)
            for c in sigmoid.find_activating_cells(gsort_path, f"{t+1}"):
                if c in target_cells:
                    continue

                bs = boolean_spikes(gsort_path, pickle_path_base, c, f"p{t+1}", 0)

                local_initial_spikes[t][c] = bs
                local_initial_probabilities[t][c] = np.mean(bs)

                # Perform disambiguation:
                # We know that during the calibration scan, the non-target cell was not activated with the electrical stimulus
                # If the bookend scan indicates that the non-target cell was activated with high probability, we assume the worst and flip the result
                # Also assume the worst by trying to disambiguate with each electrical stimulus and taking the largest activation probability
                if np.mean(bs) < 0.2:
                    for s in stim:
                        if flip(c, transform_to_519(s[0]), s[1], flip_prob=0.8, plot=False, suppress_warnings=True): 
                            bs = [not b for b in bs]
                            break

                local_spikes[t][c] = bs
                local_probabilities[t][c] = np.mean(bs)

                if np.mean(bs) > 0.5:
                    print(f"Off-target cell {c} activated at {np.mean(bs)} (expected {target_cells})")
                    local_off_target_counter += 1

            return local_initial_spikes, local_initial_probabilities, local_spikes, local_probabilities, local_off_target_counter

        if estim_trial == 0:

            # Use multiprocessing to parallelize the loop over t
            initial_spikes = {}
            initial_probabilities = {}
            spikes = {}
            probabilities = {}
            off_target_counter = 0

            with Pool() as pool:
                for result in pool.imap(process_time_pattern, range(unique_times.shape[0])):
                    local_initial_spikes, local_initial_probabilities, local_spikes, local_probabilities, local_off_target_counter = result
                    initial_spikes.update(local_initial_spikes)
                    initial_probabilities.update(local_initial_probabilities)
                    spikes.update(local_spikes)
                    probabilities.update(local_probabilities)
                    off_target_counter += local_off_target_counter

            print(f"{off_target_counter / sum(count_stimuli) * 100:.1f}% of stimuli result in off-target activation")


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

        # Make sure this index agrees with the frame you are looking at
        response = responses[response_no]


        # Build electrically evoked response for a single trial using the spike dictionary
        estim_response = [[] for _ in range(len(selective_cells_of_interest))]

        for t in range(unique_times.shape[0]):
            for c in spikes[t]:
                # Only include selective cells of interest in results for now
                if c not in selective_cells_of_interest:
                    continue
                if spikes[t][c][estim_trial]:
                    estim_response[np.where(selective_cells_of_interest == c)[0][0]].append(unique_times[t])

        for c in range(len(estim_response)):
            estim_response[c] = np.array(estim_response[c])
        estim_response = np.array(estim_response, dtype=object) / 20 # convert to ms


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
            print(f"no spikes in response {response_no}")
            response_reference = 0
        # print(f"response reference time: {response_reference}")


        estim_response_reference = sef_of_interest[0,0] / 20 # convert to ms
        # print(f"estim response reference time: {estim_response_reference}")


        espont_vcd = vl.load_vision_data(espont_path,espont,
                                        include_neurons=True)

        espont_spike_times = np.array([espont_vcd.get_spike_times_for_cell(c) for c in selective_cells_of_interest], dtype=object)

        offset = 20000 # offset of 20000 samples between SEF times and actual data
        low = unique_times[0] + offset
        high = unique_times[-1] + offset
        total_response = np.array([(spike_time[(low < spike_time) & (spike_time < high)] - offset) / 20 for spike_time in espont_spike_times], dtype=object) # convert to ms

        # Get rid of any electrically evoked spikes identified by Vision
        espont_response = [[] for _ in range(len(total_response))]
        for c in range(len(total_response)):
            espont_response[c] = np.array([spike for spike in total_response[c] if not np.any(((spike - unique_times/20) >= -1) & ((spike - unique_times/20) <= 2))])
        espont_response = np.array(espont_response, dtype=object)


        global_reference = response_reference - ttl_times[response_no]

        estim_espont_response = np.array([np.concatenate((estim_response[c], espont_response[c])) for c in range(len(selective_cells_of_interest))], dtype=object)

        if estim_espont_response.size > 0:
            estim_espont_responses[estim_trial] = estim_espont_response - estim_response_reference + global_reference


        plt.figure(figsize=(20, 10))

        # Make two lineoffsets vectors offset by a constant value
        lineoffsets1 = np.arange(len(selective_cells_of_interest))
        lineoffsets2 = np.arange(len(selective_cells_of_interest)) - 0.5

        # Create a spike raster plot
        plt.eventplot(response-response_reference+global_reference, linelengths=0.5, lineoffsets=lineoffsets1, colors='black')
        plt.eventplot(estim_espont_response-estim_response_reference+global_reference, linelengths=0.5, lineoffsets=lineoffsets2, colors='red')

        # Set the y-axis ticks and labels
        plt.yticks(range(len(selective_cells_of_interest)), selective_cells_of_interest)
        plt.ylabel('Cell ID')

        # Set the x-axis label
        plt.xlabel('Time (ms)')

        # Set the plot title
        plt.title('Visually Evoked (black) and Electrically Evoked + Spontaneous (red) Spike Trains')

        # Restrict the x axis
        plt.xlim(0, 500)

        # Save the plot
        plt.savefig(f"/Volumes/Lab/Users/ajphillips/iko/tmp/{piece}/figs{label}/frame_{frame_no}_trial_{estim_trial}.png")

        # Close the plot
        plt.close()

    # Save the numpy array
    np.save(f"/Volumes/Stream/Analysis/RETINA/{piece}/spikes{label}/frame_{frame_no}_estim_espont_responses.npy", np.array(estim_espont_responses, dtype=object), allow_pickle=True)