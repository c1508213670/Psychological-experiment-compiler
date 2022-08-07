%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Class/Function 3: eventData_resp_msg_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  a class used to store the behavioral data of a event that has both defined response and trigger/message (e.g., for Eyelink)
% Written by Yang Zhang 2020-Dec-16
classdef eventData_resp_msg_APL < handle
properties
	rt   = [];          % used to record reaction time
	resp = [];          % used to record response key code(s)
	acc  = 0;           % used to indicate whether the response is correct
	onsetTime     = []; % used to record the onset time of the event
	respOnsetTime = []; % used to record the onset time of the response
	msgEndTime    = []; % used to record the offset time of sending trigger/message
end 
end %  end of subfun3