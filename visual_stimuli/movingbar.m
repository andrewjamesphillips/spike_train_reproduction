%% data000
fprintf('\n\n<strong> Coarse Random Noise </strong>\n');
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
parameters.y_start = 0;   parameters.y_end = 479;

parameters.independent = 1;
parameters.interval = 2; % SPEED
parameters.stixel_width = 10; % SIZE (1 pixel = 1.8 micron, CRT would be 5.5 micron)
parameters.frames = round(119.5*1800); % number of frames in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;  
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);

[time_stamps] = display_stimulus(stimulus, 'wait_trigger', 1);


%% data001
fprintf('\n\n<strong> Coarse Random Noise </strong>\n');
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
parameters.y_start = 0;   parameters.y_end = 479;

parameters.independent = 0;
parameters.interval = 2; % SPEED
parameters.stixel_width = 10; % SIZE (1 pixel = 1.8 micron, CRT would be 5.5 micron)
parameters.frames = round(119.5*3600); % number of frames in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;  
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);

[time_stamps] = display_stimulus(stimulus, 'wait_trigger', 1);


%% data002
fprintf('\n\n<strong> Coarse Random Noise </strong>\n');
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
parameters.y_start = 0;   parameters.y_end = 479;

parameters.independent = 0;
parameters.interval = 2; % SPEED
parameters.stixel_width = 5; % SIZE (1 pixel = 1.8 micron, CRT would be 5.5 micron)
parameters.frames = round(119.5*7000); % number of frames in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;  
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);

[time_stamps] = display_stimulus(stimulus, 'wait_trigger', 1);

%% data003
%% Raw Movie
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
parameters.x_start = 161; 
parameters.y_start = 161;
parameters.stixel_width = 1;  
parameters.stixel_height = 1;
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

%% data004 Moving bar 5 reps, 8 dirs, 840 frames per trial (7s+1s to trigger) = 5.33 min

% TRIGGER INTERVAL 7.99
fprintf('\n\n<strong> Moving bar. </strong>\n');
clear parameters stimulus;

parameters.class = 'MB';
parameters.back_rgb = [1 1 1]*0.5;
parameters.rgb = -[1, 1, 1]*0.48;
parameters.bar_width = 10;
parameters.delta = 1;  % pixels per frame; ~ 5 degres per s
parameters.x_start = 1;  parameters.x_end = 640;
parameters.y_start = 1;   parameters.y_end = 480;
parameters.frames = 840;
parameters.delay_frames = 0;

variable_parameters = randomize_parameters('direction', [0 45 90 135 180 225 270 315], 'nrepeats',5);
path2file = write_s_file(parameters, variable_parameters);
s_params = read_s_file(path2file);


% see second option example in "S File read"
for i=2:size(s_params,2)
    trial_params = combine_parameters(s_params{1}, s_params{i});
    stimulus{i-1} = make_stimulus(trial_params, def_params);
    display_stimulus(stimulus{i-1}, 'wait_trigger', 1);
end

%%%%%%%%%% clean up %%%%%%%%%% 
for i=1:length(stimulus)
    for j=1:stimulus{i}.temporal_period
        mglDeleteTexture(stimulus{i}.texture{j});
    end
end

% white
mglClearScreen(1);
mglFlush


%% data005 Moving WHITE bar 5 reps, 8 dirs, 840 frames per trial (7s+1s to trigger) = 5.33 min; 
% TRIGGER INTERVAL 7.99
fprintf('\n\n<strong> Moving bar. </strong>\n');
clear parameters stimulus;

parameters.class = 'MB';
parameters.back_rgb = [1 1 1]*0.5;
parameters.rgb = [1, 1, 1]*0.48;
parameters.bar_width = 10;
parameters.delta = 1;  % pixels per frame; ~ 5 degres per s
parameters.x_start = 1;  parameters.x_end = 640;
parameters.y_start = 1;   parameters.y_end = 480;
parameters.frames = 840;
parameters.delay_frames = 0;

variable_parameters = randomize_parameters('direction', [0 45 90 135 180 225 270 315], 'nrepeats',5);
path2file = write_s_file(parameters, variable_parameters);
s_params = read_s_file(path2file);


% see second option example in "S File read"
for i=2:size(s_params,2)
    trial_params = combine_parameters(s_params{1}, s_params{i});
    stimulus{i-1} = make_stimulus(trial_params, def_params);
    display_stimulus(stimulus{i-1}, 'wait_trigger', 1);
end

%%%%%%%%%% clean up %%%%%%%%%% 
for i=1:length(stimulus)
    for j=1:stimulus{i}.temporal_period
        mglDeleteTexture(stimulus{i}.texture{j});
    end
end

% white
mglClearScreen(0.5);
mglFlush



%% data006
fprintf('\n\n<strong> Coarse Random Noise </strong>\n');
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
parameters.y_start = 0;   parameters.y_end = 479;

parameters.independent = 1;
parameters.interval = 2; % SPEED
parameters.stixel_width = 10; % SIZE (1 pixel = 1.8 micron, CRT would be 5.5 micron)
parameters.frames = round(119.5*3600); % number of frames in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;  
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);

[time_stamps] = display_stimulus(stimulus, 'wait_trigger', 1);


%% data007  NSEM RUN
% TRIGGER INTERVAL 0.99
fprintf('\n\n<strong> Raw Movie </strong>\n');
clear parameters stimulus time_stamps;
% For repeats
parameters.frames = 22793*4; %120 frames, 1800s

% Movie Name
parameters.movie_name = '/Users/vision/Desktop/Stimuli/run.rawMovie';
% Don't need to change
parameters.class = 'RM';
parameters.back_rgb = [1 1 1]*0.25;
parameters.x_start = 1; % x_end and y_end wil depend on movie size (and stixel size)!
parameters.y_start = 1;
parameters.stixel_width = 1;
parameters.stixel_height = 1;
parameters.start_frame = 1; % >0
parameters.interval = 4;
parameters.flip = 1;  % 1 = normal; 2 = vertical flip; 3 = horizontal flip; 4 = vertical + horizontal flip
parameters.reverse = 0;   % 1 = backward (reverse), 0 = forward

stimulus = make_stimulus(parameters, def_params);
time_stamps = display_stimulus(stimulus, 'trigger_interval', 100, 'wait_trigger',1, 'erase', 1);

% movie runs for 15 min, then 15 min gray


%% data008  NSEM RUN repeats
% TRIGGER INTERVAL 0.99
fprintf('\n\n<strong> Raw Movie </strong>\n');
clear parameters stimulus time_stamps;
% For repeats
parameters.frames = 1793*4; %120 frames, 1800s

% Movie Name
parameters.movie_name = '/Users/vision/Desktop/Stimuli/run.rawMovie';
% Don't need to change
parameters.class = 'RM';
parameters.back_rgb = [1 1 1]*0.25;
parameters.x_start = 1; % x_end and y_end wil depend on movie size (and stixel size)!
parameters.y_start = 1;
parameters.stixel_width = 1;
parameters.stixel_height = 1;
parameters.start_frame = 1; % >0
parameters.interval = 4;
parameters.flip = 1;  % 1 = normal; 2 = vertical flip; 3 = horizontal flip; 4 = vertical + horizontal flip
parameters.reverse = 0;   % 1 = backward (reverse), 0 = forward
parameters.start_frame = 21000;
stimulus = make_stimulus(parameters, def_params);

n_repeats = 1;

for i = 1:n_repeats
    time_stamps = display_stimulus(stimulus, 'trigger_interval', 100, 'wait_trigger',1, 'erase', 1);
end
% movie runs for 15 min, then 15 min gray

%% data009  NSEM RUN repeats
% TRIGGER INTERVAL 0.99
fprintf('\n\n<strong> Raw Movie </strong>\n');
clear parameters stimulus time_stamps;
% For repeats
parameters.frames = 1793*4; %120 frames, 1800s

% Movie Name
parameters.movie_name = '/Users/vision/Desktop/Stimuli/run.rawMovie';
% Don't need to change
parameters.class = 'RM';
parameters.back_rgb = [1 1 1]*0.25;
parameters.x_start = 1; % x_end and y_end wil depend on movie size (and stixel size)!
parameters.y_start = 1;
parameters.stixel_width = 1;
parameters.stixel_height = 1;
parameters.start_frame = 1; % >0
parameters.interval = 4;
parameters.flip = 1;  % 1 = normal; 2 = vertical flip; 3 = horizontal flip; 4 = vertical + horizontal flip
parameters.reverse = 0;   % 1 = backward (reverse), 0 = forward
parameters.start_frame = 21000;
stimulus = make_stimulus(parameters, def_params);

n_repeats = 10;

for i = 1:n_repeats
    time_stamps = display_stimulus(stimulus, 'trigger_interval', 100, 'wait_trigger',1, 'erase', 0);
end
% movie runs for 15 min, then 15 min gray


%% data010
%% Raw Movie
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
parameters.x_start = 161; 
parameters.y_start = 161;
parameters.stixel_width = 1;  
parameters.stixel_height = 1;
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

%% data 011 gray

%% data012 gray

%% data013 coarse WN jitter

fprintf('\n\n<strong> Coarse Random Noise </strong>\n');
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
parameters.y_start = 0;   parameters.y_end = 479;

parameters.independent = 0;
parameters.interval = 2; % SPEED
parameters.stixel_width = 10; % SIZE (1 pixel = 1.8 micron, CRT would be 5.5 micron)
parameters.frames = round(119.5*1800); % number of frames in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;  
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);

[time_stamps] = display_stimulus(stimulus, 'wait_trigger', 1);



%% data014 COARSE WHITE NOISE SPARSE JITTER; BW-40-36, prob 1/50

fprintf('\n\n<strong> Coarse Random Noise </strong>\n');
clear parameters stimulus

parameters.class = 'RN';
parameters.back_rgb = [1 1 1]*0.5;
parameters.rgb = [1 1 1]*0.48;
parameters.seed = 11111;
parameters.binary = 1;
parameters.probability = 1/50;
parameters.jitter = 1;
parameters.delay_frames = 0;

%%%%%%%%%%%%%% CRT %%%%%%%%%%%%%% 
parameters.x_start = 0;  parameters.x_end = 639;
parameters.y_start = 0;   parameters.y_end = 479;

parameters.independent = 0;
parameters.interval = 36; % SPEED
parameters.stixel_width = 40; % SIZE (1 pixel = 1.8 micron, CRT would be 5.5 micron)
parameters.frames = round(119.5*1800); % number of frames in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;  
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);

[time_stamps] = display_stimulus(stimulus, 'wait_trigger', 1);

%% data015 coarse WN with OFFSETS - CHANGE CODE

fprintf('\n\n<strong> Coarse Random Noise </strong>\n');
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
parameters.y_start = 0;   parameters.y_end = 479;

parameters.independent = 0;
parameters.interval = 2; % SPEED
parameters.stixel_width = 10; % SIZE (1 pixel = 1.8 micron, CRT would be 5.5 micron)
parameters.frames = round(119.5*3600); % number of frames in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;  
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);

[time_stamps] = display_stimulus(stimulus, 'wait_trigger', 1);


%% data016  movie balloons
% TRIGGER INTERVAL 0.99
fprintf('\n\n<strong> Raw Movie </strong>\n');
clear parameters stimulus time_stamps;
% For repeats

parameters.frames = 97200; %810s

% Movie Name
parameters.movie_name = '/Users/vision/Desktop/Stimuli/balloons_compiled_v1.rawMovie';
% Don't need to change
parameters.class = 'RM';
parameters.back_rgb = [1 1 1]*0.25;
parameters.x_start = 1; % x_end and y_end wil depend on movie size (and stixel size)!
parameters.y_start = 1;
parameters.stixel_width = 2;
parameters.stixel_height = 2;
parameters.start_frame = 1; % >0
parameters.interval = 1;
parameters.flip = 1;  % 1 = normal; 2 = vertical flip; 3 = horizontal flip; 4 = vertical + horizontal flip
parameters.reverse = 0;   % 1 = backward (reverse), 0 = forward

stimulus = make_stimulus(parameters, def_params);
time_stamps = display_stimulus(stimulus, 'trigger_interval', 100, 'wait_trigger',1, 'erase', 1);

parameters.flip = 2;  % 1 = normal; 2 = vertical flip; 3 = horizontal flip; 4 = vertical + horizontal flip
stimulus = make_stimulus(parameters, def_params);
time_stamps = display_stimulus(stimulus, 'trigger_interval', 100, 'wait_trigger',1, 'erase', 1);


parameters.flip = 3;  % 1 = normal; 2 = vertical flip; 3 = horizontal flip; 4 = vertical + horizontal flip
stimulus = make_stimulus(parameters, def_params);
time_stamps = display_stimulus(stimulus, 'trigger_interval', 100, 'wait_trigger',1, 'erase', 1);


parameters.flip = 4;  % 1 = normal; 2 = vertical flip; 3 = horizontal flip; 4 = vertical + horizontal flip
stimulus = make_stimulus(parameters, def_params);
time_stamps = display_stimulus(stimulus, 'trigger_interval', 100, 'wait_trigger',1, 'erase', 1);


%% data 017  WN + sparse
% TRIGGER INTERVAL 0.99
fprintf('\n\n<strong> Raw Movie </strong>\n');
clear parameters stimulus time_stamps;

parameters.frames = 119.5*3600; %3600s

% Movie Name
parameters.movie_name = '/Users/vision/Desktop/Stimuli/wn_plus_sparse.rawMovie';
% Don't need to change
parameters.class = 'RM';
parameters.back_rgb = [1 1 1]*0.25;
parameters.x_start = 211; % x_end and y_end wil depend on movie size (and stixel size)!
parameters.y_start = 161;
parameters.stixel_width = 1;
parameters.stixel_height = 1;
parameters.start_frame = 1; % >0
parameters.interval = 2;
parameters.flip = 1;  % 1 = normal; 2 = vertical flip; 3 = horizontal flip; 4 = vertical + horizontal flip
parameters.reverse = 0;   % 1 = backward (reverse), 0 = forward

stimulus = make_stimulus(parameters, def_params);
time_stamps = display_stimulus(stimulus, 'trigger_interval', 100, 'wait_trigger',1, 'erase', 1);

%% data 018  WN + sparse
% TRIGGER INTERVAL 0.99
fprintf('\n\n<strong> Raw Movie </strong>\n');
clear parameters stimulus time_stamps;

parameters.frames = 119.5*3600; %3600s

% Movie Name
parameters.movie_name = '/Users/vision/Desktop/Stimuli/wn_plus_sparse.rawMovie';
% Don't need to change
parameters.class = 'RM';
parameters.back_rgb = [1 1 1]*0.25;
parameters.x_start = 211; % x_end and y_end wil depend on movie size (and stixel size)!
parameters.y_start = 161;
parameters.stixel_width = 1;
parameters.stixel_height = 1;
parameters.start_frame = 1; % >0
parameters.interval = 2;
parameters.flip = 1;  % 1 = normal; 2 = vertical flip; 3 = horizontal flip; 4 = vertical + horizontal flip
parameters.reverse = 0;   % 1 = backward (reverse), 0 = forward

stimulus = make_stimulus(parameters, def_params);
time_stamps = display_stimulus(stimulus, 'trigger_interval', 100, 'wait_trigger',1, 'erase', 1);


%% data019 moving grating half contrast; 5s, 8 directions, 2 temporal periods, 2 spatial periods, 7 repeats, 3s between

% Moving Grating S File write
% trigger interval 7.99
fprintf('\n\n<strong> Moving Grating. </strong>\n');
clear parameters stimulus

parameters.class = 'MG';
parameters.spatial_modulation = 'sine'; % sine or square
parameters.rgb = [1 1 1]*0.24;
parameters.back_rgb = [1 1 1]*0.5;
parameters.frames = 5*120; % presentation of each grating, frames
parameters.x_start = 0;  parameters.x_end =639;
parameters.y_start = 0;   parameters.y_end = 479;
% parameters.direction = [0 90];

variable_parameters = randomize_parameters('direction', [0 45 90 135 180 225 270 315], 'temporal_period', [30 60], 'spatial_period', [20,40], 'nrepeats',7);
path2file = write_s_file(parameters, variable_parameters);
s_params = read_s_file(path2file);

% see second option example in "S File read"
for i=2:size(s_params,2)
    trial_params = combine_parameters(s_params{1}, s_params{i});
    stimulus{i-1} = make_stimulus(trial_params, def_params);
    display_stimulus(stimulus{i-1}, 'wait_trigger', 1);
end



%% data020
fprintf('\n\n<strong> Coarse Random Noise </strong>\n');
clear parameters stimulus

parameters.class = 'RN';
parameters.back_rgb = [1 1 1]*0.5;
parameters.rgb = [1 1 1]*0.48;
parameters.seed = 22222;
parameters.binary = 1;
parameters.probability = 1;
parameters.jitter = 1;
parameters.delay_frames = 0;

%%%%%%%%%%%%%% CRT %%%%%%%%%%%%%% 
parameters.x_start = 0;  parameters.x_end = 639;
parameters.y_start = 0;   parameters.y_end = 479;

parameters.independent = 1;
parameters.interval = 2; % SPEED
parameters.stixel_width = 10; % SIZE (1 pixel = 1.8 micron, CRT would be 5.5 micron)
parameters.frames = round(119.5*1800); % number of frames in seconds

parameters.stixel_height = parameters.stixel_width;
parameters.field_width = (parameters.x_end-parameters.x_start+1)/parameters.stixel_width;  
parameters.field_height = (parameters.y_end-parameters.y_start+1)/parameters.stixel_height;

stimulus = make_stimulus(parameters, def_params);

[time_stamps] = display_stimulus(stimulus, 'wait_trigger', 1);
