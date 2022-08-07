function varargout = overwriteOrNot(varargin)
% GUI for MATLAB to inqure about overwrite the exited result file or not
% Last Modified by Yang Zhang 08-Jun-2020 21:49:45

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @OverwriteOrNot_OpeningFcn, ...
                   'gui_OutputFcn',  @OverwriteOrNot_OutputFcn, ...
                   'gui_LayoutFcn',  @OverwriteOrNot_LayoutFcn, ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
   gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before OverwriteOrNot is made visible.
function OverwriteOrNot_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   unrecognized PropertyName/PropertyValue pairs from the
%            command line (see VARARGIN)

% Choose default command line output for OverwriteOrNot
handles.output = hObject;


if nargin >3
    inputFileName = varargin{1};
else
    error('OverwriteOrNot requires one input parameter!');
end 

set(handles.filename,'String',inputFileName);

handles.isOverwrite = 0;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes OverwriteOrNot wait for user response (see UIRESUME)
uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = OverwriteOrNot_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure

if isempty(handles)
    varargout{1} = 0;
else
    delete(handles.figure1);
    varargout{1} = handles.isOverwrite;
end



% --- Executes on button press in yes_button.
function yes_button_Callback(hObject, eventdata, handles)
% hObject    handle to yes_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.isOverwrite = 1;
% Update handles structure
guidata(hObject, handles);

uiresume;

% ---Executes the current section when the "no_button" is pressed.
function no_button_Callback(hObject, eventdata, handles)
% hObject    handle to no_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

handles.isOverwrite = 0;
% Update handles structure
guidata(hObject, handles);

uiresume;


% --- If Enable == 'on', executes on mouse press in 5 pixel border.
% --- Otherwise, executes on mouse press in 5 pixel border or over yes_button.
function yes_button_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to yes_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.isOverwrite = 1;
% Update handles structure
guidata(hObject, handles);

uiresume;


% --- If Enable == 'on', executes on mouse press in 5 pixel border.
% --- Otherwise, executes on mouse press in 5 pixel border or over no_button.
function no_button_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to no_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.isOverwrite = 0;
% Update handles structure
guidata(hObject, handles);

uiresume;


% --- Executes on key press with focus on yes_button and none of its controls.
function yes_button_KeyPressFcn(hObject, eventdata, handles)
% hObject    handle to yes_button (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.CONTROL.UICONTROL)
%	Key: name of the key that was pressed, in lower case
%	Character: character interpretation of the key(s) that was pressed
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) pressed
% handles    structure with handles and user data (see GUIDATA)
handles.isOverwrite = 1;
% Update handles structure
guidata(hObject, handles);

uiresume;


% --- Executes on key press with focus on no_button and none of its controls.
function no_button_KeyPressFcn(hObject, eventdata, handles)
% hObject    handle to no_button (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.CONTROL.UICONTROL)
%	Key: name of the key that was pressed, in lower case
%	Character: character interpretation of the key(s) that was pressed
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) pressed
% handles    structure with handles and user data (see GUIDATA)
handles.isOverwrite = 0;
% Update handles structure
guidata(hObject, handles);

uiresume;


% --- Executes during object creation, after setting all properties.
function attention_CreateFcn(hObject, eventdata, handles)
% hObject    handle to attention (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called


% --- Creates and returns a handle to the GUI figure. 
function h1 = OverwriteOrNot_LayoutFcn(policy)
% policy - create a new figure or use a singleton. 'new' or 'reuse'.

persistent hsingleton;
if strcmpi(policy, 'reuse') & ishandle(hsingleton)
    h1 = hsingleton;
    return;
end

appdata = [];
appdata.GUIDEOptions = struct(...
    'active_h', [], ...
    'taginfo', struct(...
    'figure', 2, ...
    'uipanel', 3, ...
    'text', 8, ...
    'pushbutton', 5), ...
    'override', 1, ...
    'release', 13, ...
    'resize', 'none', ...
    'accessibility', 'callback', ...
    'mfile', 1, ...
    'callbacks', 1, ...
    'singleton', 1, ...
    'syscolorfig', 1, ...
    'blocking', 0);
appdata.lastValidTag = 'figure1';
appdata.UsedByGUIData_m = [];
appdata.GUIDELayoutEditor = [];
appdata.initTags = struct(...
    'handle', [], ...
    'tag', 'figure1');

cScreenSize = get(0,'ScreenSize');

if exist('groot','builtin')
    dpiScale = get(groot,'ScreenPixelsPerInch')/96;
else
    dpiScale = 1; % for matlab older than 2014
end

fSize = [337,119]*dpiScale;

h1 = figure(...
'PaperUnits',get(0,'defaultfigurePaperUnits'),...
'Units',get(0,'defaultfigureUnits'),...
'Position',[(cScreenSize(3) - fSize(1))/2,(cScreenSize(4) - fSize(2))/2, fSize(1),fSize(2)],...
'Visible','on',...
'Color',get(0,'defaultfigureColor'),...
'IntegerHandle','off',...
'Colormap',[0 0 0.5625;0 0 0.625;0 0 0.6875;0 0 0.75;0 0 0.8125;0 0 0.875;0 0 0.9375;0 0 1;0 0.0625 1;0 0.125 1;0 0.1875 1;0 0.25 1;0 0.3125 1;0 0.375 1;0 0.4375 1;0 0.5 1;0 0.5625 1;0 0.625 1;0 0.6875 1;0 0.75 1;0 0.8125 1;0 0.875 1;0 0.9375 1;0 1 1;0.0625 1 1;0.125 1 0.9375;0.1875 1 0.875;0.25 1 0.8125;0.3125 1 0.75;0.375 1 0.6875;0.4375 1 0.625;0.5 1 0.5625;0.5625 1 0.5;0.625 1 0.4375;0.6875 1 0.375;0.75 1 0.3125;0.8125 1 0.25;0.875 1 0.1875;0.9375 1 0.125;1 1 0.0625;1 1 0;1 0.9375 0;1 0.875 0;1 0.8125 0;1 0.75 0;1 0.6875 0;1 0.625 0;1 0.5625 0;1 0.5 0;1 0.4375 0;1 0.375 0;1 0.3125 0;1 0.25 0;1 0.1875 0;1 0.125 0;1 0.0625 0;1 0 0;0.9375 0 0;0.875 0 0;0.8125 0 0;0.75 0 0;0.6875 0 0;0.625 0 0;0.5625 0 0],...
'MenuBar','none',...
'Name','Confirm File Overwrite',...
'NumberTitle','off',...
'HandleVisibility',get(0,'defaultfigureHandleVisibility'),...
'Tag','figure1',...
'UserData',[],...
'WindowStyle','modal',...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} );
% set(h1,'WindowStyle','modal');

appdata = [];
appdata.lastValidTag = 'attention';


fontSize = 12;

h2 = uipanel(...
'Parent',h1,...
'FontUnits',get(0,'defaultuipanelFontUnits'),...
'Units','normalized',...
'TitlePosition','centertop',...
'Title','Atttention!',...
'CreateFcn', {@local_CreateFcn, @(hObject,eventdata)overwriteOrNot('attention_CreateFcn',hObject,eventdata,guidata(hObject)), appdata} ,...
'Tag','attention',...
'Position',[-0.00265957446808511 -0.00615384615384615 1.00265957446809 1.00307692307692],...
'FontSize',fontSize,...
'FontName','Arial',...
'FontWeight','bold');

appdata = [];
appdata.lastValidTag = 'filename';

h3 = uicontrol(...
'Parent',h2,...
'Units','normalized',...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'String',{  'Static Text' },...
'Style','text',...
'Position',[6/fSize(1) 66/fSize(2) 322/fSize(1) 25/fSize(2)],...
'Children',[],...
'ForegroundColor',[1 0 0],...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} ,...
'Tag','filename',...
'FontSize',fontSize,...
'FontName','Arial');

appdata = [];
appdata.lastValidTag = 'text7';

h4 = uicontrol(...
'Parent',h2,...
'Units','normalized',...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'String','alreadly existed, are you sure to overwrite it?',...
'Style','text',...
'Position',[6/fSize(1) 41/fSize(2) 322/fSize(1) 25/fSize(2)],...
'Children',[],...
'ForegroundColor',get(0,'defaultuicontrolForegroundColor'),...
'ButtonDownFcn',blanks(0),...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} ,...
'DeleteFcn',blanks(0),...
'Tag','text7',...
'FontSize',fontSize,...
'FontName','Arial');

appdata = [];
appdata.lastValidTag = 'yes_button';

h5 = uicontrol(...
'Parent',h2,...
'Units','normalized',...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'String','Yes',...
'Style',get(0,'defaultuicontrolStyle'),...
'Position',[42/fSize(1) 11/fSize(2) 78/fSize(1) 28/fSize(2)],...
'Callback',@(hObject,eventdata)overwriteOrNot('yes_button_Callback',hObject,eventdata,guidata(hObject)),...
'Children',[],...
'ButtonDownFcn',@(hObject,eventdata)overwriteOrNot('yes_button_ButtonDownFcn',hObject,eventdata,guidata(hObject)),...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} ,...
'Tag','yes_button',...
'KeyPressFcn',@(hObject,eventdata)overwriteOrNot('yes_button_KeyPressFcn',hObject,eventdata,guidata(hObject)),...
'FontSize',fontSize,...
'FontName','Arial');

appdata = [];
appdata.lastValidTag = 'no_button';

h6 = uicontrol(...
'Parent',h2,...
'Units','normalized',...
'FontUnits',get(0,'defaultuicontrolFontUnits'),...
'String','No',...
'Style',get(0,'defaultuicontrolStyle'),...
'Position',[206/fSize(1) 11/fSize(2) 78/fSize(1) 28/fSize(2)],...
'Callback',@(hObject,eventdata)overwriteOrNot('no_button_Callback',hObject,eventdata,guidata(hObject)),...
'Children',[],...
'ButtonDownFcn',@(hObject,eventdata)overwriteOrNot('no_button_ButtonDownFcn',hObject,eventdata,guidata(hObject)),...
'CreateFcn', {@local_CreateFcn, blanks(0), appdata} ,...
'DeleteFcn',blanks(0),...
'Tag','no_button',...
'KeyPressFcn',@(hObject,eventdata)overwriteOrNot('no_button_KeyPressFcn',hObject,eventdata,guidata(hObject)),...
'FontSize',fontSize,...
'FontName','Arial');


hsingleton = h1;


% --- Set application data first then calling the CreateFcn. 
function local_CreateFcn(hObject, eventdata, createfcn, appdata)

if ~isempty(appdata)
   names = fieldnames(appdata);
   for i=1:length(names)
       name = char(names(i));
       setappdata(hObject, name, getfield(appdata,name));
   end
end

if ~isempty(createfcn)
   if isa(createfcn,'function_handle')
       createfcn(hObject, eventdata);
   else
       eval(createfcn);
   end
end


% --- Handles default GUIDE GUI creation and callback dispatch
function varargout = gui_mainfcn(gui_State, varargin)

gui_StateFields =  {'gui_Name'
    'gui_Singleton'
    'gui_OpeningFcn'
    'gui_OutputFcn'
    'gui_LayoutFcn'
    'gui_Callback'};
gui_Mfile = '';
for i=1:length(gui_StateFields)
    if ~isfield(gui_State, gui_StateFields{i})
        error(message('MATLAB:guide:StateFieldNotFound', gui_StateFields{ i }, gui_Mfile));
    elseif isequal(gui_StateFields{i}, 'gui_Name')
        gui_Mfile = [gui_State.(gui_StateFields{i}), '.m'];
    end
end

numargin = length(varargin);

if numargin == 0
    % OVERWRITEORNOT
    % create the GUI only if we are not in the process of loading it
    % already
    gui_Create = true;
elseif local_isInvokeActiveXCallback(gui_State, varargin{:})
    % OVERWRITEORNOT(ACTIVEX,...)
    vin{1} = gui_State.gui_Name;
    vin{2} = [get(varargin{1}.Peer, 'Tag'), '_', varargin{end}];
    vin{3} = varargin{1};
    vin{4} = varargin{end-1};
    vin{5} = guidata(varargin{1}.Peer);
    feval(vin{:});
    return;
elseif local_isInvokeHGCallback(gui_State, varargin{:})
    % OVERWRITEORNOT('CALLBACK',hObject,eventData,handles,...)
    gui_Create = false;
else
    % OVERWRITEORNOT(...)
    % create the GUI and hand varargin to the openingfcn
    gui_Create = true;
end

if ~gui_Create
    % In design time, we need to mark all components possibly created in
    % the coming callback evaluation as non-serializable. This way, they
    % will not be brought into GUIDE and not be saved in the figure file
    % when running/saving the GUI from GUIDE.
    designEval = false;
    if (numargin>1 && ishghandle(varargin{2}))
        fig = varargin{2};
        while ~isempty(fig) && ~ishghandle(fig,'figure')
            fig = get(fig,'parent');
        end
        
        designEval = isappdata(0,'CreatingGUIDEFigure') || (isscalar(fig)&&isprop(fig,'GUIDEFigure'));
    end
        
    if designEval
        beforeChildren = findall(fig);
    end
    
    % evaluate the callback now
    varargin{1} = gui_State.gui_Callback;
    if nargout
        [varargout{1:nargout}] = feval(varargin{:});
    else       
        feval(varargin{:});
    end
    
    % Set serializable of objects created in the above callback to off in
    % design time. Need to check whether figure handle is still valid in
    % case the figure is deleted during the callback dispatching.
    if designEval && ishghandle(fig)
        set(setdiff(findall(fig),beforeChildren), 'Serializable','off');
    end
else
    if gui_State.gui_Singleton
        gui_SingletonOpt = 'reuse';
    else
        gui_SingletonOpt = 'new';
    end

    % Check user passing 'visible' P/V pair first so that its value can be
    % used by oepnfig to prevent flickering
    gui_Visible = 'auto';
    gui_VisibleInput = '';
    for index=1:2:length(varargin)
        if length(varargin) == index || ~ischar(varargin{index})
            break;
        end

        % Recognize 'visible' P/V pair
        len1 = min(length('visible'),length(varargin{index}));
        len2 = min(length('off'),length(varargin{index+1}));
        if ischar(varargin{index+1}) && strncmpi(varargin{index},'visible',len1) && len2 > 1
            if strncmpi(varargin{index+1},'off',len2)
                gui_Visible = 'invisible';
                gui_VisibleInput = 'off';
            elseif strncmpi(varargin{index+1},'on',len2)
                gui_Visible = 'visible';
                gui_VisibleInput = 'on';
            end
        end
    end
    
    % Open fig file with stored settings.  Note: This executes all component
    % specific CreateFunctions with an empty HANDLES structure.

    
    % Do feval on layout code in m-file if it exists
    gui_Exported = ~isempty(gui_State.gui_LayoutFcn);
    % this application data is used to indicate the running mode of a GUIDE
    % GUI to distinguish it from the design mode of the GUI in GUIDE. it is
    % only used by actxproxy at this time.   
    setappdata(0,genvarname(['OpenGuiWhenRunning_', gui_State.gui_Name]),1);
    if gui_Exported
        gui_hFigure = feval(gui_State.gui_LayoutFcn, gui_SingletonOpt);

        % make figure invisible here so that the visibility of figure is
        % consistent in OpeningFcn in the exported GUI case
        if isempty(gui_VisibleInput)
            gui_VisibleInput = get(gui_hFigure,'Visible');
        end
        set(gui_hFigure,'Visible','off')

        % openfig (called by local_openfig below) does this for guis without
        % the LayoutFcn. Be sure to do it here so guis show up on screen.
        movegui(gui_hFigure,'onscreen');
    else
        gui_hFigure = local_openfig(gui_State.gui_Name, gui_SingletonOpt, gui_Visible);
        % If the figure has InGUIInitialization it was not completely created
        % on the last pass.  Delete this handle and try again.
        if isappdata(gui_hFigure, 'InGUIInitialization')
            delete(gui_hFigure);
            gui_hFigure = local_openfig(gui_State.gui_Name, gui_SingletonOpt, gui_Visible);
        end
    end
    if isappdata(0, genvarname(['OpenGuiWhenRunning_', gui_State.gui_Name]))
        rmappdata(0,genvarname(['OpenGuiWhenRunning_', gui_State.gui_Name]));
    end

    % Set flag to indicate starting GUI initialization
    setappdata(gui_hFigure,'InGUIInitialization',1);

    % Fetch GUIDE Application options
    gui_Options = getappdata(gui_hFigure,'GUIDEOptions');
    % Singleton setting in the GUI MATLAB code file takes priority if different
    gui_Options.singleton = gui_State.gui_Singleton;

    if ~isappdata(gui_hFigure,'GUIOnScreen')
        % Adjust background color
        if gui_Options.syscolorfig
            set(gui_hFigure,'Color', get(0,'DefaultUicontrolBackgroundColor'));
        end

        % Generate HANDLES structure and store with GUIDATA. If there is
        % user set GUI data already, keep that also.
        data = guidata(gui_hFigure);
        handles = guihandles(gui_hFigure);
        if ~isempty(handles)
            if isempty(data)
                data = handles;
            else
                names = fieldnames(handles);
                for k=1:length(names)
                    data.(char(names(k)))=handles.(char(names(k)));
                end
            end
        end
        guidata(gui_hFigure, data);
    end

    % Apply input P/V pairs other than 'visible'
    for index=1:2:length(varargin)
        if length(varargin) == index || ~ischar(varargin{index})
            break;
        end

        len1 = min(length('visible'),length(varargin{index}));
        if ~strncmpi(varargin{index},'visible',len1)
            try set(gui_hFigure, varargin{index}, varargin{index+1}), catch break, end
        end
    end

    % If handle visibility is set to 'callback', turn it on until finished
    % with OpeningFcn
    gui_HandleVisibility = get(gui_hFigure,'HandleVisibility');
    if strcmp(gui_HandleVisibility, 'callback')
        set(gui_hFigure,'HandleVisibility', 'on');
    end

    feval(gui_State.gui_OpeningFcn, gui_hFigure, [], guidata(gui_hFigure), varargin{:});

    if isscalar(gui_hFigure) && ishghandle(gui_hFigure)
        % Handle the default callbacks of predefined toolbar tools in this
        % GUI, if any
        guidemfile('restoreToolbarToolPredefinedCallback',gui_hFigure); 
        
        % Update handle visibility
        set(gui_hFigure,'HandleVisibility', gui_HandleVisibility);

        % Call openfig again to pick up the saved visibility or apply the
        % one passed in from the P/V pairs
        if ~gui_Exported
            gui_hFigure = local_openfig(gui_State.gui_Name, 'reuse',gui_Visible);
        elseif ~isempty(gui_VisibleInput)
            set(gui_hFigure,'Visible',gui_VisibleInput);
        end
        if strcmpi(get(gui_hFigure, 'Visible'), 'on')
            figure(gui_hFigure);
            
            if gui_Options.singleton
                setappdata(gui_hFigure,'GUIOnScreen', 1);
            end
        end

        % Done with GUI initialization
        if isappdata(gui_hFigure,'InGUIInitialization')
            rmappdata(gui_hFigure,'InGUIInitialization');
        end

        % If handle visibility is set to 'callback', turn it on until
        % finished with OutputFcn
        gui_HandleVisibility = get(gui_hFigure,'HandleVisibility');
        if strcmp(gui_HandleVisibility, 'callback')
            set(gui_hFigure,'HandleVisibility', 'on');
        end
        gui_Handles = guidata(gui_hFigure);
    else
        gui_Handles = [];
    end

    if nargout
        [varargout{1:nargout}] = feval(gui_State.gui_OutputFcn, gui_hFigure, [], gui_Handles);
    else
        feval(gui_State.gui_OutputFcn, gui_hFigure, [], gui_Handles);
    end

    if isscalar(gui_hFigure) && ishghandle(gui_hFigure)
        set(gui_hFigure,'HandleVisibility', gui_HandleVisibility);
    end
end

function gui_hFigure = local_openfig(name, singleton, visible)

% openfig with three arguments was new from R13. Try to call that first, if
% failed, try the old openfig.
if nargin('openfig') == 2
    % OPENFIG did not accept 3rd input argument until R13,
    % toggle default figure visible to prevent the figure
    % from showing up too soon.
    gui_OldDefaultVisible = get(0,'defaultFigureVisible');
    set(0,'defaultFigureVisible','off');
    gui_hFigure = matlab.hg.internal.openfigLegacy(name, singleton);
    set(0,'defaultFigureVisible',gui_OldDefaultVisible);
else
    % Call version of openfig that accepts 'auto' option"
    gui_hFigure = matlab.hg.internal.openfigLegacy(name, singleton, visible);  
%     %workaround for CreateFcn not called to create ActiveX
%         peers=findobj(findall(allchild(gui_hFigure)),'type','uicontrol','style','text');    
%         for i=1:length(peers)
%             if isappdata(peers(i),'Control')
%                 actxproxy(peers(i));
%             end            
%         end
end

function result = local_isInvokeActiveXCallback(gui_State, varargin)

try
    result = ispc && iscom(varargin{1}) ...
             && isequal(varargin{1},gcbo);
catch
    result = false;
end

function result = local_isInvokeHGCallback(gui_State, varargin)

try
    fhandle = functions(gui_State.gui_Callback);
    result = ~isempty(findstr(gui_State.gui_Name,fhandle.file)) || ...
             (ischar(varargin{1}) ...
             && isequal(ishghandle(varargin{2}), 1) ...
             && (~isempty(strfind(varargin{1},[get(varargin{2}, 'Tag'), '_'])) || ...
                ~isempty(strfind(varargin{1}, '_CreateFcn'))) );
catch
    result = false;
end


