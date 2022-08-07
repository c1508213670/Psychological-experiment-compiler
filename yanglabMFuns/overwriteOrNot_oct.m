function varargout = overwriteOrNot_oct(varargin)
% GUI for Octave to overwrite the exited result file or not
% Written by Yang Zhang 08-Jun-2020 21:49:45
if nargin < 1
    error('Overwrite or not require at least one input!');
end 

expNameStr = varargin{1};

h.isOverwrite = false;
cScreenSize = get(0,'ScreenSize');
screenPos   = [(cScreenSize(3) - 349)/2,(cScreenSize(4) - 119)/2, 349,119];
% ## plot title
oldgkit = graphics_toolkit;

if ~strcmp(oldgkit,'qt')
    graphics_toolkit('qt');
end

fh = dialog('name','Overwrite or not',"color", get(0, "defaultuicontrolbackgroundcolor"),'toolbar','none','menubar','none','windowstyle','modal','Position',screenPos);
 
h.attenion_label = uicontrol (fh,"style", "text",
                               "units", 'pixels',
                               "string", 'Atttention!',
                               "horizontalalignment", "center",
                               "position", [12 91 332 25],
                               'FontWeight','bold');

h.filename_label = uicontrol (fh,"style", "text",
                               "units", 'pixels',
                               "string", ['"',expNameStr, '.mat"'],
                               "ForegroundColor",[1, 0, 0],
                               "horizontalalignment", "center",
                               "position", [12 66 322 25]);

h.question_label = uicontrol (fh,"style", "text",
                               "units", 'pixels',
                               "string", 'alreadly existed, are you sure to overwrite it?',
                               "horizontalalignment", "center",
                               "position", [0 41 349 25]);



h.yes_pushbutton = uicontrol (fh,"style", "pushbutton",
                                "units", "pixels",
                                "string", "Yes",
                                'Tag','yes_button',
                                "callback", @yes_button_Callback,
                                "ButtonDownFcn", @yes_button_Callback,
                                "KeyPressFcn", @yes_button_keypress_Callback,
                                "position", [48 11 78 28]);

h.no_pushbutton = uicontrol (fh,"style", "pushbutton",
                                "units", "pixels",
                                "string", "No",
                                'Tag','no_button',
                                "callback", @no_button_Callback,
                                "ButtonDownFcn", @no_button_Callback,
                                "KeyPressFcn", @no_button_keypress_Callback,
                                "position", [212 11 78 28]);

guidata(fh, h);
uiwait(fh);

if ishghandle(fh)
    h = guidata(fh);
    delete(fh);
end

if nargout > 0
    varargout{1} = h.isOverwrite;
end

if ~strcmp(oldgkit,'qt')
    graphics_toolkit(oldgkit);
end

end 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% end of main function 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



% --- Executes on button press in yes_button.
function yes_button_Callback(obj)
% hObject    handle to yes_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    h = guidata (obj);
    h.isOverwrite = true;
    % Update handles structure
    guidata(obj, h);

    uiresume(get(gcbo, 'parent'));
end 

% ---Executes the current section when the "no_button" is pressed.
function no_button_Callback(obj)
% hObject    handle to no_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    h = guidata (obj);
    h.isOverwrite = false;
    % Update handles structure
    guidata(obj, h);

    uiresume(get(gcbo, 'parent'));

end

% --- Executes on button press in yes_button.
function yes_button_keypress_Callback(obj, eventdata)
% hObject    handle to yes_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
 if strcmpi(eventdata.Key,'return')
    h = guidata (obj);
    h.isOverwrite = true;
    % Update handles structure
    guidata(obj, h);

    uiresume(get(gcbo, 'parent'));
end
end

% ---Executes the current section when the "no_button" is pressed.
function no_button_keypress_Callback(obj, eventdata)
% hObject    handle to no_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
if strcmpi(eventdata.Key,'return')
    h = guidata (obj);
    h.isOverwrite = false;
    % Update handles structure
    guidata(obj, h);

    uiresume(get(gcbo, 'parent'));
end
end