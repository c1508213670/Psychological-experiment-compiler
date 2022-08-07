

function ShowHideWinTaskbar(IDX)
% Usage:
% IDX: 0 and 1 for hide and show the task bar respectively!
% 
% written by Yang Zhang
% 2014/1/4 10:49:12
% 
if ~exist('IDX','var')
    IDX = 1;% show the task bar
end

if ispc
    OSstr = computer;
    
    if strfind(OSstr,'64')
        ShowHideWinTaskbarMex(IDX); % for 64bit win 7
    % else
    %     ShowHideWinTaskbarMex(IDX);          % for win xp, was obsoleted as PTB did not support XP anymore
    end
end