%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Class: eventData_msg_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%a class used to store the behavioral data of a event that has no defined response but has defined trigger/message (e.g., for Eyelink)
% Written by Yang Zhang 2020-Dec-16
classdef eventData_msg_APL < handle
properties
	onsetTime  = []; % used to record the onsettime of the event
	msgEndTime = []; % used to record the offsettime of sending trigger/message
end 
end