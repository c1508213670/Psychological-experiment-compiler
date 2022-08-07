function cueing()
% function generated by PsyBuilder 0.1
% If you use PsyBuilder for your research, then we would appreciate your citing our work in your paper:
% Lin, Z., Yang, Z., Feng, C., & Zhang, Y. (2021, Nov. 17). 
% PsyBuilder: an open-source cross-platform graphical experiment builder for Psychtoolbox with built-in performance optimization. 
% Advances in Methods and Practices in Psychological Science. Accepted and in press 
% https://doi.org/10.31234/osf.io/b43vx. 
%
% To report possible bugs and any suggestions please feel free to drop me an E-mail:
% Yang Zhang
% Ph.D., Prof.
% Attention and Perception Lab (APL)
% Department of Psychology, 
% SooChow University
% zhangyang873@gmail.com 
% Or
% yzhangpsy@suda.edu.cn
% 2022-04-09 02:33:54
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%      begin      
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
global Text_11 Text_15 Text_14 Text_13 Loop_4_Repetitions Loop_4_Timeline Loop_5_Repetitions Loop_5_Timeline Loop_5_untitled_var_1 Loop_5_untitled_var_2 Loop_5_untitled_var_3 beChkedRespDevs abortKeyCode %#ok<*NUSED>

% running engine check: 
if exist('OCTAVE_VERSION', 'builtin') ~= 0
	error('Current running engine is Octave, while you selected Matlab in "running engine" under building menu');
end
% running platform (OS) check: 
if ~IsWin
	error('Current platform is not Windows (you selected Windows in "platform" under building menu)!');
end 

cFolder = fileparts(mfilename('fullpath'));
% get subject information
subInfo = subjectInfo('cueing');
if isempty(subInfo)
	error('Aborted in the subject information dialog ...');
end
try
	KbName('UnifyKeyNames');
	abortKeyCode = KbName('ESCAPE');
	expStartTime = datestr(now,'dd-mmm-YYYY:HH:MM:SS'); %#ok<*NASGU> % record start time 

	%======= Reinitialize the global random seed =======/
	cRandSeed = RandStream('mt19937ar','Seed','shuffle');
	RandStream.setGlobalStream(cRandSeed);
	%===================================================\

	HideCursor;               % hide mouse cursor
	ShowHideWinTaskbarMex(0); % hide the window taskbar
	commandwindow;            % bring the command window into front
	Priority(1);              % bring to high priority
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% define and initialize input/output devices
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%====== define input devices ========/
	kbIndices      = unique(GetKeyboardIndices);
	miceIndices    = unique(GetMouseIndices);
	%====================================\

	%===== define output devices ========/
	monitors(1).port        =  0;
	monitors(1).name        = 'screen_0';
	monitors(1).bkColor     = [128,128,128];
	monitors(1).rect        = [];
	monitors(1).multiSample =  0;
	monitors(1).gammaFile   =  '';
	monitors(1).oldTable    =  [];

	%====================================\

	disableSomeKbKeys_APL; % restrictKeysForKbCheck 

	% initialize variables
	[winIds,winIFIs,lastScrOnsetTime, cDurs] = deal(zeros(1,1));
	nextEvFlipReqTime  = 0;
	fullRects          = zeros(1,4);

	beChkedRespDevs    = struct('eData',[],'allowAble',[],'corResp',[],'rtWindow',[],'endAction',[],'type',[],'index',[],'isQueue',[],'checkStatus',[],'needTobeReset',[],'right',[],'wrong',[],'noResp',[],'respCodeDevType',[],'respCodeDevIdx',[],'start',[],'end',[],'mean',[],'isOval',false);
	beChkedRespDevs(1) = [];

	Text_11 = makeEventResultVar_APL(81, 0, 0);
	Text_15 = makeEventResultVar_APL(81, 0, 0);
	Text_14 = makeEventResultVar_APL(81, 0, 0);
	Text_13 = makeEventResultVar_APL(81, 0, 0);
	 
	[Loop_4_Repetitions,Loop_4_Timeline] = deal(cell(81,1)); % save cycle attrs
	[Loop_5_Repetitions,Loop_5_Timeline,Loop_5_untitled_var_1,Loop_5_untitled_var_2,Loop_5_untitled_var_3] = deal(cell(81,1)); % save cycle attrs
	 
	beFilledVarStruct_APL = makeBeFilledVarStruct_APL;

	% open windows
	for iWin = 1:numel(monitors)
		[winIds(iWin),fullRects(iWin,:)] = Screen('OpenWindow',monitors(iWin).port,monitors(iWin).bkColor,monitors(iWin).rect,[],[],[],monitors(iWin).multiSample);
		Screen('BlendFunction', winIds(iWin),'GL_SRC_ALPHA','GL_ONE_MINUS_SRC_ALPHA'); % force to most common alpha-blending factors
		winIFIs(iWin) = Screen('GetFlipInterval',winIds(iWin));                        % get inter frame interval (i.e., 1/refresh rate)
	end % for iWin 
	 
	flipComShiftDur = winIFIs*0.5; % 0.5 IFI before flip to ensure flipping at a right time
	opRowIdx     = 1;        % used to record the row num of the output variables
	iLoop_0_cOpR = opRowIdx; % used iLoop_*_cOpR to record cTL's output var row
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%loop:0, event1: Text_11
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% change the font settings when it's necessary
	changeFontSetting_APL(winIds(1), 8, 0, '����', [255,255,255], false);

	Text_11_fRect = makeFrameRect_APL(-0.5, -0.5, -1.0, -1.0, fullRects(1,:));
	DrawFormattedText(winIds(1),'Your text will appear here','center','center',[255,0,0],80,0,0,[],0,Text_11_fRect);
	% give the GPU a break
	Screen('DrawingFinished',winIds(1),0);

	Text_11(iLoop_0_cOpR).onsetTime = Screen('Flip',winIds(1),nextEvFlipReqTime,0); %#ok<*STRNU>

	lastScrOnsetTime(1) = Text_11(iLoop_0_cOpR).onsetTime; % temp store the last screen onset time

	% get cDur and the required flip time of the next event
	cDurs(1)          = getDurValue_APL(1000,winIFIs(1));
	nextEvFlipReqTime = cDurs(1) + lastScrOnsetTime(1) - flipComShiftDur(1); % get the required time of the  Flip for the next event 

	% Create the design matrix for loop 'Loop_4'
	Loop_4 = Loop_4_makeData_APL;

	% Shuffle the DesignMatrix
	cShuffledIdx = ShuffleCycleOrder_APL(size(Loop_4.var,1),'Random without Replacement','N/A',subInfo);
	Loop_4.var = Loop_4.var(cShuffledIdx,:);
	 
	[~,~,nextEvFlipReqTime] = checkResp_SendRespTrig_APL(cDurs(1), nextEvFlipReqTime, false);

	% looping across each row of the Loop_4.var:iLoop_1
	for iLoop_1 =1:size(Loop_4.var,1)
		iLoop_1_cOpR = opRowIdx; % output var row num for loop level 1

		% variable values will be recorded in variables named following the rule: Loop_4.var.attName to Loop_4_attName
		% e.g., the attribute variable Loop_4.var.Repetitions will be recorded in variable Loop_4_Repetitions
		% copy attr var values into output vars for row iLoop_1_cOpR
		[Loop_4_Repetitions{iLoop_1_cOpR},Loop_4_Timeline{iLoop_1_cOpR}] = deal(Loop_4.var{iLoop_1,:}{:});

		% switch across timeline types
		switch Loop_4.var.Timeline{iLoop_1}
			case 'ilove'
				% Create the design matrix for loop 'Loop_5'
				Loop_5 = Loop_5_makeData_APL;

				% Shuffle the DesignMatrix
				cShuffledIdx = ShuffleCycleOrder_APL(size(Loop_5.var,1),'Sequential','N/A',subInfo);
				Loop_5.var = Loop_5.var(cShuffledIdx,:);
				 
				% record the start row for the to be filled Loop Loop.4 variables 
				beFilledVarStruct_APL.Loop_4.startEndRows(1, beFilledVarStruct_APL.Loop_4.iCol) = opRowIdx;

				% looping across each row of the Loop_5.var:iLoop_2
				for iLoop_2 =1:size(Loop_5.var,1)
					iLoop_2_cOpR = opRowIdx; % output var row num for loop level 2

					% variable values will be recorded in variables named following the rule: Loop_5.var.attName to Loop_5_attName
					% e.g., the attribute variable Loop_5.var.Repetitions will be recorded in variable Loop_5_Repetitions
					% copy attr var values into output vars for row iLoop_2_cOpR
					[Loop_5_Repetitions{iLoop_2_cOpR},Loop_5_Timeline{iLoop_2_cOpR},Loop_5_untitled_var_1{iLoop_2_cOpR},Loop_5_untitled_var_2{iLoop_2_cOpR},Loop_5_untitled_var_3{iLoop_2_cOpR}] = deal(Loop_5.var{iLoop_2,:}{:});

					% switch across timeline types
					switch Loop_5.var.Timeline{iLoop_2}
						case 'love'
							%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
							%loop:2, event1: Text_15
							%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
							% change the font settings when it's necessary
							changeFontSetting_APL(winIds(1), 12, 0, '����', [255,255,255], false);

							Text_15_fRect = makeFrameRect_APL(-0.5, -0.5, -1.0, -1.0, fullRects(1,:));
							DrawFormattedText(winIds(1),Loop_5.var.untitled_var_2{iLoop_2},'center','center',[0,0,0],80,0,0,[],0,Text_15_fRect);
							% give the GPU a break
							Screen('DrawingFinished',winIds(1),0);

							Text_15(iLoop_2_cOpR).onsetTime = Screen('Flip',winIds(1),nextEvFlipReqTime,0); %#ok<*STRNU>

							lastScrOnsetTime(1) = Text_15(iLoop_2_cOpR).onsetTime; % temp store the last screen onset time

							% get cDur and the required flip time of the next event
							cDurs(1)          = getDurValue_APL(1000,winIFIs(1));
							nextEvFlipReqTime = cDurs(1) + lastScrOnsetTime(1) - flipComShiftDur(1); % get the required time of the  Flip for the next event 

							[~,~,nextEvFlipReqTime] = checkResp_SendRespTrig_APL(cDurs(1), nextEvFlipReqTime, false);

							opRowIdx = opRowIdx + 1; % increase outputVars by 1 only when TL contains no subLoop
						otherwise 
							% do nothing 
					end%switch Loop_5.var.Timeline{iLoop_2}
				end % iLoop_2
				% record the end row num for the to be filled Loop Loop.4 variables 
				beFilledVarStruct_APL.Loop_4.startEndRows(2, beFilledVarStruct_APL.Loop_4.iCol) = opRowIdx;

				beFilledVarStruct_APL.Loop_4.iCol = beFilledVarStruct_APL.Loop_4.iCol + 1;

				%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
				%loop:1, event1: Text_14
				%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
				% change the font settings when it's necessary
				changeFontSetting_APL(winIds(1), 12, 0, '����', [255,255,255], false);

				Text_14_fRect = makeFrameRect_APL(-0.5, -0.5, -1.0, -1.0, fullRects(1,:));
				DrawFormattedText(winIds(1),iLoop_1,'center','center',[128,128,128],80,0,0,[],0,Text_14_fRect);
				% give the GPU a break
				Screen('DrawingFinished',winIds(1),0);

				Text_14(iLoop_1_cOpR).onsetTime = Screen('Flip',winIds(1),nextEvFlipReqTime,0); %#ok<*STRNU>

				lastScrOnsetTime(1) = Text_14(iLoop_1_cOpR).onsetTime; % temp store the last screen onset time

				% get cDur and the required flip time of the next event
				cDurs(1)          = getDurValue_APL(1000,winIFIs(1));
				nextEvFlipReqTime = cDurs(1) + lastScrOnsetTime(1) - flipComShiftDur(1); % get the required time of the  Flip for the next event 

				[~,~,nextEvFlipReqTime] = checkResp_SendRespTrig_APL(cDurs(1), nextEvFlipReqTime, false);

			otherwise 
				% do nothing 
		end%switch Loop_4.var.Timeline{iLoop_1}
	end % iLoop_1
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%loop:0, event2: Text_13
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% change the font settings when it's necessary
	changeFontSetting_APL(winIds(1), 12, 0, '����', [255,255,255], false);

	Text_13_fRect = makeFrameRect_APL(-0.5, -0.5, -1.0, -1.0, fullRects(1,:));
	DrawFormattedText(winIds(1),'Your text will appear here','center','center',[0,0,0],80,0,0,[],0,Text_13_fRect);
	% give the GPU a break
	Screen('DrawingFinished',winIds(1),0);

	Text_13(iLoop_0_cOpR).onsetTime = Screen('Flip',winIds(1),nextEvFlipReqTime,0); %#ok<*STRNU>

	lastScrOnsetTime(1) = Text_13(iLoop_0_cOpR).onsetTime; % temp store the last screen onset time

	% get cDur and the required flip time of the next event
	cDurs(1)          = getDurValue_APL(1000,winIFIs(1));
	nextEvFlipReqTime = cDurs(1) + lastScrOnsetTime(1) - flipComShiftDur(1); % get the required time of the  Flip for the next event 

	[~,~,nextEvFlipReqTime] = checkResp_SendRespTrig_APL(cDurs(1), nextEvFlipReqTime, false);

	% for the last event in timeline just wait for duration
	WaitSecs('UntilTime', nextEvFlipReqTime); 

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% end of the main exp procedure
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	expEndTime = datestr(now,'dd-mmm-YYYY:HH:MM:SS'); % record the end time 

	sca;                                % Close opened windows
	ShowCursor;                         % Show the hid mouse cursor
	Priority(0);                        % Turn the priority back to normal
	RestrictKeysForKbCheck([]);         % Re-enable all keys
	ShowHideWinTaskbarMex(1);              % show the window taskbar.
	fillResultVars_APL(opRowIdx, beFilledVarStruct_APL);   % update results vars for analysis
	save(subInfo.filename);             % save the results

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% end of the experiment
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

catch cueing_error

	%#ok<*TRYNC>
	sca;                                % Close opened windows
	ShowCursor;                         % Show the hid mouse cursor
	Priority(0);                        % Turn the priority back to normal
	RestrictKeysForKbCheck([]);         % Re-enable all keys
	

	ShowHideWinTaskbarMex(1);              % show the window taskbar
	save([subInfo.filename,'_debug']);
	rethrow(cueing_error);
end % try
%  







%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                   Nested subfunctions               %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Embody subfun 1: Loop_4_makeData_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function Loop_4 = Loop_4_makeData_APL()
% create the designMatrix for the loop: Loop_4
Loop_4.var = cell2table({...
{2} {'ilove'} ;...
{2} {'ilove'} ;...
{2} {'ilove'} ;...
{2} {'ilove'} ;...
{2} {'ilove'} ;...
{2} {'ilove'} ;...
{2} {'ilove'} ;...
{2} {'ilove'} ;...
{1} {'ilove'} ;...
},'VariableNames',{'Repetitions' 'Timeline' });

end %  end of subfun 1

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Embody subfun 2: Loop_5_makeData_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function Loop_5 = Loop_5_makeData_APL()
% create the designMatrix for the loop: Loop_5
Loop_5.var = cell2table({...
{2} {'love'} {'red'} {[0,0,255]} {'s'} ;...
{2} {'love'} {'red'} {[0,0,255]} {'s'} ;...
{2} {'love'} {'yellow'} {[0,0,255]} {'s'} ;...
{2} {'love'} {'yellow'} {[0,0,255]} {'s'} ;...
{2} {'love'} {'red'} {[0,0,255]} {'a'} ;...
{2} {'love'} {'red'} {[0,0,255]} {'a'} ;...
{2} {'love'} {'blue'} {[0,100,255]} {'s'} ;...
{2} {'love'} {'blue'} {[0,100,255]} {'s'} ;...
{1} {'love'} {'red'} {[0,0,255]} {'s'} ;...
},'VariableNames',{'Repetitions' 'Timeline' 'untitled_var_1' 'untitled_var_2' 'untitled_var_3' });

end %  end of subfun 2

end % main function 







%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                      Subfunctions                   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 1: changeFontSetting_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function changeFontSetting_APL(winIdx, fontSize, fontStyle, fontName, bkColor,isSingleDraw)
% we change the font settings only when it's necessary,
% which is faster than changing the font settings every frame
persistent oldSize oldStyle oldName OldBkColor
if ~isequal(fontSize,oldSize)
	Screen('TextFont',winIdx, fontSize);
	oldSize = fontSize;
end 

if ~isequal(fontStyle, oldStyle)
	Screen('TextStyle',winIdx, fontStyle);
	oldStyle = fontStyle;
end 

if ~strcmp(fontName,oldName)
	Screen('TextFont',winIdx, fontName);
	oldName = fontName;
end 

if isSingleDraw
	OldBkColor = bkColor;
elseif ~isequal(bkColor,OldBkColor)
	Screen('TextBackgroundColor',winIdx, bkColor);
	OldBkColor = bkColor;
end 

end %  end of subfun 1

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 2: fillResultVars_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function fillResultVars_APL(opRowIdx, beFilledVarStruct_APL)%#ok<*INUSD,*INUSL>
global Text_11 Text_15 Text_14 Text_13 Loop_4_Repetitions Loop_4_Timeline Loop_5_Repetitions Loop_5_Timeline Loop_5_untitled_var_1 Loop_5_untitled_var_2 Loop_5_untitled_var_3

resultVarNames = {'Text_11', 'Text_15', 'Text_14', 'Text_13', 'Loop_4_Repetitions', 'Loop_4_Timeline', 'Loop_5_Repetitions', 'Loop_5_Timeline', 'Loop_5_untitled_var_1', 'Loop_5_untitled_var_2', 'Loop_5_untitled_var_3'};
allBeFilledLoopAttVarNames = {'Loop_4_Repetitions', 'Loop_4_Timeline'};
fieldNames = fields(beFilledVarStruct_APL);

for iVar = 1:numel(allBeFilledLoopAttVarNames)
	for iField = 1:numel(fieldNames)
		cSubStruct = beFilledVarStruct_APL.(fieldNames{iField});
		if ismember(allBeFilledLoopAttVarNames{iVar},cSubStruct.varNames)
			evalc([allBeFilledLoopAttVarNames{iVar}, ' = updateResultVar_APL(',allBeFilledLoopAttVarNames{iVar},', opRowIdx, cSubStruct.startEndRows);']);
			break;
		end % ismember
	end % iField: for each Loop
end % iVar

% for rest result variables and no need filled attributes
resultVarNames(ismember(resultVarNames,allBeFilledLoopAttVarNames)) = [];
for iVar = 1:numel(resultVarNames)
	evalc([resultVarNames{iVar}, ' = updateResultVar_APL(',resultVarNames{iVar},', opRowIdx, []);']);  
end % iVar
end %  end of subfun 2

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 3: updateResultVar_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function beUpdatedVar = updateResultVar_APL(beUpdatedVar,opRowIdx,startEndRows) %#ok<*DEFNU>
if numel(beUpdatedVar) > 1
	beUpdatedVar(opRowIdx+1:end) = [];

	startEndRows(:,~sum(startEndRows,1)) = []; % remove the empty cols
	for iCol = 1:size(startEndRows,2)
		if iscell(beUpdatedVar)
			% for attributes in cycle
			if isempty(beUpdatedVar{startEndRows(1,iCol)})
				beUpdatedVar(startEndRows(1,iCol)+1:startEndRows(2,iCol)) = beUpdatedVar(startEndRows(1,iCol));
			end 
		else
			% for event log vars
			if isempty(beUpdatedVar(startEndRows(1,iCol)).onsetTime)
				beUpdatedVar(startEndRows(1,iCol)+1:startEndRows(2,iCol)) = beUpdatedVar(startEndRows(1,iCol));
			end
		end %  iscell(beUpdatedVar)
		
	end % iCol
end % if numel(beUpdatedVar) > 1
end %  end of subfun 3

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 4: checkResp_SendRespTrig_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [isTerminateStimEvent, secs, nextEvFlipReqTime] = checkResp_SendRespTrig_APL(cDur, nextEvFlipReqTime, isOneTimeCheck)
global abortKeyCode beChkedRespDevs

isTerminateStimEvent = false;
secs                 = GetSecs; 

allTypeIndex = [beChkedRespDevs(:).type;beChkedRespDevs(:).index]';
uniqueDevs   = unique(allTypeIndex,'rows');

if ~isempty(beChkedRespDevs) && any([beChkedRespDevs(:).checkStatus])
	while secs < nextEvFlipReqTime && any([beChkedRespDevs(:).checkStatus])
		% loop across each unique resp dev: 
		for iUniDev = 1:size(uniqueDevs,1)
			cRespDevsIdx = find(ismember(uniqueDevs(iUniDev,:),allTypeIndex,'rows'));

			if any([beChkedRespDevs(cRespDevsIdx).checkStatus])
				[secs,keyCode,fEventOr1stRelease] = responseCheck_APL(uniqueDevs(iUniDev,1),uniqueDevs(iUniDev,2));

				% check aborted key
				if keyCode(abortKeyCode)
					error('The program was aborted ...!');
				end 

				for iRespDev = cRespDevsIdx
					% if RT window is not negative and cTime is out of RT Window
					if beChkedRespDevs(iRespDev).rtWindow > 0 && (secs - beChkedRespDevs(iRespDev).eData.onsetTime) > beChkedRespDevs(iRespDev).rtWindow
						beChkedRespDevs(iRespDev).checkStatus = 0; % 0, 1, 2 for off, press check and release check, respectively
						continue;
					end 

					if beChkedRespDevs(iRespDev).checkStatus == 1
						cValidRespKeys = ~~keyCode(beChkedRespDevs(iRespDev).allowAble);

						if any(cValidRespKeys)
							if beChkedRespDevs(iRespDev).respCodeDevType == 82 % Eyelink eye action
								beChkedRespDevs(iRespDev).eData.respOnsetTime = fEventOr1stRelease.time;
							else
								beChkedRespDevs(iRespDev).eData.respOnsetTime = secs;
							end 
							

							beChkedRespDevs(iRespDev).eData.resp = intersect(find(keyCode),beChkedRespDevs(iRespDev).allowAble(cValidRespKeys));

							beChkedRespDevs(iRespDev).eData.rt = beChkedRespDevs(iRespDev).eData.respOnsetTime - beChkedRespDevs(iRespDev).eData.onsetTime; 
							if beChkedRespDevs(iRespDev).respCodeDevType == 82 % 82 is Eyelink eye action
								beChkedRespDevs(iRespDev).eData.acc = all(ismember(beChkedRespDevs(iRespDev).eData.resp, beChkedRespDevs(iRespDev).corResp)) && isEyeActionInROIs_APL(fEventOr1stRelease, beChkedRespDevs(iRespDev));
							else 
								beChkedRespDevs(iRespDev).eData.acc = all(ismember(beChkedRespDevs(iRespDev).eData.resp, beChkedRespDevs(iRespDev).corResp));
							end 

							switch beChkedRespDevs(iRespDev).endAction
								case 2
									% end action: terminate till release
									beChkedRespDevs(iRespDev).checkStatus = 2;

								case 1
									% end action: terminate
									beChkedRespDevs(iRespDev).checkStatus = 0;
									isTerminateStimEvent                  = true; % will break out the while loop soon
								case 0
									% end action: none
									beChkedRespDevs(iRespDev).checkStatus = 0;
								otherwise
									error('End action type should be of [0 1 2]!');
							end%switch 
							 
						end % if there was a response

						% check key release 
					elseif beChkedRespDevs(iRespDev).checkStatus == 2
						if any(~keyCode(beChkedRespDevs(iRespDev).eData.resp))
							beChkedRespDevs(iRespDev).checkStatus = 0;
							isTerminateStimEvent                  = true; % will break out the while loop soon
						end 
						

					end % if the check switch is on
				end % for iRespDev
			end % if any([beChkedRespDevs(cRespDevsIdx).checkStatus])
		end % iUnique Dev

		% after checking all respDev, break out the respCheck while loop
		if isTerminateStimEvent 
			nextEvFlipReqTime = 0;
			break; 
		end 

		if isOneTimeCheck 
			break; 
		end 

		% to give the cpu a little bit break
		if ~isOneTimeCheck
			WaitSecs(0.001);
		end 

	end % while

	% remove unchecked respDevs
	if numel(beChkedRespDevs) > 0
		beChkedRespDevs(~[beChkedRespDevs(:).checkStatus]) = [];
	end 

	% when no resp && cDur is reached
	if numel(beChkedRespDevs) > 0 && secs >= nextEvFlipReqTime
		% for resp dev that have rtWindow == 'same as duration' (no need to check this respDev)
		cEndDevsIdx  = [beChkedRespDevs(:).rtWindow] == -1;

		% update acc info for each RespDevs
		for iRespDev = find(cEndDevsIdx)
			if isempty(beChkedRespDevs(iRespDev).corResp)
				beChkedRespDevs(iRespDev).eData.acc = 1;
			end 
		end 

		% remove no need to be checked Devs
		beChkedRespDevs(cEndDevsIdx) = []; 
	end % if

else
	detectAbortKey_APL(abortKeyCode);
end % if numel(beChkedRespDevs) > 0

end %  end of subfun 4

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 5: detectAbortKey_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function detectAbortKey_APL(abortKeyCode)
[keyIsDown, ~, keyCode] = KbCheck(-1);
if keyIsDown && keyCode(abortKeyCode)
	error('The program was aborted by the experimenter...!');
end 
end %  end of subfun 5

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 6: disableSomeKbKeys_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function disableSomeKbKeys_APL()
RestrictKeysForKbCheck(unique(KbName('escape')));

end %  end of subfun 6

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 7: makeFrameRect_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function outRect = makeFrameRect_APL(x, y, frameWidth, frameHeight, fullRect)
if x <= 0
	x = -x*fullRect(3);
end % if
if y <= 0
	y = -y*fullRect(4);
end % if
if frameWidth <= 0
	frameWidth = -frameWidth*fullRect(3);
end % if
if frameHeight <= 0
	frameHeight = -frameHeight*fullRect(4);
end % if
outRect = CenterRectOnPointd([0, 0, frameWidth, frameHeight], x, y);
end %  end of subfun 7

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 8: ShuffleCycleOrder_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function cShuffledIdx = ShuffleCycleOrder_APL(nRows,orderStr,orderByStr,subInfo)
cShuffledIdx = 1:nRows;
switch orderStr
	case 'Sequential'
		% do nothing
	case 'Random without Replacement'
		cShuffledIdx = Shuffle(cShuffledIdx);
	case 'Random with Replacement'
		cShuffledIdx = Randi(nRows,[nRows,1]);
	case 'Counter Balance'
		switch orderByStr
			case 'N/A'
			case 'Subject'
				cCBRow = rem(str2double(subInfo.num),nRows);
				if cCBRow == 0
					cCBRow = nRows;
				end
				cShuffledIdx = cShuffledIdx(cCBRow);
			case 'Session'
				cCBRow = rem(str2double(subInfo.session),nRows);
				if cCBRow == 0
					cCBRow = nRows;
				end
				cShuffledIdx = cShuffledIdx(cCBRow);
			case 'Run'
				cCBRow = rem(str2double(subInfo.run),nRows);
				if cCBRow == 0
					cCBRow = nRows;
				end
				cShuffledIdx = cShuffledIdx(cCBRow);
			otherwise
				error('Order By should be of {''Run'',''Subject'',''Session'',''N/A''}');
		end%switch 
	otherwise
		error('order methods should be of {''Sequential'',''Random without Replacement'',''Random with Replacement'',''Counter Balance''}');
end%switch 
end %  end of subfun 8

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 9: getDurValue_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function cDur = getDurValue_APL(cDur,cIFI, isSound)
if nargin < 3
	isSound = false;
end
if numel(cDur) > 1
	cDur = rand*(cDur(2) - cDur(1)) + cDur(1);
end 
cDur = cDur./1000; % transform the unit from ms to sec
if ~isSound
	cDur = round(cDur/cIFI)*cIFI;
end 
end %  end of subfun 9

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 10: makeRespStruct_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function makeRespStruct_APL(eData,allowAble,corResp,rtWindow,endAction,devType,index,isQueue,checkStatus,needTobeReset,right,wrong,noResp,respCodeDevType,respCodeDevIdx,startRect,endRect,meanRect,isOval)
global beChkedRespDevs  %#ok<*REDEF>
% this method is a little bit ugly, but surprisingly it's faster than the struct function
cIdx = numel(beChkedRespDevs) + 1;
beChkedRespDevs(cIdx).eData           = eData; %#ok<*STRNU>
beChkedRespDevs(cIdx).allowAble       = allowAble;
beChkedRespDevs(cIdx).corResp         = corResp;
beChkedRespDevs(cIdx).rtWindow        = rtWindow;
beChkedRespDevs(cIdx).endAction       = endAction;
beChkedRespDevs(cIdx).type            = devType;
beChkedRespDevs(cIdx).index           = index;
beChkedRespDevs(cIdx).isQueue         = isQueue;
beChkedRespDevs(cIdx).checkStatus     = checkStatus;
beChkedRespDevs(cIdx).needTobeReset   = needTobeReset;
beChkedRespDevs(cIdx).right           = right;
beChkedRespDevs(cIdx).wrong           = wrong;
beChkedRespDevs(cIdx).noResp          = noResp;
beChkedRespDevs(cIdx).respCodeDevType = respCodeDevType;
beChkedRespDevs(cIdx).respCodeDevIdx  = respCodeDevIdx;
beChkedRespDevs(cIdx).start           = startRect;
beChkedRespDevs(cIdx).end             = endRect;
beChkedRespDevs(cIdx).mean            = meanRect;
beChkedRespDevs(cIdx).isOval          = isOval;
end %  end of subfun 10
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 11: responseCheck_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [secs, keyCode, fEventOr1stRelease]= responseCheck_APL(respDevType,respDevIndex)
% respDevType 1,2,3,4,82 for keyboard, mouse, gamepad, response box and Eyelink eye action, respectively
fEventOr1stRelease = [];
switch respDevType
	case 3 % under windows, check it via joystickMex
		status    = joystickMex(respDevIndex); % index starts from 0
		keyCode   = bitget(status(5),1:8);
		secs      = GetSecs;
		keyIsDown = any(keyCode);
	case 4 % for Cedrus's response boxes
		status    = CedrusResponseBox('FlushEvents', respDevIndex);
		keyCode   = status(1,:);
		secs      = GetSecs;
	otherwise % keyboard or mouse or gamepad (except for window OS)
		[~, secs, keyCode] = KbCheck(respDevIndex);
end%switch 

end %  end of subfun 11

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 12: makeImDestRect_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [dRect, sRect] = makeImDestRect_APL(fRect,imDataSize,stretchMode)

sRect = [0 0 imDataSize(2) imDataSize(1)];
dRect   = CenterRect(sRect, fRect);
% calculate the width:
if ismember(stretchMode,[1 3])
	dRect([1,3]) = fRect([1,3]);
end 
% calculate the height
if ismember(stretchMode,[2 3])
	dRect([2,4]) = fRect([2,4]);
end
% in case of no stretch and the imData is larger than fRect
if stretchMode == 0
	dRect = ClipRect(dRect, fRect);
end % if stretchMode
end %  end of subfun 12

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 13: isEyeActionInROIs_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function isInROIs = isEyeActionInROIs_APL(fEvent, respDevs)
iEye = fEvent.eye + 1; % 0 1 for left and right
isInROIs = isInRect_APL(fEvent.gstx(iEye),fEvent.gsty(iEye),respDevs.start, respDevs.isOval) &...
           isInRect_APL(fEvent.genx(iEye),fEvent.geny(iEye),respDevs.end, respDevs.isOval) &...
           isInRect_APL(fEvent.gavx(iEye),fEvent.gavy(iEye),respDevs.mean, respDevs.isOval);
end %  end of subfun 13

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 14: isInRect_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function isInRectArea = isInRect_APL(x, y, cRect, isOval)
% determine whether the point defined by (x,y) is within the area defined by cRect
if numel(cRect) ~= 4
	isInRectArea = true;
else
	if isOval
		[cx, cy] = RectCenterd(cRect);
		isInRectArea = all(((x - cx)/RectWidth(cRect)).^2 + ((y - cy)/RectHeight(cRect)).^2 <= 0.25);
	else
		isInRectArea = IsInRect(x, y, cRect);
	end
end
end %  end of subfun 14

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 15: makeBeFilledVarStruct_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function beFilledVarStruct_APL = makeBeFilledVarStruct_APL()
beFilledVarStruct_APL.Loop_4.varNames     = {'Loop_4_Repetitions', 'Loop_4_Timeline'};
beFilledVarStruct_APL.Loop_4.startEndRows = zeros(2, 14);
beFilledVarStruct_APL.Loop_4.iCol         = 1;

end %  end of subfun 15

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subfun 16: makeEventResultVar_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function outVar = makeEventResultVar_APL(maxRows,haveOutPutDev,haveRespDev)
% a batch style function to initialize the results variable for events
% argins:
% maxRows       [double]: the maximum number of rows for the current event
% haveOutPutDev [0 or 1]: indicates whether the current event contains at least one output device
% haveRespDev   [0 or 1]: indicates whether the current event needs any response 

if haveOutPutDev
	if haveRespDev
		outVar(maxRows,1) = eventData_resp_msg_APL;
	else
		outVar(maxRows,1) = eventData_msg_APL;
	end % haveRespDev
else
	if haveRespDev
		outVar(maxRows,1) = eventData_resp_APL;
	else
		outVar(maxRows,1) = eventData_APL;
	end % haveRespDev
end % haveOutPutDev
end %  end of subfun
