import os
import platform
import re
import subprocess
import sys

from .modifiedData import *


class Info(object):
    """
    info类，主要存放一些配置信息及数据
    """
    ###########################################
    #           old info/data                 #
    ###########################################
    # last modified date
    LAST_MODIFY_DATE = CREATED_PSY_DATE

    DEFAULT_FONT = "Times"
    # GUI running platform: 0,1,2 for Windows, Darwin, and Linux respectively
    if platform.system() == "Windows":
        OS_TYPE: int = 0
    elif platform.system() == "Darwin":
        OS_TYPE: int = 1
    else:
        OS_TYPE: int = 2

    # is the system a retina screen under linux

    # is retina screen for linux
    IS_RETINA_SCR_LINUX: bool = False

    if OS_TYPE == 2:
        cmdOut = subprocess.run("xdpyinfo | grep dots", shell=True, capture_output=True).stdout
        s = re.findall(r' (\d+)x(\d+) dots per inch', cmdOut.decode(sys.stdout.encoding))

        for iScreen in s:
            for ixy in iScreen:
                if int(ixy) > 100:
                    IS_RETINA_SCR_LINUX = True
                    break
            if IS_RETINA_SCR_LINUX:
                break

    # target compile platform：linux\windows\mac
    PLATFORM: str = "linux"

    IMAGE_LOAD_MODE: str = "before_event"

    RUNNING_ENGINE: str = "matlab"

    # 保存widget_tabs的 (widget_id -> widget)
    WID_WIDGET = {}

    # 保存structure的 (widget_id -> node)
    WID_NODE: dict = {}

    # 只在structure中进行name的处理，避免失误(name -> [wid1, wid2...]),
    # 必须要保证wid1是所有指向的widget的widget_id！
    NAME_WID: dict = {}

    # 输入输出设备
    INPUT_DEVICE_INFO: dict = {}
    OUTPUT_DEVICE_INFO: dict = {}
    QUEST_DEVICE_INFO: dict = {}
    TRACKER_DEVICE_INFO: dict = {}

    # font and PTB preference
    FONT_DEFAULT_PREF = {}
    PTB_PREF = {}

    # 当前导入导出文件名
    FILE_NAME = ""
    FILE_DIRECTORY = ""

    # possible useful in the future
    REF_VALUE_SEPERATOR = "@"

    # widget type
    LOOP = "Loop"
    IMAGE = "Image"
    TEXT = "Text"
    SOUND = "Sound"
    VIDEO = "Video"
    COMBO = "Scene"
    BUG = "Bug"

    OPEN = "Open"
    DC = "DC"
    CALIBRATION = "Calibration"
    ACTION = "EyeAction"
    STARTR = "StartR"
    ENDR = "EndR"
    LOG = "Logging"
    QUEST_INIT = "QuestInit"
    QUEST_UPDATE = "QuestUpdate"
    QUEST_GET_VALUE = "QuestGetValue"
    IF = "If"
    SWITCH = "Switch"
    TIMELINE = "Timeline"

    DEV_NETWORK_PORT = "network port"
    DEV_SCREEN = "screen"
    DEV_PARALLEL_PORT = "parallel port"
    DEV_SERIAL_PORT = "serial port"
    DEV_SOUND = "sound"
    DEV_TRACKER = "tracker"
    DEV_QUEST = "quest"

    DEV_KEYBOARD = "keyboard"
    DEV_MOUSE = "mouse"
    DEV_RESPONSE_BOX = "response box"
    DEV_GAMEPAD = "gamepad"
    DEV_EYE_ACTION = "eye tracker"

    # FOR COMBO ITEMS:
    ITEM_POLYGON = "polygon"
    ITEM_ARC = "arc"
    ITEM_RECT = "rect"
    ITEM_CIRCLE = "circle"
    ITEM_IMAGE = "image"
    ITEM_TEXT = "text"
    ITEM_VIDEO = "video"
    ITEM_SOUND = "sound"
    ITEM_SNOW = "snow"
    ITEM_GABOR = "gabor"
    ITEM_LINE = "line"
    ITEM_DOT_MOTION = "dot motion"

    COMBO_COUNT: dict = {
        ITEM_POLYGON: 0,
        ITEM_ARC: 0,
        ITEM_RECT: 0,
        ITEM_CIRCLE: 0,
        ITEM_IMAGE: 0,
        ITEM_TEXT: 0,
        ITEM_VIDEO: 0,
        ITEM_SOUND: 0,
        ITEM_SNOW: 0,
        ITEM_GABOR: 0,
        ITEM_LINE: 0,
        ITEM_DOT_MOTION: 0,
    }

    # WAIT_DAILOG_CENTER = None
    # 图片保存路径
    # if getattr(sys, 'frozen', False): # we are running in a |PyInstaller| bundle
    #     BasePath = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname("psyBuilder.py")))
    # else: # we are running in a normal Python environment
    BasePath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # IMAGE_SOURCE_PATH = os.path.join(BasePath, "source", "image")
    # widget不同类型对应图片

    ###########################################
    #           new version info              #
    ###########################################
    # init file
    VarEnvFile = "var_env.ini"
    TempFile = "temp.ini"

    # image path
    # ImagePath = "source/images"
    ImagePath = os.path.join(BasePath, "source", "images")

    # widget type
    ERROR_WIDGET_ID = ""

    # drag type
    IconBarToTimeline = "0"
    CopyInTimeline = "1"
    MoveInTimeline = "2"
    AttributesToWidget = "3"
    StructureMoveToTimeline = "4"
    StructureCopyToTimeline = "5"
    StructureReferToTimeline = "6"

    # sender widget
    TimelineSend = 0
    CycleSend = 1
    StructureSend = 2
    ConditionSend = 3

    # name pattern
    WidgetPattern = [r"^[a-zA-Z][a-zA-Z0-9_]*$",
                     "Name must start with a letter and contain only letters, numbers, and _."]
    RepetitionsPattern = [r"^\+?[1-9][0-9]*$", "Only positive number is allowed."]

    PBBuiltinFunNames = ['cFolder', 'subInfo', 'subjectInfo', 'abortKeyCode', 'expStartTime', 'expEndTime',
                         'cRandSeed', 'HideCursor', 'ShowCursor', 'kbIndices', 'miceIndices', 'monitors',
                         'nextEvFlipReqTime', 'fullRects', 'beChkedRespDevs', 'winIFIs', 'DrawFormattedText',
                         'lastScrOnsettime', 'cShuffledIdx', 'opRowIdx', 'cDurs', 'subjectInfo', 'subjectInfo_oct',
                         'tracker2PtbTimeCoefs', 'resultVarNames', 'allBeFilledLoopAttVarNames', 'fieldNames',
                         'cSubStruct', 'flipComShiftDur', 'lastScrOnsetTime', 'iWin', 'TCPIPs','parPort', 'gamepadIndices',
                         'serPort', 'audioDevs', 'iCount', 'serialCons', 'tcpipCons','questStructs']

    PtbBuiltinFunNames = ['Beeper', 'CharAvail', 'Contents', 'Datapixx', 'DisableKeysForKbCheck',
                          'DrawFormattedText', 'DrawFormattedText2', 'Eyelink', 'FlushEvents', 'FontInfo',
                          'GetPID', 'GetSecs', 'HideCursor', 'IsWinVista', 'IsWin', 'IsLinux', 'IsOSX',
                          'KbCheck', 'KbName', 'ListenChar', 'LoadClut', 'LoadPsychHID',
                          'MachAbsoluteTimeClockFrequency', 'MachGetPriorityMex', 'PredictVisualOnsetForTime',
                          'PsychCV', 'PsychComputeSHA', 'PsychDrawSprites2D', 'PsychHID', 'PsychPortAudio',
                          'PsychTweak', 'PsychVulkanCore', 'PsychWatchDog', 'sca', 'RemapMouse',
                          'RestrictKeysForKbCheck', 'Screen', 'ScreenDrawDots', 'SetMouse', 'ShowCursor', 'Snd',
                          'VideoRefreshFromMeasurement', 'GetKeyboardIndices', 'GetGamepadIndices', 'GetMouseIndices',
                          'WaitSecs', 'WaitTicks', 'psychtoolbox', 'cleanup', 'el','ShowHideWinTaskbarMex']

    MatlabFunNames = ['if', 'eval', 'evalc', 'end', 'switch', 'struct', 'cell', 'datestr', 'save', 'rethrow',
                      'for', 'max', 'min', 'median', 'break', 'set', 'get', 'cd', 'clc', 'deal', 'zeros',
                      'close', 'error', 'continue', 'case', 'plot', 'otherwise', 'figure', 'catch',
                      'classdef', 'elseif', 'else', 'function', 'global', 'parfor', 'persistent',
                      'return', 'spmd', 'try', 'while', 'true', 'false', 'int', 'double', 'unique', 'commandwindow']

    ###########################################
    #           new version data              #
    ###########################################
    Psy = None
    # wid -> widget
    Widgets = WID_WIDGET
    # name -> list of wid
    Names = NAME_WID
    # wid -> node
    Nodes = WID_NODE

    # wid num of different add_type of widget
    WidgetTypeCount = {
        LOOP: 0,
        SOUND: 0,
        TEXT: 0,
        IMAGE: 0,
        VIDEO: 0,
        COMBO: 0,
        BUG: 0,
        OPEN: 0,
        DC: 0,
        CALIBRATION: 0,
        ACTION: 0,
        STARTR: 0,
        ENDR: 0,
        LOG: 0,
        QUEST_INIT: 0,
        QUEST_UPDATE: 0,
        QUEST_GET_VALUE: 0,
        IF: 0,
        SWITCH: 0,
        TIMELINE: 0,
    }

    # it's used to counter the count of widget name should go.
    WidgetNameCount = {
        LOOP: 0,
        SOUND: 0,
        TEXT: 0,
        IMAGE: 0,
        VIDEO: 0,
        COMBO: 0,
        BUG: 0,
        OPEN: 0,
        DC: 0,
        CALIBRATION: 0,
        ACTION: 0,
        STARTR: 0,
        ENDR: 0,
        LOG: 0,
        QUEST_INIT: 0,
        QUEST_UPDATE: 0,
        QUEST_GET_VALUE: 0,
        IF: 0,
        SWITCH: 0,
        TIMELINE: 0,
    }
