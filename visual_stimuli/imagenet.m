%% data000
%% White noise initial classification RGB-8-2-0.48-11111
% STREAM 15 MINUTES

fprintf('\n\n<strong> Random Noise </strong>\n');
clear parameters stimulus

parameters.class = 'RN';
parameters.back_rgb = [1 1 1]*0.5;
parameters.rgb = [1 1 1]*0.48;
parameters.seed = 11111;
parameters.binary = 1;
parameters.probability = 1;
parameters.jitter = 0;
parameters.delay_frames = 0;

%%%%%%%%%%%%%% CRT %%%%%%%%%%%%%%
parameters.x_start = 0;  parameters.x_end = 639;
parameters.y_start = 80;   parameters.y_end = 399;

parameters.independent = 1;
parameters.stixel_width = 8;
parameters.interval = 2;

parameters.frames = 120*1800; % 120*length of stimulus in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);
display_stimulus(stimulus, 'wait_trigger', 1, 'erase', 0);

%%
%% data001
%% RECONSTRUCTION interleaved with test images 5750s
% trigger interval = 0.5
% Fixed Images 10000 images per movie = 5750s per movie + change
mglClearScreen(0.45); mglFlush; mglClearScreen(0.45); mglFlush;
fprintf('\n\n<strong> Raw Movie </strong>\n');
clear parameters stimulus time_stamps;
n_images = 10000;
n_reps = 10;
im_per_block=n_images/n_reps;
interval = 12;

parameters.class = 'RM';
parameters.back_rgb = [1 1 1]*0.45;
parameters.x_start = 0; % x_end and y_end wil depend on movie size (and stixel size)!
parameters.y_start = 80;
parameters.stixel_width = 2;
parameters.stixel_height = 2;
parameters.interval = interval;
parameters.flip = 1;  % 1 = normal; 2 = vertical flip; 3 = horizontal flip; 4 = vertical + horizontal flip
parameters.reverse = 0;   % 1 = backward (reverse), 0 = forward
parameters.frames = interval;

SF = 1;
for i_rep = 1:n_reps
    parameters.start_frame = SF;
    parameters.movie_name = ['/Users/vision/Desktop/Stimuli/ImageNet_stix2_0_045.rawMovie'];
    stimulus = make_stimulus(parameters, def_params);
    for i = 1:im_per_block
        time_stamps{i} = display_stimulus(stimulus, 'trigger_interval', 100, 'wait_trigger',1, 'erase', 1, 'wait_key', 0);
        parameters.start_frame = parameters.start_frame + 1;
        stimulus = make_stimulus(parameters, def_params);
    end
    parameters.movie_name = ['/Users/vision/Desktop/Stimuli/ImageNetTest_v2.rawMovie'];
    parameters.start_frame = 1;
    stimulus = make_stimulus(parameters, def_params);
    for i = 1:150
        time_stamps{i} = display_stimulus(stimulus, 'trigger_interval', 100, 'wait_trigger',1, 'erase', 1, 'wait_key', 0);
        parameters.start_frame = parameters.start_frame + 1;
        stimulus = make_stimulus(parameters, def_params);
    end
    SF = SF + im_per_block;
end

%%
%% data002
%% RECONSTRUCTION interleaved with test images 5750s
% trigger interval = 0.5
% Fixed Images 10000 images per movie = 5750s per movie + change
mglClearScreen(0.45); mglFlush; mglClearScreen(0.45); mglFlush;
fprintf('\n\n<strong> Raw Movie </strong>\n');
clear parameters stimulus time_stamps;
n_images = 10000;
n_reps = 10;
im_per_block=n_images/n_reps;
interval = 12;

parameters.class = 'RM';
parameters.back_rgb = [1 1 1]*0.45;
parameters.x_start = 0; % x_end and y_end wil depend on movie size (and stixel size)!
parameters.y_start = 80;
parameters.stixel_width = 2;
parameters.stixel_height = 2;
parameters.interval = interval;
parameters.flip = 1;  % 1 = normal; 2 = vertical flip; 3 = horizontal flip; 4 = vertical + horizontal flip
parameters.reverse = 0;   % 1 = backward (reverse), 0 = forward
parameters.frames = interval;

SF = 1;
for i_rep = 1:n_reps
    parameters.start_frame = SF;
    parameters.movie_name = ['/Users/vision/Desktop/Stimuli/ImageNet_stix2_1_045.rawMovie'];
    stimulus = make_stimulus(parameters, def_params);
    for i = 1:im_per_block
        time_stamps{i} = display_stimulus(stimulus, 'trigger_interval', 100, 'wait_trigger',1, 'erase', 1, 'wait_key', 0);
        parameters.start_frame = parameters.start_frame + 1;
        stimulus = make_stimulus(parameters, def_params);
    end
    parameters.movie_name = ['/Users/vision/Desktop/Stimuli/ImageNetTest_v2.rawMovie'];
    parameters.start_frame = 1;
    stimulus = make_stimulus(parameters, def_params);
    for i = 1:150
        time_stamps{i} = display_stimulus(stimulus, 'trigger_interval', 100, 'wait_trigger',1, 'erase', 1, 'wait_key', 0);
        parameters.start_frame = parameters.start_frame + 1;
        stimulus = make_stimulus(parameters, def_params);
    end
    SF = SF + im_per_block;
end


%% data003

%% White noise initial classification RGB-8-2-0.48-11111
% STREAM 15 MINUTES

fprintf('\n\n<strong> Random Noise </strong>\n');
clear parameters stimulus

parameters.class = 'RN';
parameters.back_rgb = [1 1 1]*0.5;
parameters.rgb = [1 1 1]*0.48;
parameters.seed = 11111;
parameters.binary = 1;
parameters.probability = 1;
parameters.jitter = 0;
parameters.delay_frames = 0;

%%%%%%%%%%%%%% CRT %%%%%%%%%%%%%%
parameters.x_start = 0;  parameters.x_end = 639;
parameters.y_start = 80;   parameters.y_end = 399;

parameters.independent = 1;
parameters.stixel_width = 8;
parameters.interval = 4;

parameters.frames = 120*1800; % 120*length of stimulus in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);
display_stimulus(stimulus, 'wait_trigger', 1, 'erase', 0);

%% data004

%% White noise initial classification RGB-16-2-0.48-11111
% STREAM 15 MINUTES

fprintf('\n\n<strong> Random Noise </strong>\n');
clear parameters stimulus

parameters.class = 'RN';
parameters.back_rgb = [1 1 1]*0.5;
parameters.rgb = [1 1 1]*0.48;
parameters.seed = 11111;
parameters.binary = 1;
parameters.probability = 1;
parameters.jitter = 0;
parameters.delay_frames = 0;

%%%%%%%%%%%%%% CRT %%%%%%%%%%%%%%
parameters.x_start = 0;  parameters.x_end = 639;
parameters.y_start = 80;   parameters.y_end = 399;

parameters.independent = 1;
parameters.stixel_width = 16;
parameters.interval = 2;

parameters.frames = 120*3600; % 120*length of stimulus in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);
display_stimulus(stimulus, 'wait_trigger', 1, 'erase', 0);


%% data005
%% BW White noise rasters BW-16-2-0.48
% 30 repeats, 10 sec each
fprintf('\n\n<strong> Random Noise </strong>\n');
clear parameters stimulus

parameters.class = 'RN';
parameters.back_rgb = [1 1 1]*0.5;
parameters.rgb = [1 1 1]*0.48;
parameters.seed = 22222;
parameters.binary = 1;
parameters.probability = 1;
parameters.jitter = 0;
parameters.delay_frames = 0;
nrepeat = 30;
%%%%%%%%%%%%%% OLED %%%%%%%%%%%%%%
% parameters.x_start = 1;  parameters.x_end = 800;
% parameters.y_start = 1;   parameters.y_end = 600;

%%%%%%%%%%%%%% CRT %%%%%%%%%%%%%%
parameters.x_start = 0;  parameters.x_end = 639;
parameters.y_start = 80;   parameters.y_end = 399;

parameters.independent = 1;
parameters.interval = 2;
parameters.stixel_width = 16;
parameters.frames = 120*30; % 120*length of each repeat

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

% For Voronoi, set stixel_height and stixel_width to 1 and pass a map path
% parameters.map_file_name = [my_path, '/Maps/2011-12-13-2_f04_vorcones/map-0000.txt'];

stimulus = make_stimulus(parameters, def_params);

for i  = 1:nrepeat
    display_stimulus(stimulus, 'wait_trigger', 1, 'erase', 0);
end


%% data006

%% White noise initial classification RGB-8-2-0.48-11111
% STREAM 15 MINUTES

fprintf('\n\n<strong> Random Noise </strong>\n');
clear parameters stimulus

parameters.class = 'RN';
parameters.back_rgb = [1 1 1]*0.5;
parameters.rgb = [1 1 1]*0.48;
parameters.seed = 22222;
parameters.binary = 1;
parameters.probability = 1;
parameters.jitter = 0;
parameters.delay_frames = 0;

%%%%%%%%%%%%%% CRT %%%%%%%%%%%%%%
parameters.x_start = 0;  parameters.x_end = 639;
parameters.y_start = 80;   parameters.y_end = 399;

parameters.independent = 1;
parameters.stixel_width = 8;
parameters.interval = 2;

parameters.frames = 120*3600; % 120*length of stimulus in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);
display_stimulus(stimulus, 'wait_trigger', 1, 'erase', 0);

%% data007

%% BW White noise rasters BW-16-2-0.48
% 30 repeats, 30 sec each
fprintf('\n\n<strong> Random Noise </strong>\n');
clear parameters stimulus

parameters.class = 'RN';
parameters.back_rgb = [1 1 1]*0.5;
parameters.rgb = [1 1 1]*0.48;
parameters.seed = 33333;
parameters.binary = 1;
parameters.probability = 1;
parameters.jitter = 0;
parameters.delay_frames = 0;
nrepeat = 30;
%%%%%%%%%%%%%% OLED %%%%%%%%%%%%%%
% parameters.x_start = 1;  parameters.x_end = 800;
% parameters.y_start = 1;   parameters.y_end = 600;

%%%%%%%%%%%%%% CRT %%%%%%%%%%%%%%
parameters.x_start = 0;  parameters.x_end = 639;
parameters.y_start = 80;   parameters.y_end = 399;

parameters.independent = 1;
parameters.interval = 2;
parameters.stixel_width = 8;
parameters.frames = 120*30; % 120*length of each repeat

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

% For Voronoi, set stixel_height and stixel_width to 1 and pass a map path
% parameters.map_file_name = [my_path, '/Maps/2011-12-13-2_f04_vorcones/map-0000.txt'];

stimulus = make_stimulus(parameters, def_params);

for i  = 1:nrepeat
    display_stimulus(stimulus, 'wait_trigger', 1, 'erase', 0);
end

%% data008

%% White noise initial classification RGB-8-2-0.48-11111
% STREAM 15 MINUTES

fprintf('\n\n<strong> Random Noise </strong>\n');
clear parameters stimulus

parameters.class = 'RN';
parameters.back_rgb = [1 1 1]*0.5;
parameters.rgb = [1 1 1]*0.48;
parameters.seed = 11111;
parameters.binary = 1;
parameters.probability = 1;
parameters.jitter = 1;
parameters.delay_frames = 0;

%%%%%%%%%%%%%% CRT %%%%%%%%%%%%%%
parameters.x_start = 0;  parameters.x_end = 639;
parameters.y_start = 80;   parameters.y_end = 399;

parameters.independent = 1;
parameters.stixel_width = 8;
parameters.interval = 2;

parameters.frames = 120*1800; % 120*length of stimulus in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);
display_stimulus(stimulus, 'wait_trigger', 1, 'erase', 0);


%%
%% Raw Movie
% data009
% 3300sec, 
% 10 blocks of one 250s fitting stimulus and one 75s testing stimulus

% set the background screen to the right value
mglClearScreen(0.45); mglFlush; mglClearScreen(0.45); mglFlush;

fprintf('\n\n<strong> Raw Movie </strong>\n');
clear parameters stimulus time_stamps;

% 10 blocks
repeats = 10; 

% for the fitting movie
start_frame_fitting = 1;
frames_fitting = 500*60;
parameters.frames = frames_fitting;
parameters.movie_name = '/Users/vision/Desktop/Stimuli/INbrownian_05s_2500_0A_045.rawMovie';
% when you run again, increment this movie to from 0A -> 0B -> 1A etc

% same for both 
parameters.class = 'RM';
parameters.back_rgb = [1 1 1]*0.45;
parameters.x_start = 0; 
parameters.y_start = 80;
parameters.stixel_width = 2;  
parameters.stixel_height = 2;
parameters.start_frame = 1; 
parameters.interval = 1;
parameters.flip = 1;  % 1 = normal; 2 = vertical flip; 3 = horizontal flip; 4 = vertical + horizontal flip
parameters.reverse = 0;   % 1 = backward (reverse), 0 = forward

% for the testing movie
parameters_test = parameters;
parameters_test.movie_name = '/Users/vision/Desktop/Stimuli/INbrownian_05s_test_045.rawMovie';
parameters_test.frames = 150*60;

% make the stimuli
stimulus_fit = make_stimulus(parameters, def_params);
stimulus_test = make_stimulus(parameters_test, def_params);

count = 1;
for i = 1:repeats
    
    % fit 
    time_stamps{count} = display_stimulus(stimulus_fit, 'trigger_interval', 100, 'wait_key', 0, 'erase', 1, 'wait_trigger', 1);
    count = count + 1;
    
    % update the fitting stimulus
    start_frame_fitting = start_frame_fitting + frames_fitting;
    parameters.start_frame = start_frame_fitting;
    stimulus_fit = make_stimulus(parameters, def_params);

    % testing stimulus
    time_stamps{count} = display_stimulus(stimulus_test, 'trigger_interval', 100, 'wait_key', 0, 'erase', 1, 'wait_trigger', 1);
    count = count + 1;
    
end


%% Raw Movie
% data010
% 3300sec, 
% 10 blocks of one 250s fitting stimulus and one 75s testing stimulus

% set the background screen to the right value
mglClearScreen(0.45); mglFlush; mglClearScreen(0.45); mglFlush;

fprintf('\n\n<strong> Raw Movie </strong>\n');
clear parameters stimulus time_stamps;

% 10 blocks
repeats = 10; 

% for the fitting movie
start_frame_fitting = 1;
frames_fitting = 500*60;
parameters.frames = frames_fitting;
parameters.movie_name = '/Users/vision/Desktop/Stimuli/INbrownian_05s_2500_0B_045.rawMovie';
% when you run again, increment this movie to from 0A -> 0B -> 1A etc

% same for both 
parameters.class = 'RM';
parameters.back_rgb = [1 1 1]*0.45;
parameters.x_start = 0; 
parameters.y_start = 80;
parameters.stixel_width = 2;  
parameters.stixel_height = 2;
parameters.start_frame = 1; 
parameters.interval = 1;
parameters.flip = 1;  % 1 = normal; 2 = vertical flip; 3 = horizontal flip; 4 = vertical + horizontal flip
parameters.reverse = 0;   % 1 = backward (reverse), 0 = forward

% for the testing movie
parameters_test = parameters;
parameters_test.movie_name = '/Users/vision/Desktop/Stimuli/INbrownian_05s_test_045.rawMovie';
parameters_test.frames = 150*60;

% make the stimuli
stimulus_fit = make_stimulus(parameters, def_params);
stimulus_test = make_stimulus(parameters_test, def_params);

count = 1;
for i = 1:repeats
    
    % fit 
    time_stamps{count} = display_stimulus(stimulus_fit, 'trigger_interval', 100, 'wait_key', 0, 'erase', 1, 'wait_trigger', 1);
    count = count + 1;
    
    % update the fitting stimulus
    start_frame_fitting = start_frame_fitting + frames_fitting;
    parameters.start_frame = start_frame_fitting;
    stimulus_fit = make_stimulus(parameters, def_params);

    % testing stimulus
    time_stamps{count} = display_stimulus(stimulus_test, 'trigger_interval', 100, 'wait_key', 0, 'erase', 1, 'wait_trigger', 1);
    count = count + 1;
    
end

%% data011
%% White noise initial classification RGB-8-2-0.48-11111
% STREAM 15 MINUTES

fprintf('\n\n<strong> Random Noise </strong>\n');
clear parameters stimulus

parameters.class = 'RN';
parameters.back_rgb = [1 1 1]*0.5;
parameters.rgb = [1 1 1]*0.48;
parameters.seed = 11111;
parameters.binary = 1;
parameters.probability = 1;
parameters.jitter = 0;
parameters.delay_frames = 0;

%%%%%%%%%%%%%% CRT %%%%%%%%%%%%%%
parameters.x_start = 0;  parameters.x_end = 639;
parameters.y_start = 80;   parameters.y_end = 399;

parameters.independent = 1;
parameters.stixel_width = 8;
parameters.interval = 2;

parameters.frames = 120*1800; % 120*length of stimulus in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);
display_stimulus(stimulus, 'wait_trigger', 1, 'erase', 0);

%% data012
%% White noise BW-4-2-0.48-11111
% STREAM 15 MINUTES

fprintf('\n\n<strong> Random Noise </strong>\n');
clear parameters stimulus

parameters.class = 'RN';
parameters.back_rgb = [1 1 1]*0.5;
parameters.rgb = [1 1 1]*0.48;
parameters.seed = 11111;
parameters.binary = 1;
parameters.probability = 1;
parameters.jitter = 0;
parameters.delay_frames = 0;

%%%%%%%%%%%%%% CRT %%%%%%%%%%%%%%
parameters.x_start = 0;  parameters.x_end = 639;
parameters.y_start = 80;   parameters.y_end = 399;

parameters.independent = 0;
parameters.stixel_width = 4;
parameters.interval = 2;

parameters.frames = 120*7200; % 120*length of stimulus in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);
display_stimulus(stimulus, 'wait_trigger', 1, 'erase', 0);
