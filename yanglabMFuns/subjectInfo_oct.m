% A Octave GUI to acquire subject information
% ## 2021.06.17 Yang Zhang
% ## Useful since Octave 6.0
function  output = subjectInfo_oct(varargin)
  h.output = [];

% open file 
if numel(varargin) > 0
  expNameStr = varargin{1};
else
  error('subjectinfo require at least one input parameter!');
end


h.expName = expNameStr;

h.savePath = fileparts(mfilename('fullpath'));


h.nameStr     = 'Yang Zhang';
h.ageStr      = '38';
h.genderValue = 1;
h.handValue   = 1;

h.runStr     = '1';
h.numStr     = '1';
h.sessionStr = '1';

% load history file from last.subinfo
try %#ok<TRYNC>
    lastSavedData = load(fullfile(h.savePath,'last.subinfo'),'-mat');

    h.nameStr = lastSavedData.output.name;
    h.ageStr = lastSavedData.output.age;


	if strcmpi(lastSavedData.output.gender,'female')
        h.genderValue = 2;
	end

	if strcmpi(lastSavedData.output.hand,'right')
        h.handValue = 2;
	end

	try
	    h.runStr = num2str(str2double(lastSavedData.output.run)+1);
	end

  if isempty(sessionDefault)
    h.sessionStr = lastSavedData.output.session;
  end

  clear lastSavedData;

end



% ## plot title
oldgkit = graphics_toolkit;

if ~strcmp(oldgkit,'qt')
    graphics_toolkit('qt');
end


cScreenSize = get(0,'ScreenSize');
screenPos   = [(cScreenSize(3)-560)/2,(cScreenSize(4)-420)/2,560,420];


fh = dialog('name','Subject Information',"color", get(0, "defaultuicontrolbackgroundcolor"),'toolbar','none','menubar','none','windowstyle','modal','Position',screenPos);

h.name_edit = uicontrol (fh,"style", "edit",
                               "units", "normalized",
                               "string", h.nameStr,
                               "BackgroundColor", [1 1 1],
                               "position", [0.404825737265416 0.853896103896104 0.294906166219839 0.0844155844155844]);

h.age_edit = uicontrol (fh,"style", "edit",
                               "units", "normalized",
                               "string", h.ageStr,
                               "BackgroundColor", [1 1 1],
                               "position", [0.404825737265416 0.717532467532468 0.294906166219839 0.0844155844155844]);

h.subnum_edit = uicontrol (fh,"style", "edit",
                               "units", "normalized",
                               "string", h.numStr,
                               "BackgroundColor", [1 1 1],
                               "position", [0.15 0.22 0.15 0.0844155844155844]);

h.runnum_edit = uicontrol (fh,"style", "edit",
                               "units", "normalized",
                               "string", h.runStr,
                               "BackgroundColor", [1 1 1],
                               "position", [0.425 0.22 0.15 0.0844155844155844]);

h.sessionnum_edit = uicontrol (fh,"style", "edit",
                               "units", "normalized",
                               "string", h.sessionStr,
                               "BackgroundColor", [1 1 1],
                               "position", [0.7 0.22 0.15 0.0844155844155844]);

## labels
h.name_label = uicontrol (fh,"style", "text",
                               "units", "normalized",
                               "string", "Name:",
                               "horizontalalignment", "right",
                               "position", [0.265415549597855 0.857142857142857 0.131367292225201 0.0714285714285714]);

 h.gender_label = uicontrol (fh,"style", "text",
                               "units", "normalized",
                               "string", "Gender:",
                               "horizontalalignment", "right",
                               "position", [0.2171581769437 0.574675324675325 0.179624664879357 0.0714285714285714]);


h.Age_label = uicontrol (fh,"style", "text",
                               "units", "normalized",
                               "string", "Age:",
                               "horizontalalignment", "right",
                               "position", [0.289544235924933 0.724025974025974 0.107238605898123 0.0714285714285714]);


h.handedness_label = uicontrol (fh,"style", "text",
                               "units", "normalized",
                               "string", "Handedness:",
                               "horizontalalignment", "right",
                               "position", [0.193029490616622 0.428571428571429 0.203753351206434 0.0779220779220779]);


h.subnum_label = uicontrol (fh,"style", "text",
                               "units", "normalized",
                               "string", "SubjectNum:",
                               "horizontalalignment", "center",
                               "position", [0.15 0.31 0.15 0.064935064935065]);


h.runnum_label = uicontrol (fh,"style", "text",
                               "units", "normalized",
                               "string", "Run:",
                               "horizontalalignment", "center",
                               "position", [0.425 0.31 0.15 0.0616883116883117]);


h.sessionnum_label = uicontrol (fh,"style", "text",
                               "units", "normalized",
                               "string", "Session:",
                               "horizontalalignment", "center",
                               "position", [0.7 0.31 0.15 0.0616883116883117]);

h.designer_label = uicontrol (fh,"style", "text",
                               "units", "normalized",
                               "string", "Designed by Yang Zhang, Psy, Soochow University, China",
                               "horizontalalignment", "center",
                               "position", [0.015 0.001 0.97 0.0551948051948052]);

## popupmenus
h.gender_popup = uicontrol (fh,"style", "popupmenu",
                               "units", "normalized",
                               "string", {"male",
                                          "female"},
                                          "value", h.genderValue,
                               "position", [0.404825737265416 0.568181818181818 0.294906166219839 0.0844155844155844]);

h.handedness_popup = uicontrol (fh,"style", "popupmenu",
                               "units", "normalized",
                               "string", {"left",
                                          "right"},
                                "value", h.handValue,
                               "position", [0.404825737265416 0.435064935064935 0.294906166219839 0.0844155844155844]);


## pushbutton

## print figure
h.yes_pushbutton = uicontrol (fh,"style", "pushbutton",
                                "units", "normalized",
                                "string", "Ok",
                                "callback", @outputFunc,
                                "ButtonDownFcn", @outputFunc,
                                "KeyPressFcn", @output_keypress_Func,
                                "position", [0.168900804289544 0.08 0.227882037533512 0.095]);

h.no_pushbutton = uicontrol (fh,"style", "pushbutton",
                                "units", "normalized",
                                "string", "Quit",
                                "callback", @quitFunc,
                                "ButtonDownFcn", @quitFunc,
                                "KeyPressFcn", @quit_keypress_Func,
                                "position", [0.571045576407507 0.08 0.227882037533512 0.095]);


## markerstyle

guidata(fh, h);
uiwait(fh);

if ishghandle(fh)
    h = guidata(fh);
    delete(fh);
end
    output = h.output;


    if ~strcmp(oldgkit,'qt')
        graphics_toolkit(oldgkit);
    end

end % end of the mainfunction



function quitFunc(obj)
  uiresume(get(obj, 'parent'));
  
end

function quit_keypress_Func(obj,eventdata)
  if strcmpi(eventdata.Key,'return')
%      h = guidata (obj);

      uiresume(get(gcbo, 'parent'));
  end
end


function outputFunc(obj)
  h = guidata (obj);
    handle_Yes_event(obj, h);
end

function output_keypress_Func(obj, eventdata)
if strcmpi(eventdata.Key,'return')
  h = guidata (obj);
  handle_Yes_event(obj, h);
end

end % end of subfun


function handle_Yes_event(cObj, h)

  output.name    = get(h.name_edit,      'string');
  output.age     = get(h.age_edit,       'string');
  output.num     = get(h.subnum_edit,    'string');
  output.run     = get(h.runnum_edit,    'string');
  output.session = get(h.sessionnum_edit,'string');

  if get(h.gender_popup,'Value') == 1
      output.gender = 'male';
  else
      output.gender = 'female';
  end

  if get(h.handedness_popup,'Value') == 1
      output.hand = 'left';
  else
      output.hand = 'right';
  end

  output.filename = [h.expName,'_',output.num,'_',output.run,'_',output.session];

  if exist(fullfile(h.savePath,[output.filename,'.mat']),'file')
    set(get(cObj, 'parent'),'Visible','off');
    isOverWrite = overwriteOrNot_oct(output.filename);

    if isOverWrite
        save('-mat', fullfile(fileparts(mfilename('fullpath')),'last.subinfo'),'output');
        h.output = output;
        guidata(cObj, h);

        uiresume(get(cObj, 'parent'));
    else
        set(get(cObj, 'parent'),'Visible','on');
    end

  else

    save('-mat', fullfile(fileparts(mfilename('fullpath')),'last.subinfo'),'output');
    h.output = output;
    guidata(cObj, h);

    uiresume(get(cObj, 'parent'));
  end

end