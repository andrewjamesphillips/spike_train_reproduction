from stim_algos import gen_multi_experiment_litke_sef

import os
import sys
import logging
import time
import cv2
import subprocess
import psutil
import skimage.io
import visionloader as vl
import sta_utils as su
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import multiprocessing as mp
import copy
import warnings

import matplotlib.cm as cm
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse

from tqdm import tqdm
from scipy.io import loadmat
from multiprocessing.shared_memory import SharedMemory
from multiprocessing.managers import SharedMemoryManager

import src.config as config
import src.utils.bundle_thresholding.bundle_algo_base as bundle
import src.utils.encoding_decoding_simulation_pooled as eds
import src.utils.sigmoid as sigmoid
import src.utils.preprocess as pp

RAW_DATA_PATH = "/Volumes/Stream/Data/RETINA/Stream"
STREAM_DATA_PATH = "/Volumes/Stream/Data/RETINA"
ANALYSIS_PATH = "/Volumes/Stream/Analysis/RETINA"
BIN_FILE_PATH = "/Volumes/Acquisition/Data/electrical-stimuli/ajphillips/RETINA"

SHELL_SCRIPTS_PATH="/Volumes/Lab/Users/ajphillips/RETINA/shell"
SINGLE_ELEC_PATH = "/Volumes/Lab/Users/ajphillips/RETINA/src/utils/single_elec_nlv"
BUNDLE_PATH="/Volumes/Lab/Users/ajphillips/RETINA/src/utils/bundle_thresholding"
BIN_GENERATION_CLK_PATH="/Volumes/Lab/Users/ajphillips/stim-rewrite/scans/clockSignal"

STREAMING_GSORT_PATH="/Volumes/Lab/Users/jeffbrown/electrical_spike_sorting/e-stim-spike-sorting/gsort-run-scripts"
PREPROCESS_SINGLE_ELEC_PATH="/Volumes/Lab/Users/praful/new-labview-io"
PREPROCESS_GDM_PATH="/Volumes/Lab/Users/ajphillips/preprocessing/streaming/new-labview-io"

VISION = "/Volumes/Lab/Development/vision7/Vision.jar"
VISION_MAP_FUNC = "edu.ucsc.neurobiology.vision.tasks.MappingAnalysis"

class Experiment():

    def __init__(self, piece, board, server, cell_types, single_elec_reps) -> None:

        # Set piece
        self.piece = piece

        # Set cell types
        self.cell_types = cell_types

        # Set board
        if (board != 512) and (board != 519):
            raise Exception("Invalid board number")
        self.board = board

        # Set server
        if (server != "peggyo") and (server != "bertha"):
            raise Exception("Invalid server name")
        self.server = server

        # Set experiment-specific parameters
        self.single_elec_reps = single_elec_reps

        # Set paths
        self.raw_data_path = os.path.join(RAW_DATA_PATH, self.piece)
        self.stream_data_path = os.path.join(STREAM_DATA_PATH, self.piece)
        self.analysis_path = os.path.join(ANALYSIS_PATH, self.piece)
        self.bin_file_path = os.path.join(BIN_FILE_PATH, self.piece)

        Experiment.touch_path(self.raw_data_path)
        Experiment.touch_path(self.stream_data_path)
        Experiment.touch_path(self.analysis_path)
        Experiment.touch_path(self.bin_file_path)

        self.estim_path = os.path.join(self.analysis_path, "estim")
        self.gsort_path = os.path.join(self.analysis_path, "gsort")
        self.dictionary_path = os.path.join(self.analysis_path, "dictionary")

        Experiment.touch_path(self.estim_path)
        Experiment.touch_path(self.gsort_path)
        Experiment.touch_path(self.dictionary_path)

        self.vision_data = None
        self.vision_data_vstim = None

        print(f"Board: {self.board}")
        print(f"Piece: {self.piece}")
        print(f"Raw data path: {self.raw_data_path}")
        print(f"Stream data path: {self.stream_data_path}")
        print(f"Analysis path: {self.analysis_path}")
        print(f"Bin file path: {self.bin_file_path}")
        print(f"Single electrode reps: {self.single_elec_reps}")


    def kill_process(self, process):
        """
        Kill a process.
        """
        print(f"Killing process {process.pid}")
        Experiment.kill(process)


    def generate_single_electrode_scan(self, datarun, base_name="single_elec_nlv"):
        """
        Generate a single electrode scan.
        """
        file_name = f"{base_name}_{self.board}_{self.single_elec_reps}_reps"

        self.stim_files = os.path.join(self.estim_path, file_name)

        print(f"Generating SEF, SLF, SIF files for single electrode scan for {self.board} board with {self.single_elec_reps} repetitions at {self.stim_files}")
        os.chdir(config.SINGLE_ELEC_PATH)
        if self.server == "peggyo":
            if self.board == 512:
                subprocess.run(["matlab", "-r", f"addpath(genpath('/Volumes/Lab/Users/praful/comm_toolbox')); generateEventAndPulseFiles512('{self.estim_path}/', '{file_name}', {self.single_elec_reps}); exit;"])
            elif self.board == 519:
                subprocess.run(["matlab", "-r", f"addpath(genpath('/Volumes/Lab/Users/praful/comm_toolbox')); generateEventAndPulseFiles519('{self.estim_path}/', '{file_name}', {self.single_elec_reps}); exit;"])
        elif self.server == "bertha":
            if self.board == 512:
                subprocess.run(["matlab", "-r", f"generateEventAndPulseFiles512('{self.estim_path}/', '{file_name}', {self.single_elec_reps}); exit;"])
            elif self.board == 519:
                subprocess.run(["matlab", "-r", f"generateEventAndPulseFiles519('{self.estim_path}/', '{file_name}', {self.single_elec_reps}); exit;"])
        self.generate_bin_file(self.estim_path, file_name)


    def generate_bin_file(self, scan_path, file_name):
        """
        Generate a BIN file from S*F files.
        """

        print(f"Generating BIN file at {scan_path}")
        subprocess.run(["cp", "-R", config.BIN_GENERATION_CLK_PATH, scan_path])
        subprocess.run(["python", "-c", f"from stanford_stim_generation import main; main.PH_main(\"{file_name}\", timeWindow=5000, folder=\"{scan_path}\", verbose=True, output=None, evaluate=False, num_workers=None);"])


        print(f"Copying BIN file to {self.bin_file_path}")
        subprocess.run(["cp", os.path.join(scan_path, f"{file_name}.bin"), self.bin_file_path])
        

    def stream_vision(self, datarun, wn="RGB-8-2"):
        """
        Run Vision on a streaming white noise datarun.
        """

        # Drop .xml to generate stimulus movie on the fly
        # Default monitor size is 640x320 (divided by stixel size) and default refresh rate is 119.5 Hz
        xml = wn + "-0.48-11111"

        print(f"Running Vision on datarun {datarun} with xml {xml}")
        proc = subprocess.Popen(["/Volumes/Lab/Development/scripts/smash", "-r", "-e", self.piece, datarun, xml])
    
        return proc
    

    def stream_kilosort2(self, datarun, wn="RGB-8-2", gpu=3):
        """
        Run Kilosort2 on a streaming white noise datarun.
        """

        assert self.server == "peggyo"

        xml = wn + "-0.48-11111.xml"

        print(f"Running Kilosort2 on datarun {datarun} with xml {xml}")
        proc = subprocess.Popen([f"CUDA_VISIBLE_DEVICES={gpu},", "/Volumes/Lab/Development/vision-convert/kilosmash", f"/Volumes/Stream/Data/{self.piece}/{datarun}", f"/Volumes/Acquisition/Analysis/{self.piece}/{datarun}", "-w", "-e", "-l", xml])
    
        return proc

    
    def preprocess_single_electrode_scan(self, estim_datarun):
        """
        Run streaming preprocessing on a single electrode scan.
        """
        
        print(f"Preprocessing single electrode scan to {self.analysis_path}/{estim_datarun}")
        preprocess_proc = subprocess.Popen([f"{config.SHELL_SCRIPTS_PATH}/fast_pp.sh", "-r", self.raw_data_path, "-s", self.stream_data_path, "-a", self.analysis_path, "-e", estim_datarun, "-f", self.stim_files, "-v", self.server, "-n", config.PREPROCESS_SINGLE_ELEC_PATH, "-i", "None"])
        return preprocess_proc

    def copy_vision_analysis(self, wn_datarun):
        """
        Copy completed Vision analysis from Acquisition to analysis directory.
        """

        print(f"Copying Vision analysis from Acquisition to {self.analysis_path}")
        subprocess.run(["cp", "-R", f"/Volumes/Acquisition/Analysis/{self.piece}/{wn_datarun}", self.analysis_path])
        # subprocess.run(["cp", "-R", "/Volumes/Acquisition/Analysis/2024-02-26-1/kilosort_data008/data008", self.analysis_path])

        # Load Vision datasets
        print(f"Loading white noise datarun {wn_datarun}...")
        vision_data = vl.load_vision_data(os.path.join(self.analysis_path, wn_datarun),
                                            wn_datarun,
                                            include_neurons=True,
                                            include_ei=True,
                                            include_params=True,
                                            include_runtimemovie_params=True,
                                            include_sta=True,
                                            include_noise=True)
        
        self.vision_data = vision_data
    
    def gsort(self, wn_datarun, estim_datarun):
        """
        Run gsort.
        """

        cells_arg = " ".join(self.cell_types)

        print(f"Running gsort on {self.cell_types} using white noise datarun {wn_datarun} at {os.path.join(self.gsort_path, estim_datarun)}")


        if self.server == "peggyo":
            gsort_proc = subprocess.Popen([f"{config.SHELL_SCRIPTS_PATH}/gsort_peggyo.sh", "-s", config.STREAMING_GSORT_PATH, "-x", self.piece, "-a", self.analysis_path, "-g", self.gsort_path, "-w", wn_datarun, "-e", estim_datarun, "-c", cells_arg])
        elif self.server == "bertha":
            gsort_proc = subprocess.Popen([f"{config.SHELL_SCRIPTS_PATH}/gsort_bertha.sh", "-s", config.STREAMING_GSORT_PATH, "-x", self.piece, "-a", self.analysis_path, "-g", self.gsort_path, "-w", wn_datarun, "-e", estim_datarun, "-c", cells_arg])

        return gsort_proc
    
    def bundle_algo(self, wn_datarun, estim_datarun, save=True):
        """
        Compute bundle thresholds for a single electrode scan.
        """

        print(f"Computing bundle thresholds on single electrode datarun {estim_datarun}")
        
        if self.board == 512:
            board_type = "60 micron"
            analyzable_elecs = [i+1 for i in range(512)]
        elif self.board == 519:
            board_type = "30 micron"
            analyzable_elecs = [i+1 for i in range(519)]

        # auto_thresholds: (np.array) containing thresholds generated by algorithm with shape Nx2 (col 0: elec || col 1: first amplitude index with bundle activity)
        auto_thresholds = bundle.generate_bundle_thresholds_for_dataset(os.path.join(self.analysis_path, wn_datarun), os.path.join(self.analysis_path, estim_datarun), analyzable_elecs, board_type=board_type)
    
        self.bundle_thresholds = auto_thresholds

        # Save bundle thresholds
        if save:
            temp = os.path.join(self.dictionary_path, f"{wn_datarun}_bundle_thresholds.npz")
            print(f"Saving bundle thresholds to {temp}")
            np.savez(temp, bundle_thresholds=auto_thresholds)
    
    def read_bundle_thresholds(self, wn_datarun):

        print(f"Reading bundle thresholds from {self.dictionary_path}")
        bundle_thresholds = np.load(os.path.join(self.dictionary_path, f"{wn_datarun}_bundle_thresholds.npz"))['bundle_thresholds']

        self.bundle_thresholds = bundle_thresholds

    def run_vision_mapping_analysis(self, wn_datarun, vstim_datarun, xml="/Volumes/Lab/Development/vision-xml/current/rrs-primate-otf.xml"):
        """
        Run Vision mapping analysis on visual stimulation data.
        """

        mapping_source = os.path.join(self.analysis_path, wn_datarun)
        mapping_dest = os.path.join(self.analysis_path, f"{vstim_datarun}_from_{wn_datarun}")
        source = f"/Volumes/Stream/Data/{self.piece}/{vstim_datarun}.bin"
        # source = f"/Volumes/Scratch/Users/ajphillips/tmp/2024-08-20-0/data007.bin"

        mapping_source = f"{mapping_source}"
        mapping_dest = f"{mapping_dest}"
        source = f"{source}"

        print(f"Running Vision mapping analysis on visual stimulation datarun {vstim_datarun} using white noise datarun {wn_datarun}")
        proc = subprocess.Popen(["java", "-Xmx20G", "-Xss1G", "-classpath", VISION, VISION_MAP_FUNC, mapping_source, mapping_dest, source, "-c", xml])

        return proc

    # def run_vision_mapping_analysis_electrical(self, wn_datarun, mapping_datarun, xml="/Volumes/Lab/Development/vision-xml/current/rrs-primate-otf.xml"):
    #     """
    #     Run Vision mapping analysis on electrical stimulation data.
    #     """

    #     mapping_source = os.path.join(self.analysis_path, wn_datarun)
    #     mapping_dest = os.path.join(self.analysis_path, f"TODO{mapping_datarun}")
    #     source = f"/Volumes/Stream/Data/{self.piece}/TODO{mapping_datarun}.bin"
    #     # source = f"/Volumes/Scratch/Users/ajphillips/tmp/2023-12-13-1/data013/data013.bin"

    #     mapping_source = f"{mapping_source}"
    #     mapping_dest = f"{mapping_dest}"
    #     source = f"{source}"

    #     print(f"Running Vision mapping analysis on datarun {mapping_datarun} using white noise datarun {wn_datarun}")
    #     proc = subprocess.Popen(["java", "-Xmx20G", "-Xss1G", "-classpath", VISION, VISION_MAP_FUNC, mapping_source, mapping_dest, source, "-c", xml])

    #     return proc
    
    def load_vision_mapping_analysis(self, wn_datarun, vstim_datarun):
        """
        Load Vision mapping analysis.
        """

        print(f"Loading Vision mapping analysis")
        vision_data_vstim = vl.load_vision_data(os.path.join(self.analysis_path, f"{vstim_datarun}_from_{wn_datarun}"),
                                            f"{vstim_datarun}_from_{wn_datarun}",
                                            include_neurons=True)
        
        self.vision_data_vstim = vision_data_vstim

    def make_litke_scan(self, label=""):
        """
        Read in the SEF arrays and generate the files needed to deliver the electrical stimulation.
        """

        repeat_all_sef_arrays = np.load(os.path.join(self.dictionary_path, f"spike_trains{label}.npz"), allow_pickle=True)['sef']
        repeat_all_sef_arrays = repeat_all_sef_arrays.tolist()

        print(f"Saving SEF to {self.estim_path}")
        
        ranges = gen_multi_experiment_litke_sef(
            sef_arrays=repeat_all_sef_arrays, # list in order you want to do the experiments
            save_path = os.path.join(self.estim_path, f"spike_trains{label}.sef"),
            beginning_neg_event = -4, # This neg event will occur at time 0 on all electrodes
            dump_txt=True # by default is set to false, saves the sef as plain text with .sef_txt extension
        )

        np.savez(os.path.join(self.estim_path, f"ranges{label}.npz"), ranges=ranges)

        print(f"The complete SEF is {ranges[-1][-1]/20000} seconds")

        print(f"Copying SIF and SLF files for BIN generation to {self.estim_path}")
        subprocess.run(["cp", f"{self.stim_files}.sif", os.path.join(self.estim_path, f"spike_trains{label}.sif")])
        subprocess.run(["cp", f"{self.stim_files}.slf", os.path.join(self.estim_path, f"spike_trains{label}.slf")])

        self.generate_bin_file(self.estim_path, f"spike_trains{label}")

    def preprocess_litke_scan(self, estim_datarun, tasks, trials, whole, pp_info_prefix="preprocessing_info", label=""):
        """
        Run streaming preprocessing on the electrical stimulation scan.
        """

        print(f"Preprocessing electrical stimulation scan to {self.analysis_path}/{estim_datarun}")

        pp_info_filename = f"{pp_info_prefix}{label}.mat"

        litke_stim_files = os.path.join(self.estim_path, f"spike_trains{label}")
        
        _ = pp.preprocess_spike_trains_info(self.estim_path, tasks, trials, whole, write=True, filename=pp_info_filename, label=label)

        litke_preprocess_proc = subprocess.Popen([f"{SHELL_SCRIPTS_PATH}/fast_pp.sh", "-r", self.raw_data_path, "-s", self.stream_data_path, "-a", self.analysis_path, "-e", estim_datarun, "-f", litke_stim_files, "-v", self.server, "-n", PREPROCESS_GDM_PATH, "-i", os.path.join(self.estim_path, pp_info_filename)])
        return litke_preprocess_proc

    @staticmethod
    def kill(proc):
        """
        Recursively kill a process.
        """
        process = psutil.Process(proc.pid)
        for p in process.children(recursive=True):
            p.kill()
        process.kill()
        
    @staticmethod
    def touch_path(path):
        """
        Create a directory if it doesn't already exist.
        """
        if not os.path.exists(path):
            os.makedirs(path)