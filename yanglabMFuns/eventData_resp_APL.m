%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Class/Function 1: eventData_resp_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% a class used to store the behavioral data of a event that has defined response but not has defined trigger/message (e.g., for Eyelink)
% Written by Yang Zhang 2020-Dec-16
classdef eventData_resp_APL < handle
properties
	rt   = [];          % used to record reaction time
	resp = [];          % used to record response key code(s)
	acc  = 0;           % used to indicate whether the response is correct
	onsetTime     = []; % used to record the onset time of the event
	respOnsetTime = []; % used to record the onset time of the response
end 
end %  end of subfun1