function dotsData = initialDotPos(nDots,direction,coherence,isOval,w,h)
% a sub-function to calculate the initial dot positions for do motion stim
% argins:
% nDots     [double] a scaler double denote the number of dots
% direction [double] a scaler double (0~ 360) defines the direction of coherence motion
% coherence [double] a scaler double (0~100) defines the percentage of dots moved coherently
% isOval   [boolean] a boolean indicates whether to use the inscribed circle to filter out dots
% w, h     [double]  indicates the width and height of the area respectively
% argouts:
% dotsData [4*nDots double matrix] : col 1-4 correspond to x, y, direction, and show or not
% Written by Yang Zhang 20201-Dec-16

nCohDots = round(nDots*coherence/100);

dotsData = zeros(4, nDots); %  rows: x, y, direction, isShow  



dotsData(1,:) = rand(1,nDots)*w - w/2;
dotsData(2,:) = rand(1,nDots)*h - h/2;
dotsData(3,:) = [repmat(direction*pi/180,1,nCohDots),rand(1,nDots - nCohDots)*2*pi];

if isOval
	dotsData(4,:) = dotsData(1,:).^2/(w/2) + dotsData(2,:).^2/(h/2) <= 1; 
else
	dotsData(4,:) = 1;
end 

end