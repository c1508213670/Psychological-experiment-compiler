function lptOut(portAdd,value)
% send TTL trigger via matlab under linux
% USAGE:
% % lptoutMex(port,value)
%
% Argins:
% portAdd       [double]: Port address (e.g., 888 = 0x378 )
% value         [double]: value to write (0-255)
%
% Examples:
% lptout(888,42);  
%
% Author: Yang Zhang, Soochow University, Suzhou,China 2015
% Fri Jan 23 21:01:09 2015

lptoutMex(portAdd,value);