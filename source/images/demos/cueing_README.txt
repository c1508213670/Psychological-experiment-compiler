%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Function information:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cueing.m   the main function that you need to run in MATLAB/Octave

possible sub functions:
eventData_resp_APL.m:        a class function to define behavioral data
eventData_resp_msg_APL.m:    a class function to define behavioral data with trigger offset times
eventData_APL.m:             a class function to define behavioral data without response data
eventData_msg_APL.m:         a class function to define behavioral data without response data but with trigger offset times 
subjectInfo.m:               a GUI dialog to acquire subject info in MATLAB
overwriteOrNot.m:            a GUI dialog in MATLAB to determine whether to overwrite existed results file or not
lptOut.m/lptoutMex.mex:      a customized mex file to send trigger via parallel under Linux OS
parPulsemexa64/parPulse.mex: a borrowed mex file to send trigger via parallel under Windows OS

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Data structure of the results file:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

There are three main types of results data:

%Variables about the subject and running environment:

subInfo          [struct]: a structure variable storing the subject's info

	   .name     [string]: name
	   .age      [string]: age
	   .gender   [string]: gender
	   .hand     [string]: handedness
	   .num      [string]: subject number
	   .run      [string]: run number
	   .session  [string]: session number
	   .filename [string]: filename of the results file

monitors         [struct]: a structure variable storing the setting of the monitor device

		.port        [int]:    index of the screen
		.name        [string]: name of the screen
		.bkColor     [RGB]:    background color
		.rect        [vector]: window rect
		.multiSample [int]:    multisample parameter of the screen (for anti-aliasing)
		.gammaFile   [string]: file name of the possible color lookup table
		.oldTable    [double]: raw color lookup table

expStartTime:  [string]: start time of the task
expEndTime:    [string]: end time of the task
cRandSeed:     [double]: random seed


% Dependent variables:

For each event, there is a class vector that records related information.
E.g., suppose we have an event named 'instruction', then there will be a class vector named 'instruction' in the results file.
The possible fields (properties) in the class are listed below:

instruction.rt             [double]: reaction time of the current event
instruction.resp           [double]: response key code(s)
instruction.acc            [double]: accuracy of the response
instruction.onsetTime      [double]: onset time of the event
instruction.respOnsetTime  [double]: onset time of response
instruction.msgEndTime     [double]: offset time of sending trigger/message


% Independent variables:

For each loop, all the attributes defined in the loop table will be recorded by a variable using the below rule:
LoopName.var.variableName will be recorded in LoopName_variableName, e.g., for a loop event named 'blocksLoop': 
blocksLoop.var.Repetitions  -->  blocksLoop_Repetitions
blocksLoop.var.Timeline     -->  blocksLoop_Timeline
                            ...
blocksLoop.var.variableName -->  blocksLoop_variableName
