import copy
import datetime
import os
import re
import shutil
import numpy as np
import scipy.io as sio
from PIL import Image as PillIma

from app.func import Func
from app.info import Info

cIndents = 0
printMaxCol = 150
isPreLineSwitch = 0
haveGaborStim = False
haveArcStim = 0
haveSnowStim = False
haveDotMotion = False
haveGammaTable = False
enabledKBKeysSet = set()
isDummyPrint = False
spFormatVarDict = dict()
inputDevNameIdxDict = dict()
outputDevNameIdxDict = dict()
historyPropDict = dict()
cInfoDict = dict()
allPossImaFilenameIdxDict = dict()
allPossImaWidNameIdxDict = dict()
queueDevIdxValueStr = str()
globalAttributesSetDict = dict()
stimWidgetTypesList = [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO, Info.IF, Info.SWITCH]

questVarNames = list()

closeImaMethodType = True

parameterTypeDict = {'Duration': 'dur',
                     'Clear After': 'clearAfter',
                     'Enable': 'enableFrame',
                     'Stretch Mode': 'stretchMode',
                     'Is Oval': 'boolean',
                     'Style': 'fontStyle',
                     'Right To Left': 'rightToLeft',
                     'Aspect Ratio': 'aspectRatio',
                     'Wait For Start': 'waitForStart',
                     'Border Color': 'color',
                     'Dot Color': 'color',
                     'Fill Color': 'color',
                     'Back Color': 'color',
                     'Frame Fill Color': 'color',
                     'Frame Transparent': 'percent',
                     'Transparent': 'percent',
                     'Width': 'percent',
                     'Height': 'percent',
                     'Center X': 'percent',
                     'Center Y': 'percent',
                     'Border Width': 'percent',
                     'Dot Num': 'percent',
                     'Dot Type': 'percent',
                     'Dot Size': 'percent',
                     'Move Direction': 'percent',
                     'Speed': 'percent',
                     'Coherence': 'percent',
                     'Spatial': 'percent',
                     'Contrast': 'percent',
                     'Phase': 'percent',
                     'Orientation': 'percent',
                     'SDx': 'percent',
                     'SDy': 'percent',
                     'Rotation': 'percent',
                     'Points': 'percent',
                     'Angle Start': 'percent',
                     'Angle Length': 'percent'
                     }


def throwCompileErrorInfo(inputStr):
    Func.printOut(inputStr, 3)
    raise Exception("compile failed: see info above for details.")


def debugPrint(inputStr: str):
    isDebug = False
    if isDebug:
        print(inputStr)


def pyStr2MatlabStr(inputStr):
    if isinstance(inputStr, str):
        if isSingleQuotedStr(inputStr):
            inputStr = inputStr[1:-1]

        # inputStr = re.sub("'", "''", inputStr)
        # replace the \n with \\n so that we could print it with \n to matlab
        inputStr = "\\n".join(inputStr.split("\n"))
        # inputStr = re.sub(r"\\\%","%",inputStr)
    return inputStr


def bitGet(number: int, pos: int = 0) -> int:
    return (number >> pos) & 1


# def dataStrConvert(dataStr, isRef=False, transMATStr=False, transPercent=True) -> str or float or int:
def dataStrConvert(dataStr, isRef=False, transMATStr=False, transPercent=True):
    # convert string to neither a string or a num
    # e.g.,
    # 1） "2"    to 2
    # 2） "2.00" to 2.0
    # 3） "string" to "'string'"
    # 4） "[12,12,12]" to "[12,12,12]"
    # 5） "12,12,12"  to "[12,12,12]"
    # 6） is a referred value will do nothing
    if isinstance(dataStr, str):
        if dataStr:
            if isPercentStr(dataStr):
                if transPercent:
                    outData = parsePercentStr(dataStr)
                else:
                    outData = addSingleQuotes(dataStr)

            elif isRgbWithBracketsStr(dataStr):
                outData = breakSquBrackets(dataStr)

            elif isRgbaWithBracketsStr(dataStr):
                outData = breakSquBrackets(dataStr)

            elif isRgbStr(dataStr):
                outData = addMinBrackets(dataStr)

            elif isRgbaStr(dataStr):
                outData = addMinBrackets(dataStr)

            elif isIntStr(dataStr):
                outData = int(dataStr)

            elif isFloatStr(dataStr):
                outData = float(dataStr)

            elif isRefStr(dataStr):
                outData = breakSquBrackets(dataStr)  # maybe a bug

            elif isVectWithBracketsStr(dataStr):
                outData = dataStr

            else:

                if isRef:
                    outData = breakSquBrackets(dataStr)  # maybe a bug
                else:
                    if transMATStr:

                        outData = addSingleQuotes(pyStr2MatlabStr(dataStr))  # maybe a bug
                    else:
                        outData = addSingleQuotes(dataStr)  # maybe a bug
        else:
            outData = "()"

    else:  # in case there is something wrong
        # raise Exception(f"the input dataStr:{dataStr} is not a string!")
        outData = breakSquBrackets(dataStr)

    return outData


def addedTransparentToRGBStr(RGBStr, transparentStr):
    transparentValue = parsePercentStr(transparentStr)

    if isinstance(transparentValue, (int, float)):
        if transparentValue == -1:  # for 100%
            return RGBStr
        else:
            transparentValue = transparentValue * -255
    else:
        if transparentValue != '()':
            transparentValue = f"{transparentValue}*-255"

    if transparentValue != '()':
        if isRgbStr(RGBStr):
            RGBStr = f"({RGBStr},{transparentValue})"
        elif isRgbWithBracketsStr(RGBStr):
            RGBStr = re.sub(']', f",{transparentValue}]", RGBStr)
        elif isRefStr(RGBStr):
            RGBStr = f"({RGBStr},{transparentStr})"
        else:
            raise Exception(
                f"the input parameter 'RGBStr' is not a RGB format String\n should be of R,G,B, [R,G,B], or referred values!")

    return RGBStr


# add curly brackets
def addCurlyBrackets(inputStr):
    # outputStr = "{"+str(inputStr)+"}"
    outputStr = f"{{{inputStr}}}"
    return outputStr


# add single quotes
def addSingleQuotes(inputStr: str) -> str:
    if inputStr.startswith("'") and inputStr.endswith("'"):
        if inputStr.startswith("''") and inputStr.endswith("''"):
            inputStr = f"'{inputStr}'"

    else:
        inputStr = f"'{inputStr}'"
    return inputStr


# add square brackets
def addSquBrackets(inputStr: str) -> str:
    inputStr = f"[{inputStr}]"
    return inputStr
def addMinBrackets(inputStr: str) -> str:
    inputStr = f"rgb({inputStr})"
    return inputStr
def breakSquBrackets(inputStr: str) -> str:
    inputStr=inputStr.replace("[","")
    inputStr=inputStr.replace("]","")
    if inputStr.find("var")!=-1:
        inputStr=str_html_var(inputStr)
    inputStr = f"${{{inputStr}}}"
    return inputStr

def removeSingleQuotes(inputStr: str) -> str:
    if isinstance(inputStr, str):
        if re.fullmatch("'.+'", inputStr):  # any character except a new line
            inputStr = inputStr[1:-1]
    return inputStr


def removeSquBrackets(inputStr: str) -> str:
    if isinstance(inputStr, str):
        if re.fullmatch(r"\[.+]", inputStr):  # any character except a new line
            inputStr = inputStr[1:-1]
    return inputStr


def isSubWidgetOfIfOrSwitch(widgetOrId) -> bool:
    isSubWidget = False
    if isinstance(widgetOrId, str):
        cWidgetId = widgetOrId
    else:
        cWidgetId = widgetOrId.widget_id

    parentWid = Func.getParentWid(cWidgetId)

    if parentWid:
        if getWidgetType(parentWid) in [Info.IF, Info.SWITCH]:
            isSubWidget = True

    return isSubWidget


def updateSpFormatVarDict(propertyValue, formatTypeStr, cSpecialFormatVarDict):
    if Func.isRef(propertyValue) == 2:
        allRefers = re.findall(r'(\[[A-Za-z]+[a-zA-Z._0-9]*?])', propertyValue)

        for cRefer in allRefers:
            updateSpFormatVarDict(cRefer, formatTypeStr, cSpecialFormatVarDict)

    elif isRefStr(propertyValue):
        propertyValue = propertyValue[1:-1]  # remove the square brackets
        allRefedCycleAttrs = getAllNestedVars(propertyValue, [])

        for cAttrName in allRefedCycleAttrs:

            if cAttrName in cSpecialFormatVarDict:
                if cSpecialFormatVarDict[cAttrName] != formatTypeStr:
                    throwCompileErrorInfo(
                        f"attribute: {cAttrName} are not allowed to be both {formatTypeStr} or {cSpecialFormatVarDict[cAttrName]}")
            else:
                cSpecialFormatVarDict.update({cAttrName: formatTypeStr})


def isContainChStr(inputStr):
    # :param check_str: {str}
    # :return: {bool} True and False for have and have not chinese characters respectively
    for ch in inputStr:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def isSoundRelatedWidget(cWidget) -> bool:
    haveSound = False
    cWidgetType = getWidgetType(cWidget)

    if Info.SOUND == cWidgetType:
        haveSound = True
    elif Info.COMBO == cWidgetType:
        itemIds = getSliderItemIds(cWidget)

        if isContainItemType(itemIds, Info.ITEM_SOUND):
            haveSound = True

    return haveSound


def isSingleQuotedStr(inputStr):
    if inputStr.startswith("'") and inputStr.endswith("'"):
        return True
    return False


def isRgbStr(inputStr):
    isRgbFormat = re.fullmatch(r'^\d+,\d+,\d+$', inputStr)
    return isRgbFormat


def isRgbaStr(inputStr):
    isRgbaFormat = re.fullmatch(r'^\d+,\d+,\d+,\d+$', inputStr)
    return isRgbaFormat


def isRectStr(inputStr):
    if len(inputStr) == 0:
        return None
    isRectFormat = re.fullmatch(r'^\d+,\d+,\d+,\d+$', inputStr)
    return isRectFormat


def isRgbaWithBracketsStr(inputStr):
    if len(inputStr) == 0:
        return None
    isRgbaFormat = re.fullmatch(r'^\[\d+,\d+,\d+,\d+]$', inputStr)
    return isRgbaFormat


def isRectWithBracketsStr(inputStr):
    if len(inputStr) == 0:
        return None
    isRectFormat = re.fullmatch(r'^\[\d+,\d+,\d+,\d+]$', inputStr)
    return isRectFormat


def isRgbWithBracketsStr(inputStr):
    if len(inputStr) == 0:
        return None
    isRgbFormat = re.fullmatch(r'^\[\d+,\d+,\d+]$', inputStr)
    return isRgbFormat
def isRgbWithMinBracketsStr(inputStr):
    if len(inputStr) == 0:
        return None
    isRgbFormat = re.fullmatch(r'^(\d+,\d+,\d+)$', inputStr)
    return isRgbFormat

def isVectWithBracketsStr(inputStr):
    if len(inputStr) == 0:
        return False

    if inputStr.startswith("[") and inputStr.endswith("]"):
        return re.sub(r"[,.]", "", inputStr[1:-1]).isdigit()
    else:
        return False


def isLegalMatlabStr(inputStr) -> bool:
    isLegal = True
    if inputStr.startswith("'") and inputStr.endswith("'"):
        inputStr = inputStr[1:-1]

    inputStr = re.sub("''", "", inputStr)

    if len(re.findall("'", inputStr)) > 0:
        isLegal = False

    return isLegal


def isNumStr(inputStr):
    if isinstance(inputStr, str):
        if len(inputStr) == 0:
            return False

        # return re.fullmatch(r"([\d]*\.?[\d$]+)|\d*", inputStr)
        return re.fullmatch(r"\d*\.?\d+|\d+\.?\d*", inputStr)

    return False


def isIntStr(inputStr):
    if isinstance(inputStr, str):
        if len(inputStr) == 0:
            return False

        return re.fullmatch(r"\d+", inputStr)

    return False


def isFloatStr(inputStr):
    if isinstance(inputStr, str):
        if len(inputStr) == 0:
            return False
        return re.fullmatch(r"\d*\.(\d+)$", inputStr)

    return False


def isPercentStr(inputStr):
    if isinstance(inputStr, str):
        if len(inputStr) == 0:
            return False
        # (^ \d * \.{1}\d+ % {1}$) | (^ \d+ % {1}$)
        return re.fullmatch(r"^\d*(\.\d+)?%$", inputStr)

    return False


def isRefStr(inputStr):
    isRef = False

    if isinstance(inputStr, str):
        # if isRgbWithBracketsStr(inputStr):
        #     return False
        if len(inputStr) == 0:
            return False

        # special chars lose their special meaning inside sets [], so . inside [] just means the char '.'
        if re.fullmatch(r'\[[A-Za-z]+[a-zA-Z._0-9]*]', inputStr):
            isRef = True

    return isRef

def mypathform(str):
    if str.find("var")!=-1:
        str="`${"+str_html_var(str)+"}`"
    strls=str.split("\\")
    str="/".join(strls)
    return str

def isContainCycleTL(widgetId) -> bool:
    """
    :param widgetId: widget id of the current timeline
    :return: True or False for contains Loop sub widget or not
    """
    cTimelineWidgetIds = getWidgetIDInTimeline(widgetId)

    for cWidgetId in cTimelineWidgetIds:
        if Func.isWidgetType(cWidgetId, Info.LOOP):
            return True
    return False


# def isContainCycleTL(widget_id) -> bool:
#     containCycleTL = False
#     cTimelineWidgetIds = getWidgetIDInTimeline(widget_id)
#
#     for cWidgetId in cTimelineWidgetIds:
#         if Func.isWidgetType(cWidgetId, Info.LOOP):
#             containCycleTL = True
#
#     return containCycleTL
def getCrossAngleLineXYsInArc(w, h, startAngle, arcAngle) -> str:
    parsedPoints = list()
    parsedPoints.append(getCrossPointInArc(w, h, startAngle))
    parsedPoints.append([0, 0])
    parsedPoints.append([0, 0])
    parsedPoints.append(getCrossPointInArc(w, h, startAngle - arcAngle))

    pointListStr = "".join(str(cXY[0]) + "," + str(cXY[1]) + ";" for cXY in parsedPoints)
    pointListStr = addSquBrackets(pointListStr[0:-1]) + "'"

    return pointListStr


def getCrossPointInArc(w, h, Angle) -> list:
    """
    :param w: the width of the arc
    :param h: the height of the arc
    :param Angle: the angle
    :return: the axis of the cross point
    """
    # % Angles are measured clockwise from vertical in PTB
    xy = []
    # in PTB draw arc, vertical is zero
    Angle = Angle
    Angle = Angle % 360
    arcAngle = np.pi * Angle / 180

    if Angle in [90, 270]:
        xy.append(0)
        xy.append(-0.5 * w * np.sign(np.sin(arcAngle)))
    else:
        cx = np.sqrt((0.5 * w * h) ** 2 / ((np.tan(arcAngle) * w) ** 2 + h ** 2)) * np.sign(np.cos(arcAngle))
        cy = -np.tan(arcAngle) * cx
        xy.append(round(cx * 100) / 100)
        xy.append(round(cy * 100) / 100)  # In PTB vertical up is negative in Y
    # x = sqrt((0.5 * w * h) ^ 2 / ((tanTheta * w) ^ 2 + h ^ 2)) * sign(cosd(angle_degree));
    return xy


def getSpOutDevTypeNum(devType: str) -> int:
    """
    :param devType:
    :return: the number of device in the current device type
    """
    cOutDevNum = 0

    output_devices = Info.OUTPUT_DEVICE_INFO

    for outDev_Id, cDevice in output_devices.items():

        if cDevice['Device Type'] == devType:
            cOutDevNum += 1

    return cOutDevNum


def getImaLoadMode() -> int:
    """
    :return: imageLoadMode: 1,2,3 for before event, trial, and exp respectively
    """
    if Info.IMAGE_LOAD_MODE == "before_exp":
        return 3
    elif Info.IMAGE_LOAD_MODE == "before_trial":
        return 2
    else:
        return 1


def getFlipType(cWidget) -> int:
    """
    :param cWidget: widget object
    :return: sliceFlipType: 0,1,2 for none, video related widget , and dot motion respectively
    """
    sliceFlipType = 0

    if Func.isWidgetType(cWidget.widget_id, Info.VIDEO):
        sliceFlipType += 1

    elif Func.isWidgetType(cWidget.widget_id, Info.COMBO):

        if isContainItemType(getSliderItemIds(cWidget), Info.ITEM_VIDEO):
            sliceFlipType += 1

        if isContainItemType(getSliderItemIds(cWidget), Info.ITEM_DOT_MOTION):
            sliceFlipType += 2

    return sliceFlipType


def isContainItemType(itemIds: list, itemType: str) -> bool:
    haveItemType = False

    for cItemId in itemIds:
        if getItemType(cItemId) == itemType:
            haveItemType = True
            break

    return haveItemType


def isFirstStimWidgetInTL(widget_id: str) -> bool:
    global stimWidgetTypesList

    if isSubWidgetOfIfOrSwitch(widget_id):
        return isFirstStimWidgetInTL(Func.getParentWid(widget_id))

    isFirstEvent = True

    preWidgetId = getPreWID(widget_id)

    while preWidgetId:
        if getWidgetIdType(preWidgetId) in stimWidgetTypesList:
            isFirstEvent = False
            break
        else:
            preWidgetId = getPreWID(widget_id)

    return isFirstEvent


def isLastStimWidgetInTL(widget_id: str) -> bool:
    global stimWidgetTypesList
    isLastEvent = True

    nextWidgetId = getNextWID(widget_id)
    while nextWidgetId:
        if getWidgetIdType(nextWidgetId) in stimWidgetTypesList:
            isLastEvent = False
            break
        else:
            nextWidgetId = getNextWID(nextWidgetId)

    return isLastEvent


def keyNameToCodes(keyNameList: list, isKeyCode: bool = False) -> list:
    """
    :type keyNameList: list of key names
    """
    keyCodesDict = {'any': '1:255', 'left_mouse': 1, 'right_mouse': 2, 'middle_mouse': 4, 'backspace': 8,
                    'tab': 9, 'clear': 12, 'return': 13, 'shift': 16, 'control': 17,
                    'alt': 18, 'pause': 19, 'capslock': 20, 'escape': 27, 'space': 32,
                    'pageup': 33, 'pagedown': 34, 'end': 35, 'home': 36, 'leftarrow': 37,
                    'uparrow': 38, 'rightarrow': 39, 'downarrow': 40, 'printscreen': 44,
                    'insert': 45, 'delete': 46, 'help': 47, '0)': 48, '1!': 49, '2@': 50,
                    '3#': 51, '4$': 52, '5%': 53, '6^': 54, '7&': 55, '8*': 56, '9(': 57, 'a': 65,
                    'b': 66, 'c': 67, 'd': 68, 'e': 69, 'f': 70, 'g': 71, 'h': 72, 'i': 73, 'j': 74,
                    'k': 75, 'l': 76, 'm': 77, 'n': 78, 'o': 79, 'p': 80, 'q': 81, 'r': 82, 's': 83,
                    't': 84, 'u': 85, 'v': 86, 'w': 87, 'x': 88, 'y': 89, 'z': 90, 'leftgui': 91,
                    'rightgui': 92, 'application': 93, '0': 96, '1': 97, '2': 98, '3': 99, '4': 100,
                    '5': 101, '6': 102, '7': 103, '8': 104, '9': 105, '*': 106, '+': 107, 'seperator': 108,
                    '-': 109, '.': 110, '/': 111, 'f1': 112, 'f2': 113, 'f3': 114, 'f4': 115, 'f5': 116, 'f6': 117,
                    'f7': 118, 'f8': 119, 'f9': 120, 'f10': 121, 'f11': 122, 'f12': 123, 'f13': 124, 'f14': 125,
                    'f15': 126,
                    'f16': 127, 'f17': 128, 'f18': 129, 'f19': 130, 'f20': 131, 'f21': 132, 'f22': 133, 'f23': 134,
                    'f24': 135, 'numlock': 144, 'scrolllock': 145, 'leftshift': 160, 'rightshift': 161,
                    'leftcontrol': 162, 'rightcontrol': 163, 'leftalt': 164, 'rightalt': 165, ';': 186,
                    '=+': 187, ',<': 188, '-_': 189, '.>': 190, '/?': 191, '`~': 192, '[{': 219, '\\\\': 220,
                    ']}': 221, "'": 222, 'attn': 246, 'crsel': 247, 'exsel': 248, 'play': 251, 'zoom': 252, 'pa1': 254}
    keyCodes = []

    for keyName in keyNameList:

        if isKeyCode:
            cKeyCode = keyCodesDict.get(keyName.lower(), None)
        else:
            if keyName.lower() == 'any':
                cKeyCode = '1:255'
            else:
                # [KbName('s'),KbName('s')] is much faster than KbName({'s','s'})
                cKeyCode = f"KbName('{keyName}')"

        if cKeyCode:
            keyCodes.append(cKeyCode)

    return keyCodes


def replaceDot(screenNameStr, newSplitStr="_") -> str:
    return newSplitStr.join(screenNameStr.split('.'))


def genAppropriatePathSplitter(filename: str, isForWin: bool = False) -> str:
    if isForWin:
        filename = re.sub(r'[\\/]', r'\\', filename)
    else:
        filename = re.sub(r'[\\/]', r'/', filename)

    return filename


def makeInputDevIndexValueStr(devType: str, indexStr: str, isOrderNum=True) -> [str, int]:
    if Info.DEV_KEYBOARD == devType:
        devIndexesVarName = "kbIndices"
        cDevType = 1
    elif Info.DEV_MOUSE == devType:
        devIndexesVarName = "miceIndices"
        cDevType = 2

    elif Info.DEV_GAMEPAD == devType:
        devIndexesVarName = "gamepadIndices"
        cDevType = 3

    elif Info.DEV_RESPONSE_BOX == devType:
        devIndexesVarName = "rbIndices"
        cDevType = 4
    elif Info.DEV_EYE_ACTION == devType:
        devIndexesVarName = "eyetrackerIndices"
        cDevType = 82
    else:
        cDevType = -1
        devIndexesVarName = "un_supportedInputDevs"

    if isOrderNum:
        inputDevIndexValue = f"{devIndexesVarName}({indexStr})"
    else:
        inputDevIndexValue = indexStr

    return inputDevIndexValue, cDevType


def shouldNotBeCitationCheck(keyStr, value):
    if isRefStr(value):
        throwCompileErrorInfo(f"'{keyStr}': the value should NOT be a citation!")


def shouldNotBeEmptyCheck(keyStr, value):
    if value == '':
        throwCompileErrorInfo(f"'{keyStr}' should NOT be empty!")


def copyYanglabFiles(beCopyFilenames: list):
    for cFile in beCopyFilenames:
        copyYanglabFile(cFile)
    return 0


def copyYanglabFile(filename: str):
    destinationDir = os.path.dirname(os.path.abspath(Info.FILE_NAME))

    if isinstance(filename, list):
        for cFile in filename:
            copyYanglabFile(cFile)
        return 0

    cPyFullFile = os.path.abspath(__file__)

    for iLevel in range(3):
        cPyFullFile, _ = os.path.split(cPyFullFile)

    sourceFile = os.path.join(cPyFullFile, 'yanglabMFuns', filename)
    destinationFile = os.path.join(destinationDir, filename)

    shutil.copyfile(sourceFile, destinationFile)

    return 0


def outPutTriggerCheck(cWidget) -> dict:
    """
    : force the pulse dur to be 10 ms if the ppl device will be used to send responses triggers
    """
    cOutPutDevices = cWidget.getOutputDevice()
    cInputDevices = cWidget.getInputDevice()

    respTriggerDevNames = set()
    for cInputDevInfo in cInputDevices.values():
        cRespTriggerDevName = cInputDevInfo['Output Device']

        shouldNotBeCitationCheck('Resp Trigger Device', cRespTriggerDevName)

        respTriggerDevNames.update([cRespTriggerDevName])

    shortPulseDurParallelsDict = dict()

    for cOpDevInfo in cOutPutDevices.values():
        if cOpDevInfo['Device Type'] == Info.DEV_PARALLEL_PORT:
            if cOpDevInfo['Device Name'] in respTriggerDevNames:
                shortPulseDurParallelsDict.update({cOpDevInfo['Device Id']: 10})
                Func.printOut('Currently we will force the pulse duration to be 10 ms', False)

    return shortPulseDurParallelsDict


def updateEnableKbKeysList(allowKeyStr):
    global enabledKBKeysSet

    if len(allowKeyStr) > 0:
        if allowKeyStr.startswith('[') and allowKeyStr.endswith(']'):
            enabledKBKeysSet.add(allowKeyStr[1:-1])
        else:
            enabledKBKeysSet.add(allowKeyStr)


def parseRectStr(inputStr: str, isRef=False) -> str:
    if isinstance(inputStr, str):
        if not isRef:
            if isRectStr(inputStr):
                inputStr = addSquBrackets(inputStr)
            elif isRectWithBracketsStr(inputStr):
                pass
            elif len(inputStr) == 0:
                inputStr = addSquBrackets(inputStr)
            else:
                throwCompileErrorInfo(
                    f"the value {inputStr} is not a rect format in PTB ('x0,y0,x1,y1' or '[x0,y0,x1,y1]')!")

    return inputStr

# def parseMfileEncodeFormatStr(inputStr: str) -> int:

def parseViusalDebugLevelStr(inputStr: str) -> int:
    debugLevel = -1

    if inputStr == "-1: Do nothing":
        debugLevel = -1
    elif inputStr == "0: Shut up":
        debugLevel = 0
    elif inputStr == "1: Only errors (black startup screen)":
        debugLevel = 1
    elif inputStr == "2: Also warnings":
        debugLevel = 2
    elif inputStr == "3: Disable startup msg":
        debugLevel = 3
    elif inputStr == "4: Also blue bootup screen":
        debugLevel = 4
    elif inputStr == "5: Also visual test sheets":
        debugLevel = 5

    return debugLevel


def parseVerbosityLevelStr(inputStr: str) -> int:
    verbosityLevel = 4
    if inputStr == "4: More useful info (default)":
        verbosityLevel = 4
    elif inputStr == "0: Shut up":
        verbosityLevel = 0
    elif inputStr == "1: Print errors":
        verbosityLevel = 1
    elif inputStr == "2: Also warnings":
        verbosityLevel = 2
    elif inputStr == "3: Also some info":
        verbosityLevel = 3
    elif inputStr == "5: Be very verbose":
        verbosityLevel = 5

    return verbosityLevel


def parseSyncTestLevelStr(inputStr: str) -> int:
    syncTestLevel = 0
    if inputStr == "0: Enable syncing test (default)":
        syncTestLevel = 0
    elif inputStr == "1: Shorten syncing test":
        syncTestLevel = 1
    elif inputStr == "2: Disable syncing test":
        syncTestLevel = 2

    return syncTestLevel


def parseQuestMethodsStr(inputStr: str):
    if isinstance(inputStr, str):
        if inputStr.lower() == 'quantile':
            inputStr = "1"
        elif inputStr.lower() == 'mean':
            inputStr = "2"
        elif inputStr.lower() == 'mode':
            inputStr = "3"
        else:
            throwCompileErrorInfo("quest method should be of {'quantile', 'mean', or 'mode'}!!")
    return inputStr


def parseBooleanStr(inputStr, isRef=False):
    if isinstance(inputStr, str):
        if not isRef:
            if inputStr.lower() in ["'yes'", "'true'", 'yes', 'true', '0', '1']:
                inputStr = "1"
            elif inputStr.lower() in ["'no'", "'false'", 'no', 'false', '0', '1']:
                inputStr = "0"
            else:
                throwCompileErrorInfo(
                    f"the value of '{inputStr}' should be of ['False','True','Yes','No','1', or '0'] ")
    elif isinstance(inputStr, bool):
        if inputStr:
            inputStr = "1"
        else:
            inputStr = "0"

    return inputStr


def parseDontClearAfterStr(inputStr):
    if isinstance(inputStr, str):
        inputStr = removeSingleQuotes(inputStr)

        if inputStr == "clear_0":
            inputStr = '0'
        elif inputStr == "notClear_1":
            inputStr = '1'
        elif inputStr == "doNothing_2":
            inputStr = '2'
    return inputStr


def parseDurationStr(inputStr):
    if isinstance(inputStr, str):
        inputStr = removeSingleQuotes(inputStr)

        if inputStr == "(Infinite)":
            inputStr = "999000"  # an extremely impossible value maximum of 1000 second
        elif re.fullmatch(r"\d+~\d+", inputStr):
            cDurRange = inputStr.split('~')
            inputStr = f"{cDurRange[0]},{cDurRange[1]}"

    return inputStr


def parseEndActionStr(endActionStr):
    if endActionStr == 'Terminate':
        endActionStr = '1'
    elif endActionStr == 'Terminate Till Release':
        endActionStr = '2'
    else:
        endActionStr = '0'

    return endActionStr


def trans2relativePath(fullFileName: str):
    if fullFileName:
        # for relative path just return
        if fullFileName[0].isalpha() and ":" not in fullFileName:
            return fullFileName

        beSavedDir = os.path.dirname(Info.FILE_NAME)

        # noinspection PyBroadException
        try:
            if os.path.dirname(fullFileName):
                commonPath = os.path.commonpath([fullFileName, beSavedDir])
                # re.sub(r'[\\/]', r'\\', filename)
                if len(commonPath) > 0 and re.sub(r'[\\/]', r'\\', commonPath) != re.sub(r'[\\/]', r'\\', beSavedDir):
                    raise Exception

                fullFileName = fullFileName[len(commonPath) + 1:]
        except:
            if not isRefStr(fullFileName):
                throwCompileErrorInfo(f"All experimental materials should be put under the same fold as the project: {beSavedDir}")

    return fullFileName


def formatPathSplitter(inputStr):
    inputStr = genAppropriatePathSplitter(inputStr, Info.PLATFORM == 'windows')

    return inputStr


def parsePhysicSize(inputStr: str) -> list:
    allValues = re.split(r'[,xX\s]\s*', inputStr)
    for value in allValues:


        if not isNumStr(value) and not value == 'auto':
            # if not value.isdigit() and not value == 'auto':
            throwCompileErrorInfo(f"{inputStr}: the physical size parameter should be a format of numberXnumber, a number, or 'auto'!\n"
                                  f"for using an eyetracker device, the screen physical size and viewing distance should be set (can not be empty).")
    return allValues


def parseStartEndTimeStr(inputStr, isRef=False) -> str:
    if not isRef:
        inputStr = inputStr

    return inputStr


def parseColorStr(inputStr, isRef=False) -> str:
    # color_map: dict = {
    #     "White": "255,255,255",
    #     "Gray": "128,128,128",
    #     "Black": "0,0,0",
    #     "Red": "255,0,0",
    #     "Orange": "255,165,0",
    #     "Yellow": "255,255,0",
    #     "Green": "0,255,0",
    #     "Blue": "0,0,255",
    #     "Purple": "128,0,128",
    #     "Transparent": "0,0,0,0"
    # }
    if not isRef:
        if inputStr.capitalize() == "White":
            inputStr = "255,255,255"
        if inputStr.capitalize() == "Gray":
            inputStr = "128,128,128"
        if inputStr.capitalize() == "Black":
            inputStr = "0,0,0"
        if inputStr.capitalize() == "Red":
            inputStr = "255,0,0"
        if inputStr.capitalize() == "Orange":
            inputStr = "255,165,0"
        if inputStr.capitalize() == "Green":
            inputStr = "0,255,0"
        if inputStr.capitalize() == "Blue":
            inputStr = "0,0,255"
        if inputStr.capitalize() == "Purple":
            inputStr = "128,0,128"
        if inputStr.capitalize() == "Yellow":
            inputStr = "255,255,0"
        if inputStr.capitalize() == "Transparent":
            inputStr = "0,0,0,0"

        if isRgbStr(inputStr):
            inputStr = addSquBrackets(inputStr)
        if isRgbaStr(inputStr):
            inputStr = addSquBrackets(inputStr)

        # inputStr = dataStrConvert(inputStr, isRef)

    return inputStr


def parseFontStyleStr(inputStr):
    if isinstance(inputStr, str):
        inputStr = removeSingleQuotes(inputStr)
        if inputStr == "normal_0":
            inputStr = '0'
        elif inputStr == "bold_1":
            inputStr = '1'
        elif inputStr == "italic_2":
            inputStr = '2'
        elif inputStr == "underline_4":
            inputStr = '4'
        elif inputStr == "outline_8":
            inputStr = '8'
        elif inputStr == "overline_16":
            inputStr = '16'
        elif inputStr == "condense_32":
            inputStr = '32'
        elif inputStr == "extend_64":
            inputStr = '64'

        if not isRefStr(inputStr) and not isIntStr(inputStr):
            throwCompileErrorInfo("font style should be of {'normal_0','bold_1','italic_2','underline_4','outline_8','overline_16','condense_32','extend_64'}"
                                  " <br> or an int string (1~128) denote the eight styles (or combination of them: e.g., 3 indicates bold and italic style) <br>")
    return inputStr


def parseRespKeyCodesStr(kbCorRespStr, isRefValue, devType) -> str:
    if isRefValue:
        kbCorRespCodesStr = kbCorRespStr
    else:
        if len(kbCorRespStr) > 0:

            haveRightBreaket = re.findall(r'{]}}', kbCorRespStr)

            if haveRightBreaket:
                kbCorRespStr = re.sub(r'{]}}', '', kbCorRespStr)

            splittedStrList = re.split(r'({.*?})', kbCorRespStr)
            splittedStrList = [tempItem for tempItem in splittedStrList if tempItem != ""]

            if haveRightBreaket:
                splittedStrList.append("{]}}")

            kbNameList = []
            for item in splittedStrList:
                if item.startswith('{') and item.endswith('}'):
                    item = item[1:-1]
                    kbNameList.append(item)
                else:
                    for char in item:
                        kbNameList.append(char)

            if devType == Info.DEV_KEYBOARD:
                kbCorRespCodes = keyNameToCodes(kbNameList)
            else:
                kbCorRespCodes = kbNameList

            if len(kbCorRespCodes) > 1:
                kbCorRespCodesStr = "".join(f"{value}, " for value in kbCorRespCodes[0:-1])
                kbCorRespCodesStr = "[" + kbCorRespCodesStr + f"{kbCorRespCodes[-1]}" + "]"
            else:
                kbCorRespCodesStr = f"{kbCorRespCodes[0]}"

        else:
            kbCorRespCodesStr = ""
            # kbCorRespCodesStr = "[0]"

    return kbCorRespCodesStr


def parsePercentStr(inputStr):
    if isinstance(inputStr, str):
        if isPercentStr(inputStr):
            if float(inputStr[:-1]) == 0:
                outputValue = float(inputStr[:-1])
            else:
                outputValue = float(inputStr[:-1]) / -100
        elif isIntStr(inputStr):
            outputValue = int(inputStr)
        elif isFloatStr(inputStr):
            outputValue = float(inputStr)
        else:
            outputValue = inputStr
    else:
        outputValue = inputStr

    return outputValue


def parseRTWindowStr(inputStr):
    if isinstance(inputStr, str):
        if inputStr == "(Same as duration)":
            inputStr = '-1'
        elif inputStr == "(End of timeline)":
            inputStr = '-2'
        # else:
        #
    return inputStr


def parseAspectRationStr(inputStr, isRef=False):
    # ""、Both、Horizontal、Vertical、[attr]
    if not isRef:
        if isinstance(inputStr, str):
            if inputStr == "Default":
                inputStr = "0"
            elif inputStr == "Ignore":
                inputStr = "1"
            elif inputStr == "keep":
                inputStr = "2"
            elif inputStr == "KeepByExpanding":
                inputStr = "3"
            else:
                inputStr = "0"

    return inputStr


def parseStretchModeStr(inputStr, isRef=False):
    # ""、Both、Horizontal、Vertical、[attr]
    if not isRef:
        if isinstance(inputStr, str):
            if inputStr == "Both":
                inputStr = "3"
            elif inputStr == "Horizontal":
                inputStr = "1"
            elif inputStr == "Vertical":
                inputStr = "2"
            else:
                inputStr = "0"

    return inputStr


def parseTextContentStrNew(inputStr) -> str:
    """
    new fun to support citation within current_text
    :param inputStr:
    :return:
    """
    if isContainChStr(inputStr):
        inputStr = "double(" + inputStr + ")"

    return inputStr


def parseTextContentStr(inputStr, isRef=False) -> str:
    if not isRef:
        # if isContainChStr(inputStr):
        #     # inputStr = "double(" + inputStr + ")"
        #     inputStr = "[" + "".join(f"{ord(value)} " for value in inputStr) + "]"
        # else:
        #   inputStr = pyStr2MatlabStr(inputStr)
        inputStr = addSingleQuotes(pyStr2MatlabStr(inputStr))
        # inputStr = addSingleQuotes(inputStr)

    return inputStr


def printOutList(f, inputList: list):
    for cRowStr in inputList:
        cRowStr = "{{".join(cRowStr.split('{'))
        cRowStr = "}}".join(cRowStr.split('}'))
        printAutoInd(f, cRowStr)

    return


# noinspection PyStringFormat
def printAutoInd(f, inputStr, *argins):
    global cIndents, isPreLineSwitch, isDummyPrint

    if isDummyPrint:
        # DO nothing
        return

    if isinstance(f, list):
        f.append(inputStr.format(*argins))
        return

    incrAfterStr = ('if', 'try', 'switch', 'for', 'while', 'properties', 'methods', 'classdef')
    decreAndIncrStr = ('else', 'elseif', 'otherwise', 'catch')

    keyWordStr = inputStr.split(' ')[0]

    if keyWordStr in incrAfterStr:
        tabStrs = '\t' * cIndents

        print(f"{tabStrs}{inputStr}".format(*argins), file=f)
        # print(f"\n{tabStrs}{inputStr}".format(*argins), file=f)

        cIndents += 1

    elif keyWordStr in decreAndIncrStr:
        cIndents -= 1
        tabStrs = '\t' * cIndents

        print(f"{tabStrs}{inputStr}".format(*argins), file=f)

        cIndents += 1

    elif 'end' == keyWordStr:
        cIndents -= 1
        tabStrs = '\t' * cIndents

        print(f"{tabStrs}{inputStr}".format(*argins), file=f)
        # print(f"{tabStrs}{inputStr}\n".format(*argins), file=f)

    elif 'end%switch' == keyWordStr:
        cIndents -= 2
        tabStrs = '\t' * cIndents

        print(f"{tabStrs}{inputStr}".format(*argins), file=f)
        # print(f"{tabStrs}{inputStr}\n".format(*argins), file=f)

    elif 'case' == keyWordStr:

        if 0 == isPreLineSwitch:
            cIndents -= 1

        tabStrs = '\t' * cIndents

        print(f"{tabStrs}{inputStr}".format(*argins), file=f)

        cIndents += 1

    else:

        tabStrs = '\t' * cIndents

        print(f"{tabStrs}{inputStr}".format(*argins), file=f)

    if 'switch' == keyWordStr:
        isPreLineSwitch = 1
    else:
        isPreLineSwitch = 0

    if cIndents < 0:
        cIndents = 0

    return


def haveTrackerType(trackerType: str = 'EyeLink') -> bool:
    eye_tracker_devices = Info.TRACKER_DEVICE_INFO

    exist_eye_tracker_type = False

    for cEyeTracker, cEyeTrackerProperty in eye_tracker_devices.items():
        if cEyeTrackerProperty.get('Select Tracker Type') == trackerType:
            exist_eye_tracker_type = True
            break

    return exist_eye_tracker_type


def getAllEventWidgetsList(includedType: int = 1) -> list:
    """
    :param includedType: 1 none LOOP, 2 LOOP, 3 all eventTypes
    :return: a list for event widget
    """
    allEventWidgets = []

    if includedType == 3:
        allEventWidgetTypes = [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO, Info.IF, Info.SWITCH,
                               Info.LOOP]
    elif includedType == 2:
        allEventWidgetTypes = [Info.LOOP]
    else:
        allEventWidgetTypes = [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO, Info.IF, Info.SWITCH]

    for cWidgetId, cWidget in Info.WID_WIDGET.items():
        if not isSubWidgetOfIfOrSwitch(cWidgetId) and getWidgetType(cWidgetId) in allEventWidgetTypes:
            allEventWidgets.append(cWidget)
    return allEventWidgets


def getAllEventWidgetNamesList(includedType: int = 1) -> list:
    """
    :param includedType: 1 not include LOOP,2 LOOP only, 3 include LOOP
    :return: a list for event widget names
    """
    cAllEventWidgetNameList = []

    if includedType == 3:
        allEventWidgetTypes = [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO, Info.IF, Info.SWITCH,
                               Info.LOOP]
    elif includedType == 2:
        allEventWidgetTypes = [Info.LOOP]
    else:
        allEventWidgetTypes = [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO, Info.IF, Info.SWITCH]

    for cWidgetId, cWidget in Info.WID_NODE.items():

        if not isSubWidgetOfIfOrSwitch(cWidgetId) and getWidgetType(cWidgetId) in allEventWidgetTypes:
            cAllEventWidgetNameList.append(getWidgetName(cWidgetId))

    return cAllEventWidgetNameList


def haveOutputDevs(cWidget) -> bool:
    haveOPDev = False
    cWidgetType = getWidgetType(cWidget)

    if cWidgetType in stimWidgetTypesList:
        if cWidgetType == Info.SWITCH:
            for cCaseDict in cWidget.getCases():
                # {'Case Value': '',
                #  'Id Pool': {'Image': 'Image.0', 'Video': '', 'Text': '', 'Sound': '', 'Slider': ''},
                #  'Sub Wid': 'Image.0', 'Stim Type': 'Image', 'Event Name': 'U_Image_6574'}
                if cCaseDict['Sub Wid']:
                    if Info.WID_WIDGET.get(cCaseDict['Sub Wid']).getOutputDevice():
                        haveOPDev = True
                        break

        elif cWidgetType == Info.IF:
            cTrueWidget = cWidget.getTrueWidget()
            cFalseWidget = cWidget.getFalseWidget()

            nTrueOutputDev = 0
            nFalseOutputDev = 0

            if cTrueWidget is not None:
                nTrueOutputDev = len(cTrueWidget.getOutputDevice())
            if cFalseWidget is not None:
                nFalseOutputDev = len(cFalseWidget.getOutputDevice())

            haveOPDev = (nTrueOutputDev + nFalseOutputDev) > 0
        else:
            haveOPDev = len(cWidget.getOutputDevice()) > 0

    return haveOPDev


def saveIma2mat(imName: str, pillImaData):

    imNameOnly = imName.split('.')[0]

    if imNameOnly:
        imFullfile = os.path.abspath(os.path.join(Info.FILE_DIRECTORY, imNameOnly + '.mat'))
        # cFolder, _ = os.path.split(imFullfile)
        # os.makedirs(cFolder, exist_ok=True)
        sio.savemat(imFullfile, {'data': np.asarray(pillImaData)})
    else:
        return -1
    return 0


def getAllImSizeInMb(imNameList: list):
    """
    :param imNameList:
    :return:  all image size in kb
    """
    allSize = 0

    for cIm in imNameList:
        im = PillIma.open(os.path.join(Info.FILE_DIRECTORY, cIm))
        allSize += im.height*im.width*len(im.getbands())
        saveIma2mat(cIm, im)

    return allSize/1024/1024


def getWidLevel(cWid: str) -> int:
    if isSubWidgetOfIfOrSwitch(cWid):
        cWid = Func.getParentWid(cWid)

    return Func.getWidLevel(cWid)


def getWidgetName(widgetOrId, isNameInTL=True) -> str:
    """
    :param widgetOrId: widget or widget_id
    :param isNameInTL: Is it looking for parent name if the current widget is a sub widget of IF or SWITCH?
    :return:
    """
    if isinstance(widgetOrId, str):
        cWid = widgetOrId
    else:
        cWid = widgetOrId.widget_id

    if isNameInTL and isSubWidgetOfIfOrSwitch(cWid):
        cWid = Func.getParentWid(cWid)

    return Func.getWidgetName(cWid)


def getWidgetPos(widgetOrId) -> None or int:
    if isinstance(widgetOrId, str):
        cWidgetId = widgetOrId
    else:
        cWidgetId = widgetOrId.widget_id

    if isSubWidgetOfIfOrSwitch(cWidgetId):
        cWidgetId = Func.getParentWid(cWidgetId)

    return Func.getWidgetPosition(cWidgetId)


# noinspection PyBroadException
def getWidgetEventPos(widget_id: str):
    # def getWidgetEventPos(widget_id: str) -> int or None:
    allEventWidgetTypes = [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO, Info.IF, Info.SWITCH]
    # 如果是widget是timeline，不存在位置信息
    if widget_id.startswith(Info.TIMELINE):
        return None
    #
    try:
        node = Info.WID_NODE[widget_id]
        parent_node = node.parent()

        # for subWidgets under IF or SWITCH, try to extract pos based on IF or SWITCH widget
        if isSubWidgetOfIfOrSwitch(widget_id):
            widget_id = parent_node.widget_id
            parent_node = parent_node.parent()

        allIdList = []
        for iWidget in range(parent_node.childCount()):
            if getWidgetType(parent_node.child(iWidget)) in allEventWidgetTypes:
                allIdList.append(parent_node.child(iWidget).widget_id)

        try:
            return allIdList.index(widget_id)
        except:
            return None
    except:
        print(f"error: widget not founded.")
        return None


def getNextStimWID(widget_id: str) -> None or str:
    nextStimWID = getNextWID(widget_id)

    while nextStimWID and getNextWID(widget_id) not in stimWidgetTypesList:
        nextStimWID = getNextWID(widget_id)

    return nextStimWID


def getNextWID(widget_id: str) -> None or str:
    if isSubWidgetOfIfOrSwitch(widget_id):
        return Func.getNextWidgetId(Func.getParentWid(widget_id))
    else:
        return Func.getNextWidgetId(widget_id)


def getPreStimWID(widget_id: str) -> None or str:
    preWID = getPreWID(widget_id)

    while preWID and getWidgetType(preWID) not in stimWidgetTypesList:
        preWID = getPreWID(preWID)

    return preWID


def getPreWID(widget_id: str) -> None or str:
    if isSubWidgetOfIfOrSwitch(widget_id):
        return Func.getPreviousWidgetId(Func.getParentWid(widget_id))
    else:
        return Func.getPreviousWidgetId(widget_id)


def getMaxLenInStrList(strList: list) -> int:
    """
    :param strList: list composed of strings
    :return:
    """
    maxLen = 0
    for cStr in strList:
        maxLen = max(maxLen, len(cStr))

    return maxLen


def getAllRefValueSetDict():
    global globalAttributesSetDict
    refValueSetDict = globalAttributesSetDict.copy()
    getTLRefValueSet(Info.WID_WIDGET[f"{Info.TIMELINE}.0"], refValueSetDict)

    return refValueSetDict


def getCycleRefValueSet(cWidget, refValueSetDict):
    cLoopLevel = 0

    cWidgetName = getWidgetName(cWidget.widget_id)

    for iRow in range(cWidget.rowCount()):
        cRowDict = cWidget.getAttributes(iRow)
        for key, value in cRowDict.items():
            # get the referenced var value
            cValue, isRefValue, cRefValueSet = getRefValueSet(cWidget, value, refValueSetDict)

            cAttributeName = f"{cWidgetName}.var.{key}"

            if not isRefValue:
                cRefValueSet = {cValue}

            if cAttributeName in refValueSetDict:
                preValueSet = refValueSetDict[cAttributeName][2]
            else:
                preValueSet = set()

            refValueSetDict.update({cAttributeName: [cLoopLevel, "", cRefValueSet.union(preValueSet)]})

    # handle each timeline
    cTimeLineList = cWidget.getTimelines()
    # squeeze the timelines
    cTimelineIdSet = set()

    for iTimeline in cTimeLineList:
        cTimelineIdSet.add(iTimeline[1])

    for iTimeline_id in cTimelineIdSet:
        if iTimeline_id:
            getTLRefValueSet(Info.WID_WIDGET[iTimeline_id], refValueSetDict)

    return 0


def getWidNameIndexStr(widNamesList) -> str:
    """
    :param widNamesList: widNamesList corresponding to imas
    :return: outStr: e.g., '[1,2,3]'
    """
    global allPossImaWidNameIdxDict

    if isinstance(widNamesList, str):
        widNamesList = [widNamesList]

    outStr = ''.join(f"{allPossImaWidNameIdxDict[key]}," for key in widNamesList)

    if len(widNamesList) > 1:
        outStr = addSquBrackets(outStr[:-1])
    else:
        outStr = outStr[:-1]

    return outStr


def parseImaFileStr(inputStr: str):
    if inputStr.startswith("'") and inputStr.endswith("'"):
        inputStr = inputStr[1:-1]
    return inputStr


def getImaIndexStr(imaNamesList) -> str:
    """
    :param imaNamesList: imaNameList
    :return: outStr: e.g., '[1,2,3]'
    """
    global allPossImaFilenameIdxDict

    if isinstance(imaNamesList, str):
        imaNamesList = [imaNamesList]

    outStr = ''.join(f"{allPossImaFilenameIdxDict[parseImaFileStr(key)]}," for key in imaNamesList)

    if len(imaNamesList) > 1:
        outStr = addSquBrackets(outStr[:-1])
    else:
        outStr = outStr[:-1]

    return outStr


def getTLRefValueSet(cWidget, refValueSetDict):

    cTimelineWidgetIds = getWidgetIDInTimeline(cWidget.widget_id)

    for cWidgetId in cTimelineWidgetIds:
        cWidget = Info.WID_WIDGET[cWidgetId]

        if Info.LOOP == getWidgetType(cWidget):
            getCycleRefValueSet(cWidget, refValueSetDict)

    return 0


def getAllNestedVars(inputStr, opVars=None) -> set:
    if opVars is None:
        opVars = []

    if isRefStr(inputStr):
        inputStr = inputStr[1:-1]

    if len(inputStr.split('.')) == 3:
        opVars.append(inputStr)
        cCycleName, _, attName = inputStr.split('.')

        if cCycleName in Info.NAME_WID:
            cWidget = Info.WID_WIDGET[Info.NAME_WID[cCycleName][0]]
        else:
            throwCompileErrorInfo(f"wrong citation: [{inputStr}], perhaps you changed the Loop name but did not update the corresponding citation!")

        for iRow in range(cWidget.rowCount()):
            cRowDict = cWidget.getAttributes(iRow)
            if attName in cRowDict:
                getAllNestedVars(cRowDict[attName], opVars)
            else:
                throwCompileErrorInfo(f"wrong variable name: [{attName}], perhaps you changed the variable name in the Loop table but did not update the corresponding citation!")

    return set(opVars)


def getCycleRealRows(widgetId: str) -> int:
    cCycle = Info.WID_WIDGET[widgetId]

    repetitionsList = cCycle.getAttributeValues(0)

    sumValue = 0
    for cWeightStr in repetitionsList:
        sumValue = sumValue + dataStrConvert(cWeightStr)

    return sumValue


def getCycleAttVarNamesList(cWidget) -> list:
    cRowDict = cWidget.getAttributes(0)
    #
    allAttVarNameList = [f"{getWidgetName(cWidget.widget_id)}_{cVar}" for cVar in cRowDict.keys()]

    return allAttVarNameList


def getWidgetLeftJustLen(widgetsList: list) -> int:
    # get length for left just
    cLJustLen = 0
    for cWidget in widgetsList:
        cLJustLen = max(len(getWidgetName(cWidget.widget_id)), cLJustLen)
    return cLJustLen


def getAllCycleAttVarNameList(containsSubCycleOnly: bool = False) -> list:
    allAttrVarNameList = []

    allEventWidgets = getAllEventWidgetsList(2)  # 2 for cycle widget only

    for cWidget in allEventWidgets:
        if containsSubCycleOnly:
            if isCycleContainsSubCycle(cWidget):
                cCycleAttVarNameList = getCycleAttVarNamesList(cWidget)
                allAttrVarNameList.extend(cCycleAttVarNameList)
        else:
            cCycleAttVarNameList = getCycleAttVarNamesList(cWidget)
            allAttrVarNameList.extend(cCycleAttVarNameList)

    return allAttrVarNameList


# def getDevPropertyValue(devList: dict, devName: str, searchedKey: str) -> str or float or int or None:
def getDevPropertyValue(devList: dict, devName: str, searchedKey: str):
    keyValue = None
    for cDevId, cDevPro in devList.items():
        if devName == cDevPro['Device Name']:
            keyValue = cDevPro[searchedKey]
            break

    return keyValue


def getMaxLoopLevel() -> int:
    maxLoopLevel = -1

    for cWidgetId in Info.WID_NODE.keys():
        maxLoopLevel = max(maxLoopLevel, getWidLoopLevel(cWidgetId))
    return maxLoopLevel


def getFilenamePossWidgetsDict(fileType: int = 1) -> dict:
    """
    :param fileType:  1,2,4 for image, sound, and video file respectively
    :return: allFilenameWidgetNameDict {filename: [widgetNameList]}
    """
    widgetFileInfo = getAllWidgetFileInfo(fileType)
    allPossFilenames, _ = getAllPossFilenames(fileType, widgetFileInfo)

    allFilenameWidgetNameDict = dict()

    for cFilename in allPossFilenames:
        cFileWidgetNames = set()
        for widgetName, possFilenames in widgetFileInfo.items():
            if cFilename in possFilenames:
                cFileWidgetNames.add(widgetName)

        allFilenameWidgetNameDict.update({cFilename: list(cFileWidgetNames)})

    return allFilenameWidgetNameDict


def getAllPossFilenames(fileType: int = 1, widgetFileInfo: dict = None):
    """
    :param fileType: 1,2,4 for image, sound, and video file respectively
    :param widgetFileInfo: dict of {widgetName or widgetName_itemName : filenames}
    :return: allPossFilenames: list of all possible filenames (unique)
    :return: allPossWidgetNames: list of all possible ima related widgetNames (unique)
    """
    allPossFilenames = set()
    allPossWidgetNames = set()

    if widgetFileInfo is None:
        widgetFileInfo = getAllWidgetFileInfo(fileType)

    for key, value in widgetFileInfo.items():
        allPossFilenames.update(value)
        allPossWidgetNames.update([key])

    return list(allPossFilenames), list(allPossWidgetNames)


def getWidgetFileInfo(cWidget, fileType: int = 1, refValueSetDict=None) -> dict:
    """
    :param cWidget:
    :param fileType: 1,2,4 for image, sound, and video file respectively
    :param refValueSetDict:
    :return: widgetNameFilenameDict: {widgetName or widgetName_itemName : filenames}
    """
    widgetNameFilenameDict = dict()

    if not cWidget:
        return widgetNameFilenameDict

    if refValueSetDict is None or len(refValueSetDict) == 0:
        refValueSetDict = getAllRefValueSetDict()

    allWidgetTypes = list()

    cWidgetId = cWidget.widget_id

    # if len(refValueSetDict) == 0:
    #     refValueSetDict = getAllRefValueSetDict()

    if bitGet(fileType, 0):
        allWidgetTypes.append(Info.IMAGE)
    if bitGet(fileType, 1):
        allWidgetTypes.append(Info.SOUND)
    if bitGet(fileType, 2):
        allWidgetTypes.append(Info.VIDEO)

    # for specifically stim widget types
    if getWidgetType(cWidgetId) in allWidgetTypes:
        cFilename = cWidget.getFilename()
        if cFilename:
            widgetNameFilenameDict.update({getWidgetName(cWidget.widget_id): getWidgetPossFilenames(cWidget, cFilename, refValueSetDict)})

    # for COMBO
    if getWidgetType(cWidgetId) == Info.COMBO:
        fileInfo = cWidget.getFilename(fileType)

        for cItemName, cFilename in fileInfo.items():
            if cFilename:
                widgetNameFilenameDict.update({f"{getWidgetName(cWidgetId)}_{cItemName}": getWidgetPossFilenames(cWidget, cFilename, refValueSetDict)})

    return widgetNameFilenameDict


def getcTLPossfilenames(cTLWidget, fileType: int = 1) -> set:
    widgetNameFilenameDict: dict = dict()
    cTLPossFilenames = set()

    if getWidgetType(cTLWidget) == Info.TIMELINE:
        cTimelineWidgetIds = getWidgetIDInTimeline(cTLWidget.widget_id)

        refValueSetDict = getAllRefValueSetDict()

        for cWidgetId in cTimelineWidgetIds:
            cWidget = Info.WID_WIDGET[cWidgetId]
            widgetNameFilenameDict.update(getWidgetFileInfo(cWidget, fileType, refValueSetDict))
    else:
        throwCompileErrorInfo(
            f"the current widget type '{cTLWidget.widget_id}' is not a timeline \n")

    for cFilenames in widgetNameFilenameDict.values():
        cTLPossFilenames.update(cFilenames)

    return cTLPossFilenames


def getAllWidgetFileInfo(fileType: int = 1) -> dict:
    """
    :param fileType: 1,2,4 for image, sound, and video file respectively
    :return: widgetNameFilenameDict: dict {widgetName or widgetName_itemName : filenames}
    """
    refValueSetDict = getAllRefValueSetDict()

    widgetNameFilenameDict = dict()

    for cWidgetId, cWidget in Info.WID_WIDGET.items():
        # for if or switch
        if getWidgetType(cWidgetId) == Info.IF:
            falseWidget = cWidget.getFalseWidget()
            trueWidget = cWidget.getTrueWidget()

            widgetNameFilenameDict.update(getWidgetFileInfo(falseWidget, fileType, refValueSetDict))
            widgetNameFilenameDict.update(getWidgetFileInfo(trueWidget, fileType, refValueSetDict))

        elif getWidgetType(cWidgetId) == Info.SWITCH:
            caseWidgetsInfo = cWidget.getCases()

            for cCase in caseWidgetsInfo:
                cSubWid = cCase['Sub Wid']

                if cSubWid:
                    widgetNameFilenameDict.update(getWidgetFileInfo(Info.WID_WIDGET[cSubWid], fileType, refValueSetDict))

        else:
            widgetNameFilenameDict.update(getWidgetFileInfo(cWidget, fileType, refValueSetDict))

    return widgetNameFilenameDict


def getWidgetPossTextItems(cWidget, inputStr: str, refValueSetDict: dict = None) -> set:
    """
    :param cWidget: a widget
    :param inputStr: to be parsed text content
    :param refValueSetDict:
    :return: outValuesSet: set of all possible filenames
    """
    refPat = r'(\[[A-Za-z]+[a-zA-Z._0-9]*?\])'
    tmpOutValueSet = set()
    outValuesSet = set()

    if refValueSetDict is None or len(refValueSetDict) == 0:
        refValueSetDict = getAllRefValueSetDict()
        # 'sessionNum': [0, 'subInfo.session', {'subInfo.session'}]

    allRefs = re.findall(refPat, inputStr)

    if len(allRefs) > 0:
        cRefs = re.sub(r"[\[\]]", '', allRefs[0])
        if cRefs in refValueSetDict:
            possibleValuesSet = refValueSetDict[cRefs][2]

            for cValue in possibleValuesSet:
                cOUtValueStr = re.sub(r"\["+cRefs+"]", cValue, inputStr)
                if Func.isRef(cOUtValueStr):
                    tmpOutValueSet.add(cOUtValueStr)
                else:
                    outValuesSet.add(genAppropriatePathSplitter(cOUtValueStr, Info.PLATFORM == 'windows'))
        else:
            throwCompileErrorInfo(
                f"The cited attribute '{cRefs}' is not available for {getWidgetName(cWidget.widget_id)}")
    else:
        if inputStr:
            outValuesSet.add(inputStr)

    if len(tmpOutValueSet) > 0:
        for cStr in tmpOutValueSet:
            outValuesSet.update(getWidgetPossTextItems(cWidget, cStr, refValueSetDict))

    return outValuesSet


def getWidgetPossFilenames(cWidget, inputStr: str, refValueSetDict: dict = None) -> set:
    """
    :param cWidget: a widget
    :param inputStr: to be parsed string
    :param refValueSetDict:
    :return: outValuesSet: set of all possible filenames
    """
    refPat = r'(\[[A-Za-z]+[a-zA-Z._0-9]*?\])'
    tmpOutValueSet = set()
    outValuesSet = set()

    if refValueSetDict is None or len(refValueSetDict) == 0:
        refValueSetDict = getAllRefValueSetDict()

    allRefs = re.findall(refPat, inputStr)

    if len(allRefs) > 0:
        cRefs = re.sub(r"[\[\]]", '', allRefs[0])
        if cRefs in refValueSetDict:
            possibleValuesSet = refValueSetDict[cRefs][2]

            for cValue in possibleValuesSet:
                cOUtValueStr = re.sub(r"\["+cRefs+"]", cValue, inputStr)
                if Func.isRef(cOUtValueStr):
                    tmpOutValueSet.add(cOUtValueStr)
                else:
                    outValuesSet.add(genAppropriatePathSplitter(cOUtValueStr, Info.PLATFORM == 'windows'))
        else:
            throwCompileErrorInfo(
                f"The cited attribute '{cRefs}' is not available for {getWidgetName(cWidget.widget_id)}")
    else:
        if inputStr:
            outValuesSet.add(inputStr)

    if len(tmpOutValueSet) > 0:
        for cStr in tmpOutValueSet:
            outValuesSet.update(getWidgetPossFilenames(cWidget, cStr, refValueSetDict))

    return outValuesSet


def isDynamicString(inputStr: str) -> bool:
    meanPat = r'\[([A-Za-z]+[a-zA-Z._0-9]*?)\]@mean'
    medianPat = r'\[([A-Za-z]+[a-zA-Z._0-9]*?)\]@median'
    modePat = r'\[([A-Za-z]+[a-zA-Z._0-9]*?)\]@mode'

    if re.findall(meanPat, inputStr):
        return True
    if re.findall(medianPat, inputStr):
        return True
    if re.findall(modePat, inputStr):
        return True
    return False


def transStatisticExp(inputStr, isString = False):
    meanPat = r'\[([A-Za-z]+[a-zA-Z._0-9]*?)\]@mean'
    medianPat = r'\[([A-Za-z]+[a-zA-Z._0-9]*?)\]@median'
    modePat = r'\[([A-Za-z]+[a-zA-Z._0-9]*?)\]@mode'

    patFunDict = {'mean':meanPat, 'median':medianPat,'mode':modePat}

    # get all event widget names list
    allEventWidgets = getAllEventWidgetsList()
    allEventWidgetNames = []
    for cWidget in allEventWidgets:
        allEventWidgetNames.append(Func.getWidgetName(cWidget.widget_id))

    for func, pattern in patFunDict.items():

        allRefs = re.findall(pattern, inputStr)
        for cRef in allRefs:
            allParts = cRef.split('.')[0]

            if allParts[0] in allEventWidgetNames:
                # for widget data only
                if len(allParts) == 2:
                    if isString:
                        inputStr = re.sub(pattern, rf"',num2str({func}([{allParts[0]}(:).{allParts[1]}])),'", inputStr)
                    else:
                        inputStr = re.sub(pattern, rf'{func}([{allParts[0]}(:).{allParts[1]}])', inputStr)
                else:
                    if isString:
                        inputStr = re.sub(pattern, rf"',num2str({func}([\1])),'", inputStr)
                    else:
                        inputStr = re.sub(pattern, rf'{func}([\1])', inputStr)

            else:
                if isString:
                    inputStr = re.sub(pattern, rf"',num2str({func}([\1])),'", inputStr)
                else:
                    inputStr = re.sub(pattern, rf'{func}([\1])', inputStr)

    return inputStr


def getValueInContainRefExp(cWidget, inputStr, attributesSetDict, isOutStr=False, transformStrDict=None):
    referredObNameList = list()
    isContainRef = 0

    # for string contains citations
    if transformStrDict is None:
        transformStrDict = {}

    # for single
    if isRefStr(inputStr):
        cRefsValue, isContainRef = getRefValue(cWidget, inputStr, attributesSetDict, True)
        if isContainRef:
            # for real citation
            # todo maybe a bug here, since loop variable should be loop.var.
            referredObNameList.append(inputStr[1:-1].split('.')[0:-1])
        else:
            # only have citation format without real citation
            cRefsValue = addSingleQuotes(cRefsValue)

        return cRefsValue, isContainRef, referredObNameList

    refWithBracketPat = r'(\(\[[A-Za-z]+[a-zA-Z._0-9]*?\]\))'
    refPat = r'(\[[A-Za-z]+[a-zA-Z._0-9]*?\])'

    meanPat = r'\[([A-Za-z]+[a-zA-Z._0-9]*?)\]@mean'
    medianPat = r'\[([A-Za-z]+[a-zA-Z._0-9]*?)\]@median'
    modePat = r'\[([A-Za-z]+[a-zA-Z._0-9]*?)\]@mode'

    leftPat = r'--impossibleValeForLeftBracket--'
    rightPat = r'--impossibleValeForRightBracket--'

    inputStr = inputStr.replace('(', leftPat)
    inputStr = inputStr.replace(')', rightPat)

    for key, value in transformStrDict.items():
        inputStr = inputStr.replace(key, value)

    isMatlabStr = inputStr.startswith("'") and inputStr.endswith("'")

    if isMatlabStr:
        # remove the single quotes
        inputStr = inputStr[1:-1]

    if isOutStr or isMatlabStr:
        if not isLegalMatlabStr(inputStr):
            throwCompileErrorInfo(
                f"{inputStr} in {Func.getWidgetName(cWidget.widget_id)}: To match the rules of MATLAB/Octave, you need to use two single quotes to get a single quote inside a string.")

        # inputStr = inputStr.replace("'", "''")
        inputStr = addSingleQuotes(inputStr)

    # if isOutStr and isMatlabStr is False:
    #      inputStr = addSingleQuotes(inputStr)

    # rawInputStr = inputStr
    # stage 1: parse @mean @median or @mode
    if isMatlabStr or isOutStr:

        inputStr = re.sub(meanPat, r"',num2str(mean([\1])),'", inputStr)
        inputStr = re.sub(medianPat, r"',num2str(median([\1])),'", inputStr)
        inputStr = re.sub(modePat, r"',num2str(mode([\1])),'", inputStr)

        # in case the citation located in the begin or the end of inputStr
        # if rawInputStr != inputStr:
        #     if inputStr.startswith("'',num2str(m"):
        #         inputStr = "'" + inputStr[3:]
        #     if inputStr.endswith(")),''"):
        #         inputStr = inputStr[0:-3] + "'"
    else:
        inputStr = re.sub(meanPat, r'mean([\1])', inputStr)
        inputStr = re.sub(medianPat, r'median([\1])', inputStr)
        inputStr = re.sub(modePat, r'mode([\1])', inputStr)

    # stage 2: parse refs in @ mean, mode, or median
    allRefs = re.findall(refWithBracketPat, inputStr)
    if len(allRefs) > 0:
        for cRefs in allRefs:
            cRefsWithoutBracket = cRefs[1:-1]
            cRefsValue, isRefValue = getRefValue(cWidget, cRefsWithoutBracket, attributesSetDict, True)

            if not isRefStr(cRefsValue):
                referredObNameList.append(
                    "".join(cItem + '.' for cItem in re.sub(r'[\[\]]', '', cRefsWithoutBracket).split('.')[0:-1])[0:-1])

                inputStr = inputStr.replace(cRefs, cRefsValue)

                isContainRef = isContainRef + isRefValue

    # stage 3: parse all other refs
    rawInputStr = inputStr
    allRefs = re.findall(refPat, inputStr)

    if len(allRefs) > 0:
        for cRefs in allRefs:
            cRefsValue, isRefValue = getRefValue(cWidget, cRefs, attributesSetDict, True)

            if not isRefStr(cRefsValue):

                referredObNameList.append(
                    "".join(cItem + '.' for cItem in re.sub(r'[\[\]]', '', cRefs).split('.')[0:-1])[0:-1])

                if isMatlabStr or isOutStr:
                    # inputStr = re.sub(meanPat, r"',num2str(mean([\1])),'", inputStr)
                    inputStr = inputStr.replace(cRefs, f"',num2str({cRefsValue}),'")
                else:
                    inputStr = inputStr.replace(cRefs, cRefsValue)

                isContainRef = isContainRef + isRefValue

    if isMatlabStr or isOutStr:
        # in case the citation located in the begin or the end of inputStr
        if rawInputStr != inputStr:
            if inputStr.startswith("'',"):
                inputStr = inputStr[3:]
            if inputStr.endswith(",''"):
                inputStr = inputStr[0:-3]

        # for whole citation, there no need to add square brackets
        if isContainRef > 0:
            inputStr = addSquBrackets(inputStr)

    isContainRef = isContainRef != 0

    inputStr = inputStr.replace(leftPat, '(')
    inputStr = inputStr.replace(rightPat, ')')

    inputStr = repr(inputStr)

    if inputStr.startswith("'\\'") and inputStr.endswith("\\''"):
        inputStr = addSingleQuotes(inputStr[3:-3])
    else:
        inputStr = inputStr[1:-1]

    return inputStr, isContainRef, referredObNameList


def getWidgetIDInTimeline(widget_id: str) -> list:
    wid_name_list = Func.getWidgetIDInTimeline(widget_id)

    return list(wId for wId, wName in wid_name_list)


# def getRefValue2(cWidget, inputStr, attributesSetDict, allowUnlistedAttr=False) -> list:
#     isUnlistedRef = False
#
#     inputStr, isRefValue = getRefValue(cWidget, inputStr, attributesSetDict, allowUnlistedAttr)
#
#     if isRefValue(inputStr):
#         isUnlistedRef = True
#
#     return [inputStr, isRefValue, isUnlistedRef]

def isCiteQuestStr(inputStr) -> bool:
    global questVarNames

    isCiteQuest = False

    if isRefStr(inputStr):
        inputStr = re.sub(r'[\[\]]', '', inputStr)

    if inputStr in questVarNames:
        return True

    # if inputStr == "randQuestValue":
    #     return True
    # elif inputStr in questVarNames:
    #     valueSet = attributesSetDict[inputStr][2]
    #     for cValue in valueSet:
    #         if re.fullmatch(r'quest\(\d+\)', cValue):
    #             return True

    return isCiteQuest
def str_html_var(s):
    #Loop_4.var.color{iLoop_1}
    if s.find("var")!=-1:
        index=s.find('{')
        alter_s=s[index+1:len(s)-1]
        s=s[:index]
        s=s.replace(".var.","["+alter_s+"]"+"[\"")
        s+="\"]"
    return s

def getRefValue(cWidget, inputStr, attributesSetDict: dict, allowUnlistedAttr: bool = False, isForLoop: bool = False) -> list:
    """
    :param cWidget:
    :param inputStr:
    :param attributesSetDict:
    :param allowUnlistedAttr:
    :param isForLoop: is for the loop widget or not
    :return: list [inputStr, isRefValue]
    """
    isRefValue = False

    if isinstance(inputStr, str):

        isRefValue = isRefStr(inputStr)

        if isRefValue:
            # remove the brackets for refValue : a possible bug here
            inputStr = re.sub(r'[\[\]]', '', inputStr)

            if inputStr in attributesSetDict:
                if isForLoop:
                    inputStr = attributesSetDict[inputStr][1]
                else:
                    if isCiteQuestStr(inputStr):
                        inputStr = f"getQcValue_APL({attributesSetDict[inputStr][1]})"
                    else:
                        inputStr = attributesSetDict[inputStr][1]
            else:
                if allowUnlistedAttr:
                    inputStr = addSquBrackets(inputStr)
                    isRefValue = False
                else:
                    throwCompileErrorInfo(
                        f"The cited attribute '{inputStr}' \nis not available for {getWidgetName(cWidget.widget_id)}")

    return [inputStr, isRefValue]


def getRefValueSet(cWidget, inputStr: str, attributesSetDict: dict):
    isRefValue = False
    valueSet = set()

    if isinstance(inputStr, str):

        isRefValue = isRefStr(inputStr)

        if isRefValue:
            inputStr = re.sub(r"[\[\]]", '', inputStr)

            if inputStr in attributesSetDict:
                valueSet = attributesSetDict[inputStr][2]
                inputStr = attributesSetDict[inputStr][1]
            else:
                throwCompileErrorInfo(
                    f"The cited attribute '{inputStr}' \nis not available for {getWidgetName(cWidget.widget_id)}")

    return [inputStr, isRefValue, valueSet]


def getSpecialRespsFormatAtts(cInputDevices, cSpecialFormatVarDict):
    for cRespProperties in cInputDevices.values():
        if cRespProperties['Device Id'].split('.')[0] == Info.DEV_KEYBOARD:
            updateSpFormatVarDict(cRespProperties['Correct'], 'kbCorrectResp', cSpecialFormatVarDict)
            updateSpFormatVarDict(cRespProperties['Allowable'], 'kbAllowKeys', cSpecialFormatVarDict)
        else:
            updateSpFormatVarDict(cRespProperties['Correct'], 'noKbDevCorrectResp', cSpecialFormatVarDict)
            updateSpFormatVarDict(cRespProperties['Allowable'], 'noKbAllowKeys', cSpecialFormatVarDict)

        updateSpFormatVarDict(cRespProperties['Start'], 'startRect', cSpecialFormatVarDict)
        updateSpFormatVarDict(cRespProperties['End'], 'endRect', cSpecialFormatVarDict)
        updateSpFormatVarDict(cRespProperties['Mean'], 'meanRect', cSpecialFormatVarDict)


def getSpecialFormatAtts(cSpecialFormatVarDict: dict = None, wIdAndWidgetDict: dict = None) -> dict:
    """
    : special varType:
    : percentage
    """
    global parameterTypeDict

    if wIdAndWidgetDict is None:
        wIdAndWidgetDict = {}
    if cSpecialFormatVarDict is None:
        cSpecialFormatVarDict = {}

    if len(wIdAndWidgetDict) == 0:
        wIdAndWidgetItems = Info.WID_WIDGET.items()
    else:
        wIdAndWidgetItems = wIdAndWidgetDict.items()

    for widgetId, cWidget in wIdAndWidgetItems:

        cProperties = Func.getWidgetProperties(widgetId)

        if Func.isWidgetType(widgetId, Info.LOOP):
            pass
        elif Func.isWidgetType(widgetId, Info.SWITCH):
            # we do not need to do this here because all sub widgets are contained in Info.Wid_WIDGET
            # cSwitchList = cWidget.getCases()
            pass

        elif Func.isWidgetType(widgetId, Info.IF):
            # cTrueWidget = cWidget.getTrueWidget()
            # cSpecialFormatVarDict = getSpecialFormatAtts(cSpecialFormatVarDict, {cTrueWidget.widget_id: cTrueWidget})
            pass

        elif Func.getWidgetType(widgetId) in [Info.TEXT, Info.VIDEO, Info.SOUND,Info.IMAGE]:
            for cWidgetKey, cWidgetValue in cProperties.items():
                if cWidgetKey in parameterTypeDict:
                    updateSpFormatVarDict(cWidgetValue, parameterTypeDict[cWidgetKey], cSpecialFormatVarDict)

            getSpecialRespsFormatAtts(cWidget.getInputDevice(), cSpecialFormatVarDict)

        elif Func.isWidgetType(widgetId, Info.COMBO):
            for cWidgetKey, cWidgetValue in cProperties['Properties'].items():
                if cWidgetKey in parameterTypeDict:
                    updateSpFormatVarDict(cWidgetValue, parameterTypeDict[cWidgetKey], cSpecialFormatVarDict)

            cItems = cProperties['Items']
            itemIds = getSliderItemIds(cWidget)
            itemIds.reverse()  # reverse the key id order

            for cItemId in itemIds:
                # cItemType = getItemType(cItemId)
                cItemProperties = cItems[cItemId]

                for cItemKey, cItemValue in cItemProperties.items():

                    if cItemKey in parameterTypeDict:
                        if cItemKey == 'Points':
                            for cXY in cItemValue:
                                updateSpFormatVarDict(cXY[0], parameterTypeDict[cItemKey], cSpecialFormatVarDict)
                                updateSpFormatVarDict(cXY[1], parameterTypeDict[cItemKey], cSpecialFormatVarDict)
                        else:
                            # Center X Y in polygon is int
                            updateSpFormatVarDict(cItemValue, parameterTypeDict[cItemKey], cSpecialFormatVarDict)

            getSpecialRespsFormatAtts(cWidget.getInputDevice(), cSpecialFormatVarDict)

    return cSpecialFormatVarDict


def list2matlabCell(varNameList: list, addedCurlyBrackets: bool = True, addedSingleQuote: bool = True) -> str:
    """
    :param varNameList: list of strings
    :param addedCurlyBrackets: added {} or not
    :param addedSingleQuote: added '' for each item or not
    :return: string
    """
    cellStr4Mat = list2Str(varNameList, ', ', addedSingleQuote)

    if addedCurlyBrackets:
        return addCurlyBrackets(cellStr4Mat)
    else:
        return cellStr4Mat


def list2Str(varNameList: list, Spacer: str = ' ', addedSingleQuote: bool = True) -> str:
    """
    :param varNameList: list of string
    :param Spacer:      split char
    :param addedSingleQuote: added single quote or not
    :return: string
    """
    if addedSingleQuote:
        cellStr4Mat = ''.join("'" + cVarName + "'" + Spacer for cVarName in varNameList)
    else:
        cellStr4Mat = ''.join(cVarName + Spacer for cVarName in varNameList)
    return cellStr4Mat[0:-len(Spacer)]


def getUniqueList(inputList: list) -> list:
    outputList = list()
    for item in inputList:
        if item not in outputList:
            outputList.append(item)

    return outputList


def getOutputDevCountsDict() -> dict:
    output_devices = Info.OUTPUT_DEVICE_INFO

    iMonitor = 0
    iParal = 0
    iNetPort = 0
    iSerial = 0
    iSound = 0

    for outDev_Id, cDevice in output_devices.items():

        if cDevice['Device Type'] == Info.DEV_SCREEN:
            iMonitor += 1
        elif cDevice['Device Type'] == Info.DEV_NETWORK_PORT:
            iNetPort += 1
        elif cDevice['Device Type'] == Info.DEV_PARALLEL_PORT:
            iParal += 1
        elif cDevice['Device Type'] == Info.DEV_SERIAL_PORT:
            iSerial += 1
        elif cDevice['Device Type'] == Info.DEV_SOUND:
            iSound += 1

    return {Info.DEV_SCREEN: iMonitor, Info.DEV_NETWORK_PORT: iNetPort, Info.DEV_PARALLEL_PORT: iParal,
            Info.DEV_SERIAL_PORT: iSerial, Info.DEV_SOUND: iSound}


# def getWidgetPosType(cWidget) -> int or None:
def getWidgetPosType(cWidget):
    global stimWidgetTypesList
    cWidgetPosType = None  # 0 -1 None for start, end, and others in event position respectively

    # if is the sub widget of a IF or SWITCH widget, get the pos via inquiring the parent widget
    if isSubWidgetOfIfOrSwitch(cWidget.parent()):
        return getWidgetPosType(cWidget.parent())

    cWidgetId = cWidget.widget_id

    while getWidgetType(cWidgetId) in stimWidgetTypesList:

        if getWidgetType(cWidgetId) in stimWidgetTypesList:
            while isFirstStimWidgetInTL(cWidgetId) or isLastStimWidgetInTL(cWidgetId):
                # Loop till we get a none timeline parentId
                while getWidgetType(cWidgetId) != Info.TIMELINE:
                    cWidgetId = Func.getParentWid(cWidgetId)

            if isFirstStimWidgetInTL(cWidgetId):
                cWidgetPosType = 0
                break
            elif isLastStimWidgetInTL(cWidgetId):
                cWidgetPosType = -1
                break
        else:
            break

    return cWidgetPosType


# noinspection PyBroadException
def getWidLoopLevel(wid: str) -> int:
    """
    :only cycle can increase the loop level
    :param wid: 输入的wid
    :return: 如果wid不存在，返回-1
    """
    try:
        node = Info.WID_NODE[wid]
    except:
        return -1
    # 不断迭代，直至父结点为空
    loopLevel = 1

    node = node.parent()

    while node:
        node = node.parent()
        if Func.isWidgetType(node.widget_id, Info.LOOP):
            loopLevel += 1
    return loopLevel


def getItemType(itemId: str) -> str:
    return itemId.split('_')[0]


def formatLoopVarValue(cWidget , value, attributesSetDict: dict, allLoopNames: list):
    needCurlyBrackets = True

    refValue, isRef = getRefValue(cWidget, value, attributesSetDict, True, True)

    if isRef and refValue.split('.')[0] in allLoopNames:
        needCurlyBrackets = False
        refValue = re.sub(r'{([A-Za-z._\-0-9]+?)}$', r'(\1)', refValue)

    # refValue = dataStrConvert(refValue, isRef, False, False)

    if needCurlyBrackets:
        refValue = addCurlyBrackets(refValue)

    return refValue


def getClearAfterInfo(cWidget, attributesSetDict) -> str:
    """
    :param cWidget:
    :param attributesSetDict:
    :return:
    : "clear_0"     -> "0"
    : "notClear_1"  -> "1"
    : "doNothing_2" -> "2"
    : "0" -> "0"
    : "1" -> "1"
    : "2" -> "2"
    """

    if Info.COMBO == getWidgetType(cWidget):
        cProperties = Func.getWidgetProperties(cWidget.widget_id)['Properties']
    else:
        cProperties = Func.getWidgetProperties(cWidget.widget_id)

    clearAfter = dataStrConvert(*getRefValue(cWidget, cProperties['Clear After'], attributesSetDict))
    clearAfter = parseDontClearAfterStr(clearAfter)

    return clearAfter


def getScreenInfo(cWidget, attributesSetDict):
    """
    :param cWidget:
    :param attributesSetDict:
    :return:
    :cScreenName:
    :cWinIdx: index of the current screen
    :cWinStr: winIdx(index) in matlab
    """
    global outputDevNameIdxDict
    shouldNotBeCitationCheck('Screen Name', cWidget.getScreenName())

    cScreenName, ign = getRefValue(cWidget, cWidget.getScreenName(), attributesSetDict)

    # currently we just used the nearest previous flipped screen info
    cWinIdx = outputDevNameIdxDict.get(cScreenName)
    cWinStr = f"winIds({cWinIdx})"

    return cScreenName, cWinIdx, cWinStr


def getSliderItemIds(cWidget, itemType='') -> list:
    itemIds = []
    if Func.isWidgetType(cWidget.widget_id, Info.COMBO):
        properties = Func.getWidgetProperties(cWidget.widget_id)

        if len(itemType) == 0:
            itemIds = [key for key in properties['Items'].keys()]
        else:
            itemIds = [key for key in properties['Items'].keys() if getItemType(key) == itemType]

    return itemIds


def getSliderItemTypeNums(cWidget, itemType: str) -> int:
    itemNums = 0

    if Func.isWidgetType(cWidget.widget_id, Info.COMBO):
        itemIds = getSliderItemIds(cWidget)

        for cItemId in itemIds:
            if getItemType(cItemId) == itemType:
                itemNums += 1

    return itemNums


def getParentCycleWid(widgetId: str):
    parentTL = Func.getParentWid(widgetId)
    return Func.getParentWid(parentTL)


def getCycleFillAttrAllRangeNums(cWidget) -> int:
    return getParentCycleLoopNums(cWidget) * getSubCycleAttMaxFillRanges(cWidget)


def getParentCycleLoopNums(cWidget) -> int:
    allParentLoopNums = 1
    cCycleWidget_id = cWidget.widget_id

    while cCycleWidget_id:
        cParentLoopRows = getParentCycleLoopRows(cCycleWidget_id)
        allParentLoopNums *= cParentLoopRows

        cCycleWidget_id = getParentCycleWid(cCycleWidget_id)

    return allParentLoopNums


def isAnyTeBeFilledCycle() -> bool:
    """
    :return: True or False for need to be filled or not respectively
    """
    allCycleWidgets = getAllEventWidgetsList(2)
    for cCycle in allCycleWidgets:
        if isCycleContainsSubCycle(cCycle):
            return True
    return False


def getParentCycleLoopRows(cCycleWidget_id) -> int:
    nReps = 1
    cTL_id = Func.getParentWid(cCycleWidget_id)
    cTLName = getWidgetName(cTL_id)

    # todo maybe a bug here
    parentCycleWid = getParentCycleWid(cCycleWidget_id)

    if parentCycleWid:
        pCycleWidget = Func.getWidget(parentCycleWid)

        if pCycleWidget:
            for iRow in range(pCycleWidget.rowCount()):
                cRowDict = pCycleWidget.getAttributes(iRow)
                if cTLName == cRowDict['Timeline']:
                    if '' == cRowDict['Repetitions']:
                        cRepeat = 1
                    else:
                        cRepeat = dataStrConvert(cRowDict['Repetitions'])

                    nReps += cRepeat

    return nReps


def getSubCycleAttMaxFillRanges(cWidget) -> int:
    nFillRanges = 0

    cTLNameIdList = cWidget.getTimelines()

    for iRow in range(cWidget.rowCount()):
        if isContainCycleTL(cTLNameIdList[iRow][1]):
            cRowDict = cWidget.getAttributes(iRow)

            if '' == cRowDict['Repetitions']:
                cRepeat = 1
            else:
                cRepeat = dataStrConvert(cRowDict['Repetitions'])

            nFillRanges += cRepeat

    return nFillRanges


def isCycleContainsSubCycle(cWidget) -> bool:
    cTLNameIdList = cWidget.getTimelines()
    # squeeze the timelines
    cTLIdList = set()
    for cTLNameId in cTLNameIdList:
        cTLIdList.add(cTLNameId[1])

    for cTL_id in cTLIdList:
        if isContainCycleTL(cTL_id):
            return True

    return False


def getContainItemTypeNums(itemIds: list, itemType: str) -> int:
    itemNums = 0
    for cItemId in itemIds:
        if getItemType(cItemId) == itemType:
            itemNums += 1

    return itemNums


def getMaximumOpDataRows() -> int:
    MaxOpDataRows = updateTLOpDataRow(Info.WID_WIDGET[f"{Info.TIMELINE}.0"], 0)

    return MaxOpDataRows


def getMaxSlaveSoundDevs() -> dict:
    # dictionary: sound dev ID:maximum slave devs
    maxSlaveSoundDevs = dict()

    for cWidget in Info.WID_WIDGET.values():
        maxSlaveSoundDevs.update(getWidgetMaxSlaveSoundDevs(cWidget))

    return maxSlaveSoundDevs


def getWidgetMaxSlaveSoundDevs(cWidget) -> dict:
    # dictionary: sound dev ID:maximum slave devs
    maxSlaveSoundDevs = dict()

    cWidgetId = cWidget.widget_id

    if Func.isWidgetType(cWidgetId, Info.COMBO):
        itemIds = getSliderItemIds(cWidget)

        cProperties = Func.getWidgetProperties(cWidgetId)

        if isContainItemType(itemIds, Info.ITEM_SOUND):
            cSoundNumList = dict()

            for cItemId in itemIds:
                if getItemType(cItemId) == Info.ITEM_SOUND:
                    cItemPro = cProperties['Items'][cItemId]
                    cSoundDevName = cItemPro['Sound Device']
                    cSoundDevNum = cSoundNumList.get(cSoundDevName, 0)
                    cSoundNumList.update({cSoundDevName: cSoundDevNum + 1})

                    nSounds = max(maxSlaveSoundDevs.get(cSoundDevName, 0), cSoundNumList[cSoundDevName])
                    maxSlaveSoundDevs.update({cSoundDevName: nSounds})

    elif Func.isWidgetType(cWidgetId, Info.SOUND):
        cProperties = Func.getWidgetProperties(cWidgetId)
        nSounds = max(maxSlaveSoundDevs.get(cProperties['Sound Device'], 0), 1)
        maxSlaveSoundDevs.update({cProperties['Sound Device']: nSounds})

    return maxSlaveSoundDevs


def getWidgetType(cWidgetOrId) -> str:
    if isinstance(cWidgetOrId, str):
        return cWidgetOrId.split('.')[0]
    else:
        return cWidgetOrId.widget_id.split('.')[0]


def getWidgetIdType(widget_id: str) -> str:
    return widget_id.split('.')[0]


def updateTLOpDataRow(cTLWidget, opDataRowsInPy: int) -> int:
    noSubCycleTL = True

    cTimelineWidgetIds = getWidgetIDInTimeline(cTLWidget.widget_id)

    for cWidgetId in cTimelineWidgetIds:
        cWidget = Info.WID_WIDGET[cWidgetId]

        if Func.isWidgetType(cWidgetId, Info.LOOP):
            noSubCycleTL = False
            opDataRowsInPy = updateCycleOpDataRows(cWidget, opDataRowsInPy)

    if noSubCycleTL:
        opDataRowsInPy += 1

    return opDataRowsInPy


def updateCycleOpDataRows(cCyleWdiget, opDataRowsInPy: int) -> int:
    cTimeLineids = cCyleWdiget.getTimelines()

    for iRow in range(cCyleWdiget.rowCount()):
        cRowDict = cCyleWdiget.getAttributes(iRow)
        cTLid = cTimeLineids[iRow]
        cTLWidget = Info.WID_WIDGET[cTLid[1]]

        if '' == cRowDict['Repetitions']:
            cRepeat = 1
        else:
            cRepeat = dataStrConvert(cRowDict['Repetitions'])

        for iRep in range(cRepeat):
            opDataRowsInPy = updateTLOpDataRow(cTLWidget, opDataRowsInPy)
    return opDataRowsInPy


def printCycleWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes):
    global spFormatVarDict, cInfoDict, questVarNames
    print(spFormatVarDict)
    # start from 1 to compatible with MATLAB
    cLoopLevel += 1
    # cOpDataRowNum = cInfoDict.get('maximumRows')
    attributesSetDict = copy.deepcopy(attributesSetDict)

    cWidgetName = getWidgetName(cWidget.widget_id)

    attributesSetDict.setdefault(f"{cWidgetName}.cLoop", [cLoopLevel, f"iLoop_{cLoopLevel}", {f"iLoop_{cLoopLevel}"}])

    attributesSetDict.setdefault(f"{cWidgetName}.rowNums",
                                 [cLoopLevel, f"size({cWidgetName}.var,1)", {f"size({cWidgetName}.var,1)"}])
    print(attributesSetDict)
    # if cLoopLevel > 1:
    #     attributesSetDict.setdefault(f"{cWidgetName}.rowNums", [cLoopLevel, f"size({cWidgetName}.raw,1)", {f"size({cWidgetName}.raw,1)"}])
    # else:
    #     attributesSetDict.setdefault(f"{cWidgetName}.rowNums", [cLoopLevel, f"size({cWidgetName}.var,1)", {f"size({cWidgetName}.var,1)"}])

    cLoopIterStr = attributesSetDict[f"{cWidgetName}.cLoop"][1]
    allLoopWidgetNames = getAllEventWidgetNamesList(2)

    cCycleVarDataCodes = allWidgetCodes.get(f"{cWidgetName}_varData", [])

    '''
    # create the design matrix  (table) for the current cycle
    '''
    startExpStr = cWidgetName + '.var = cell2table({...'
    # if cLoopLevel > 1:
    #     startExpStr = cWidgetName + '.raw = cell2table({...'
    # else:
    #     startExpStr = cWidgetName + '.var = cell2table({...'

    # printAutoInd(cCycleVarDataCodes, '% create the designMatrix for the loop: {0}', cWidgetName)
    # printAutoInd(cCycleVarDataCodes, '{0}', startExpStr)

    endExpStr = "},'VariableNames',{"

    referredWidgetList = []
    # get referred widget list:
    cRowlist=[]
    cRowstr="var "+cWidgetName+"=["
    for iRow in range(cWidget.rowCount()):
        cRowDict = cWidget.getAttributes(iRow)
        print(cRowDict)
        cRowstr+="{"
        for i,j in cRowDict.items():
            cRowstr+="\""+str(i)+"\""
            cRowstr+=":"
            if str(i)!="Repetitions":
                cRowstr+="\""+str(j)+"\""
                cRowstr+=","
            else:
                cRowstr+=str(j)
                cRowstr+=","
        cRowlist.append(cRowDict)
        cRowstr=cRowstr.rstrip(',')
        cRowstr+="},"
        for _, value in cRowDict.items():
            if isRefStr(value):
                tempValue = re.sub(r"[\[\]]", '', value)
                # none match will return the raw string
                if tempValue.split('.')[0] != tempValue:
                    referredWidgetList.append(tempValue.split('.')[0])
    cRowstr=cRowstr.rstrip(',')
    cRowstr+="];"
    # preWidget_name = ''
    printPreRespCodeBeforeDesignMatrix = False
    printAutoInd(f,"{0}",cRowstr)
    preWidget_id = getPreWID(cWidget.widget_id)
    print(cRowlist,cRowstr)
    if preWidget_id:
        preWidget_name = getWidgetName(preWidget_id)

        if preWidget_name in referredWidgetList:
            printPreRespCodeBeforeDesignMatrix = True
            # print response codes of the previous widget if possible
            printInAllWidgetCodesByKey(f, allWidgetCodes, f"{preWidget_id}_cRespCodes")

    #cWidget.getAttributes(iRow)即可获得对应行的字典
    for iRow in range(cWidget.rowCount()):
        cRowDict = cWidget.getAttributes(iRow)
        if 0 == iRow:
            endExpStr = endExpStr + ''.join("'" + key + "' " for key in cRowDict.keys()) + "});"

        for key, value in cRowDict.items():
            # get all quest related variables
            cVarNamestr = f"{Func.getWidgetName(cWidget.widget_id)}.var.{key}"
            if isCiteQuestStr(value):
                questVarNames.append(cVarNamestr)
            print("!!!!???!!!")
            print(cVarNamestr)
            # get the referenced var value
            cValue, isRefValue, cRefValueSet = getRefValueSet(cWidget, value, attributesSetDict)

            cKeyAttrName = f"{cWidgetName}.var.{key}"
            print("###!!!!???!!!###")
            print(cVarNamestr)
            """
            # handle the references and the values in special format (e.g., percent, duration)
            """
            isTransformed = False
            # --- replaced the percentageStr--------/
            if cKeyAttrName in spFormatVarDict:
                if 'percent' == spFormatVarDict[cKeyAttrName]:
                    cValue = parsePercentStr(cValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'dur' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseDurationStr(cValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'fontStyle' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseFontStyleStr(cValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'clearAfter' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseDontClearAfterStr(cValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'flipHorizontal' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'flipVertical' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'rightToLeft' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'enableFrame' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'waitForStart' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'kbCorrectResp' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseRespKeyCodesStr(cValue, isRefValue, Info.DEV_KEYBOARD)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'noKbDevCorrectResp' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseRespKeyCodesStr(cValue, isRefValue, 'noneKbDevs')
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'kbAllowKeys' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseRespKeyCodesStr(cValue, isRefValue, Info.DEV_KEYBOARD)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'noKbAllowKeys' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseRespKeyCodesStr(cValue, isRefValue, 'noneKbDevs')
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'textContent' == spFormatVarDict[cKeyAttrName]:

                    if Func.isRef(value) > 1:
                        throwCompileErrorInfo(f"{cKeyAttrName}: can only be either a plaint text content or citation, should not be a nested citation! -> {value}")

                    if not isLegalMatlabStr(value):
                        throwCompileErrorInfo(f"'{value}' in {cKeyAttrName}: To match the rules of MATLAB/Octave, you need to use two single quotes to get a single quote inside a string.")

                    cValue = parseTextContentStr(cValue, isRefValue)

                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'aspectRation' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseAspectRationStr(cValue, isRefValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'stretchMode' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseAspectRationStr(cValue, isRefValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'startRect' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseRectStr(cValue, isRefValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'endRect' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseRectStr(cValue, isRefValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'meanRect' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseRectStr(cValue, isRefValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'color' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseColorStr(cValue, isRefValue)
                    cRowDict[key] = cValue
                    isTransformed = True

                elif 'boolean' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue
                    isTransformed = True
            #     TO BE CONTINUING... FOR ALL OTHER Special Types
            # --------------------------------------\
            # todo maybe a bug here
            if not isRefValue and not isTransformed and key != 'Repetitions':
                cRowDict[key] = dataStrConvert(cValue, isRefValue, False, False)
            if not isRefValue:
                cRefValueSet = {cValue}
            if cKeyAttrName in attributesSetDict:
                preValueSet = attributesSetDict[cKeyAttrName][2]
            else:
                preValueSet = set()
            #昨天到这里
            attributesSetDict.update(
                {cKeyAttrName: [cLoopLevel, f"{cKeyAttrName}{{{cLoopIterStr}}}", cRefValueSet.union(preValueSet)]})
        # print out the design matrix of the current Cycle
        print("attributesSetDict")
        print(attributesSetDict)
        if '' == cRowDict['Repetitions']:
            cRepeat = 1
        else:
            cRepeat = dataStrConvert(cRowDict['Repetitions'])
        for iRep in range(cRepeat):
            printAutoInd(cCycleVarDataCodes, '{0}', "".join(
                formatLoopVarValue(cWidget , value, attributesSetDict, allLoopWidgetNames) + " "
                for key, value in cRowDict.items()) + ";...")

    # printAutoInd(cCycleVarDataCodes, '{0}\n', endExpStr)

    # Shuffle the designMatrix:
    cycleOrderStr = dataStrConvert(*getRefValue(cWidget, cWidget.getOrder(), attributesSetDict))
    cycleOrderByStr = dataStrConvert(*getRefValue(cWidget, cWidget.getOrderBy(), attributesSetDict))

    #  to make sure the repetitions is one for counterbalance selection of order ----/
    if cycleOrderStr == "'Counter Balance'":
        cCycleWeightList = cWidget.getAttributeValues(0)
        for cLineWeight in cCycleWeightList:
            if dataStrConvert(cLineWeight) != 1:
                throwCompileErrorInfo(
                    f"Found an incompatible error in Cycle {cWidgetName}:\nFor Counter Balance selection, the timeline repetitions should be 1")
    # ------------------------------------------------------------------------\

    # printAutoInd(f, "% Create the design matrix for loop '{0}'", cWidgetName)
    # printAutoInd(f, "{0} = {0}_makeData_APL;\n", cWidgetName)

    # printAutoInd(f, "% Shuffle the DesignMatrix")

    cLJustLen = len(cWidgetName) + 4
    # printAutoInd(f, '{0} = ShuffleCycleOrder_APL({1},{2},{3},subInfo);', "cShuffledIdx".ljust(cLJustLen, ' '),
    #              attributesSetDict[f"{cWidgetName}.rowNums"][1], cycleOrderStr, cycleOrderByStr)
    print("cShuffledIdx".ljust(cLJustLen, ' '),
          attributesSetDict[f"{cWidgetName}.rowNums"][1], cycleOrderStr, cycleOrderByStr)
    # printAutoInd(f, '{0}.var = {0}.var(cShuffledIdx,:);', cWidgetName)

    # if cLoopLevel > 1:
    #     printAutoInd(f, '{0}.var = {0}.raw(cShuffledIdx,:);', cWidgetName)
    # else:
    #     printAutoInd(f, '{0}.var = {0}.var(cShuffledIdx,:);', cWidgetName)

    # printAutoInd(f, " ")

    # print previous stim widget's response code
    if preWidget_id and printPreRespCodeBeforeDesignMatrix is False:
        # print response codes of the previous widget if possible
        printInAllWidgetCodesByKey(f, allWidgetCodes, f"{preWidget_id}_cRespCodes")

    # cycling
    # record start rows for possible to be filled Loop attributes
    cCycleParentCycle_id = getParentCycleWid(cWidget.widget_id)
    if cCycleParentCycle_id:
        pass
        # printAutoInd(f, "% record the start row for the to be filled Loop {0} variables ", cCycleParentCycle_id)
        # printAutoInd(f, "beFilledVarStruct_APL.{0}.startEndRows(1, beFilledVarStruct_APL.{0}.iCol) = opRowIdx;\n",
        #              getWidgetName(cCycleParentCycle_id))
    print("cCycleParentCycle_id")
    print(cCycleParentCycle_id)
    # printAutoInd(f, '% looping across each row of the {0}.var:{1}', cWidgetName, cLoopIterStr)
    # printAutoInd(f, 'for {0} =1:size({1},1)', cLoopIterStr, f"{cWidgetName}.var")
    printAutoInd(f,"for(let {0}=0;{0}<{1}.length;{0}++)",cLoopIterStr,cWidgetName)
    f.write("{")
    cLoopOpIdxStr = cLoopIterStr + "_cOpR"

    # printAutoInd(f, "{0} = opRowIdx; % output var row num for loop level {1}\n", cLoopOpIdxStr, cLoopLevel)
    print("cWidgetName, cLoopIterStr,cLoopIterStr:")
    print(cWidgetName, cLoopIterStr,cLoopIterStr)
    # printAutoInd(f, "% variable values will be recorded in variables named following the rule: {0}.var.attName to {0}_attName", cWidgetName)
    # printAutoInd(f, "% e.g., the attribute variable {0}.var.Repetitions will be recorded in variable {0}_Repetitions", cWidgetName)
    # printAutoInd(f, "% copy attr var values into output vars for row {0}", cLoopOpIdxStr)

    cRowDict = cWidget.getAttributes(0)
    otVarStr = ''.join(cWidgetName + '_' + key + f"{{{cLoopOpIdxStr}}}," for key in cRowDict.keys())
    otVarStr = f"[{otVarStr[0:-1]}] = deal({cWidgetName}.var{{{cLoopIterStr},:}}{{:}});"

    # printAutoInd(f, "{0}\n", otVarStr)
    print("otVarStr")
    print(otVarStr)
    # handle each timeline
    cTimeLineList = cWidget.getTimelines()
    # squeeze the timelines
    cTimelineIdSet = set()
    print("cTimeLineList")
    print(cTimeLineList)
    for iTimeline in cTimeLineList:
        cTimelineIdSet.add(iTimeline[1])
    print("cTimelineIdSet")
    print(cTimelineIdSet)
    # printAutoInd(f, '% switch across timeline types')
    printAutoInd(f,'for(let {0}=0;{0}<{2}[{1}]["Repetitions"];{0}++)',cLoopOpIdxStr,cLoopIterStr,cWidgetName)
    f.write('{')
    printAutoInd(f, 'switch ({1}[{0}]["Timeline"])',cLoopIterStr,cWidgetName)
    f.write("{")
    for iTimeline_id in cTimelineIdSet:
        if '' == iTimeline_id:
            throwCompileErrorInfo(f"In {cWidgetName}: Timeline should not be empty!")
        else:
            printAutoInd(f, 'case {0}:', f"{addSingleQuotes(getWidgetName(iTimeline_id))}")

            allWidgetCodes = printTimelineWidget(Info.WID_WIDGET[iTimeline_id], f, attributesSetDict, cLoopLevel,
                                                 allWidgetCodes)
            printAutoInd(f,"break;")
            print(Info.WID_WIDGET[iTimeline_id])
            if not isContainCycleTL(iTimeline_id):
                pass
                # printAutoInd(f, "opRowIdx = opRowIdx + 1; % increase outputVars by 1 only when TL contains no subLoop")

    # printAutoInd(f, 'otherwise ')
    # printAutoInd(f, '% do nothing ')
    # printAutoInd(f, 'end%switch {0}', f"{cWidgetName}.var.Timeline{{{cLoopIterStr}}}")
    #
    # printAutoInd(f, 'end % {0}', cLoopIterStr)
    f.write('}')
    f.write('}')
    f.write('}')
    # Save end rows for possible need to be filled Loop attributes
    # if cCycleParentCycle_id:
    #     printAutoInd(f, "% record the end row num for the to be filled Loop {0} variables ", cCycleParentCycle_id)
    #     printAutoInd(f, "beFilledVarStruct_APL.{0}.startEndRows(2, beFilledVarStruct_APL.{0}.iCol) = opRowIdx;\n",
    #                  getWidgetName(cCycleParentCycle_id))
    #     printAutoInd(f, "beFilledVarStruct_APL.{0}.iCol = beFilledVarStruct_APL.{0}.iCol + 1;\n",
    #                  getWidgetName(cCycleParentCycle_id))

    '''
    # --------------------------------------------------------------
    # close possible textures and maybe audio buffers in the further
    # --------------------------------------------------------------
    '''
    # close possible visual textures
    xedTxAFCycleWidgetFilenameList: list = allWidgetCodes.get(f"xedTxAFCycleWidgetFilenameList_{cLoopLevel}", [])

    xedTxAFCycleWidgetFilenameList = getUniqueList(xedTxAFCycleWidgetFilenameList)

    if len(xedTxAFCycleWidgetFilenameList) > 0:
        xedWidgetNameAFCycleList = list()
        xedFilenamesAFCycleList = list()

        for item in xedTxAFCycleWidgetFilenameList:
            for k, v in item.items():
                xedWidgetNameAFCycleList.append(k)
                xedFilenamesAFCycleList.append(v)

        # printAutoInd(f, ' ')
        # printAutoInd(f, '% close image textures for Loop : {0}', cWidgetName)
        #
        # printAutoInd(f, "CloseTexture_APL({0}, {1}, false);\n",
        #              getImaIndexStr(xedFilenamesAFCycleList),
        #              getWidNameIndexStr(xedWidgetNameAFCycleList))
        allWidgetCodes.update({f"xedTxAFCycleWidgetFilenameList_{cLoopLevel}": []})

    beClosedTxAFCycleList = allWidgetCodes.get(f"beClosedTextures_{cLoopLevel}", [])
    if len(beClosedTxAFCycleList) > 0:
        bePrintStr = "".join(f"{cTx}," for cTx in beClosedTxAFCycleList)
        if len(beClosedTxAFCycleList) == 1:
            bePrintStr = "Screen('Close'," + bePrintStr[0:-1] + ");\n"
        else:
            bePrintStr = "Screen('Close',[" + bePrintStr[0:-1] + "]);\n"

        printAutoInd(f, ' ')
        if closeImaMethodType:
            printAutoInd(f, '% close textures of stim generated by MATLAB (e.g., Gabor, Snow)')
        else:
            printAutoInd(f, '% close visual textures')

        printAutoInd(f, bePrintStr)
    # after print clean up the list
    allWidgetCodes.update({f"beClosedTextures_{cLoopLevel}": []})
    allWidgetCodes.update({f"{cWidgetName}_varData": cCycleVarDataCodes})

    # close possible audio buffers

    return allWidgetCodes


# noinspection PyStringFormat
def printToDelayedCodes(allWidgetCodes, keyName, inputStr, *argins):
    global isDummyPrint

    if not isDummyPrint:
        allWidgetCodes[keyName].append = f"{inputStr}".format(*argins)


def printInAllWidgetCodesByKey(f, bePrintedCodes: dict, key='respCodes') -> dict:
    cKeyValueList = bePrintedCodes.get(key, [])

    for cRowStr in cKeyValueList:
        cRowStr = "{{".join(cRowStr.split('{'))
        cRowStr = "}}".join(cRowStr.split('}'))
        printAutoInd(f, cRowStr)

    bePrintedCodes.update({key: []})  # clean the key value

    return bePrintedCodes


# def printBeforeFlipCodes(f, bePrintedCodes: dict or list) -> dict or list:
def printBeforeFlipCodes(f, bePrintedCodes):
    if isinstance(bePrintedCodes, dict):
        cCodesBeFip = bePrintedCodes.get('codesBeFip', [])
        for cRowStr in cCodesBeFip:
            cRowStr = "{{".join(cRowStr.split('{'))
            cRowStr = "}}".join(cRowStr.split('}'))
            printAutoInd(f, cRowStr)
        # clear out the print buffer
        bePrintedCodes.update({'codesBeFip': []})
    elif isinstance(bePrintedCodes, list):
        for cRowStr in bePrintedCodes:
            cRowStr = "{{".join(cRowStr.split('{'))
            cRowStr = "}}".join(cRowStr.split('}'))
            printAutoInd(f, cRowStr)
        bePrintedCodes = []

    return bePrintedCodes


def flipScreen(cWidget, f, cLoopLevel, attributesSetDict, allWidgetCodes):
    global historyPropDict, isDummyPrint
    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num

    # get screen index and cWinStr :winIdx(index)
    _, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    clearAfter = getClearAfterInfo(cWidget, attributesSetDict)

    cWidgetName = getWidgetName(cWidget.widget_id)
    cWidgetPos = getWidgetEventPos(cWidget.widget_id)

    cRespCodes = allWidgetCodes.get(f"{cWidget.widget_id}_cRespCodes", [])

    # if getWidgetPos(cWidget.widget_id) > 0 and not(isSubWidgetOfIfOrSwitch(cWidget.widget_id)):
    #     # Step 2: print out help info for the current widget
    #     printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    #     printAutoInd(f, '%loop:{0}, event{1}: {2}', cLoopLevel, cWidgetPos + 1,
    #                  getWidgetName(cWidget.widget_id))
    #     printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    flipType = getFlipType(cWidget)
    # 0,1,2 for none, video related widget , and dot motion respectively
    if flipType:
        # slicing flip
        allWidgetCodes = printBeforeFlipCodes(f, allWidgetCodes)

        allWidgetCodes = genCheckResponse(cWidget, f, cLoopLevel, attributesSetDict, allWidgetCodes)
        # printAutoInd(f, "% initialise video flip ")
        # printAutoInd(f, "iFrame = 1;")
        # printAutoInd(f, "secs              = GetSecs;")
        # printAutoInd(f, "afVideoFipReqTime = GetSecs; % temp value but ensure larger than secs\n")

        cVideoItemNums = getSliderItemTypeNums(cWidget, Info.ITEM_VIDEO)

        # if bitGet(flipType, 0):
        #     '''
        #     have video widgets
        #     '''
        #     if cVideoItemNums > 1:
        #         # printAutoInd(f, "{0}_beClosedMIdx = true(1,{1});", cWidgetName, cVideoItemNums)
        #         printAutoInd(f," ")
        #     if cVideoItemNums <= 1:
        #         # printAutoInd(f, "{0}_tPtr = 1;", cWidgetName)
        #         # printAutoInd(f, "{0}_CPt  =-1;\n", cWidgetName)
        #         printAutoInd(f," ")
        #
        #         # printAutoInd(f, "while {0}_tPtr > 0 && {0}_CPt < {0}_eMTime", cWidgetName)
        #         # printAutoInd(f, "while secs < afVideoFipReqTime", cWidgetName)
        #     else:
        #         # printAutoInd(f, "{0}_tPtrs = repmat(1,1,{1});", cWidgetName, cVideoItemNums)
        #         # printAutoInd(f, "{0}_CPts  = repmat(-1,1,{1});", cWidgetName, cVideoItemNums)
        #         #
        #         # printAutoInd(f, "while any( {0}_tPtrs > 0 && ({0}_CPts./{0}_eMTimes) < 1 )", cWidgetName)
        #         printAutoInd(f," ")
        # else:
        #     '''
        #     have no video widget & have dot motion slider only
        #     '''
        #     # printAutoInd(f, "while secs < afVideoFipReqTime", cWidgetName)
        #     printAutoInd(f," ")

        ''' 
        draw all visual stim looply over here: print cVSLCodes 
        '''
        allWidgetCodes = printInAllWidgetCodesByKey(f, allWidgetCodes, 'forVideoSliderLoopCodes')

        # printAutoInd(f, f"[isTerminateStimEvent, secs] = checkResp_SendRespTrig_APL(cDurs({cWinIdx}), afVideoFipReqTime, true); ")
        #
        # printAutoInd(f, "if iFrame == 1 ")

        # if cWidgetPos == 0:
        #     printAutoInd(f, "nearestPrevFrameOnsetTime = Screen('Flip',{0},nextEvFlipReqTime,{1});", cWinStr, clearAfter)
        # else:
        #     printAutoInd(f, "nearestPrevFrameOnsetTime = Screen('Flip',{0},nextEvFlipReqTime,{1});", cWinStr, clearAfter)
        #
        # printAutoInd(f, "{0}({1}).onsetTime = nearestPrevFrameOnsetTime;", cWidgetName, cOpRowIdxStr)

        allWidgetCodes = genStimTriggers(cWidget, f, cLoopLevel, attributesSetDict, allWidgetCodes)
        allWidgetCodes = genUpdateWidgetDur(cWidget, f, attributesSetDict, allWidgetCodes, 'afVideoFipReqTime')

        # printAutoInd(f, "nextEvFlipReqTime = afVideoFipReqTime; % after the first flip, update nextEvFlipReqTime")
        # printAutoInd(f, "else ")
        # printAutoInd(f, "nearestPrevFrameOnsetTime = Screen('Flip', {0}, 0, {1}); %", cWinStr, clearAfter)
        # printAutoInd(f, "end \n")

        '''
        only for video related widget, the video texture need to be closed 
        '''
        # if bitGet(flipType, 0):
        #     # single video without dot motion
        #     if cVideoItemNums <= 1 and bitGet(flipType, 1) == 0:
        #         printAutoInd(f, "Screen('Close',{0}_tPtr);\n", cWidgetName)
        #     # single video with dot motion
        #     elif cVideoItemNums <= 1 and bitGet(flipType, 1):
        #         printAutoInd(f, "if {0}_beClosedMIdx", cWidgetName)
        #         printAutoInd(f, "Screen('Close',{0}_tPtr);", cWidgetName)
        #         printAutoInd(f, "end \n")
        #     # multiple videos
        #     elif cVideoItemNums > 1:
        #         printAutoInd(f, "Screen('Close',{0}_tPtrs({0}_beClosedMIdx));", cWidgetName)
        #
        # printAutoInd(f, "if isTerminateStimEvent")
        # printAutoInd(f, "nextEvFlipReqTime = 0;")
        # printAutoInd(f, "break;")
        # printAutoInd(f, "end")

        # print response check section
        # printAutoInd(f, "iFrame = iFrame + 1; ")
        # printAutoInd(f, "end % while\n")

        """
        # close opened movies
        """
        # if bitGet(flipType, 0):
        #     printAutoInd(cRespCodes, "% close the movie prts and visual textures")
        #     if cVideoItemNums <= 1:
        #         printAutoInd(cRespCodes, "Screen('CloseMovie', {0}_mPtr);", cWidgetName)
        #         # printAutoInd(cRespCodes, "Screen('Close',{0}_tPtr); % close the last video frame", cWidgetName)
        #     else:
        #         printAutoInd(cRespCodes, "Screen('CloseMovie', {0}_mPtrs);", cWidgetName)
        #         # printAutoInd(cRespCodes, "Screen('Close',TPtrs); % close the last video frame")
    else:
        """ 
        # for widgets that needs flipped one time
        """
        # if cWidgetPos == 0:
        #     # printAutoInd(f, "% for first event, flip immediately.. ")
        #     # f"{getWidgetName(cWidget.widget_id)}_onsetTime({cOpRowIdxStr})"
        #     printAutoInd(f, "{0}({1}).onsetTime = Screen('Flip',{2},nextEvFlipReqTime,{3}); %#ok<*STRNU>\n",
        #                  cWidgetName,
        #                  cOpRowIdxStr, cWinStr, clearAfter)
        # else:
        #     printAutoInd(f, "{0}({1}).onsetTime = Screen('Flip',{2},nextEvFlipReqTime,{3}); %#ok<*STRNU>\n",
        #                  cWidgetName,
        #                  cOpRowIdxStr, cWinStr, clearAfter)

    """
    # close all possible ima textures
    """
    cAfEndVideoFlipCodes = allWidgetCodes.get('codesJustBeRespCodes', [])
    cRespCodes.extend(cAfEndVideoFlipCodes)
    allWidgetCodes.update({'codesJustBeRespCodes': []})

    allWidgetCodes.update({f"{cWidget.widget_id}_cRespCodes": cRespCodes})

    return allWidgetCodes


def flipAudio(cWidget, f, cLoopLevel, attributesSetDict, iSlave=1):
    # for sound widget only, not for slider that contains sound item
    global historyPropDict, isDummyPrint
    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num

    # get screen cWinIdx and cWinStr: winIdx(index)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    clearAfter = getClearAfterInfo(cWidget, attributesSetDict)

    # isSyncToVbl = True
    # haveSound = isContainSound(cWidget)
    # isSlider = Func.isWidgetType(cWidget.widget_id, Info.COMBO)

    # 1) check the sound dev parameter:
    cSoundDevName, isRef = getRefValue(cWidget, cWidget.getSoundDeviceName(), attributesSetDict)
    cSoundIdxStr = f"{outputDevNameIdxDict.get(cSoundDevName)}({iSlave})"

    # 2) check the repetitions parameter:
    repetitionsStr, isRef = getRefValue(cWidget, cWidget.getRepetitions(), attributesSetDict)

    # 3) get the isSyncToVbl parameter for sound widget only:
    #    sound in the slider will force tobe sync to the VBL
    # if Func.isWidgetType(cWidget.widget_id, Info.SOUND):
    isSyncToVbl = cWidget.getSyncToVbl()

    # if getWidgetPos(cWidget.widget_id) > 0 and not(isSubWidgetOfIfOrSwitch(cWidget.widget_id)):
    #     # Step 2: print out help info for the current widget
    #     printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    #     printAutoInd(f, '%loop:{0}, event{1}: {2}', cLoopLevel, getWidgetEventPos(cWidget.widget_id) + 1,
    #                  getWidgetName(cWidget.widget_id))
    #     printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    # if isSyncToVbl:
    #     # Flip the Screen
    #     printAutoInd(f, "% sync to the vertical blank of screen:{0}", cWidget.getScreenName())
    #     if getWidgetPos(cWidget.widget_id) == 0:
    #         printAutoInd(f, "% for first event, play the audio at the immediately VBL .. ")
    #         printAutoInd(f, "predictedVisOnset = PredictVisualOnsetForTime({0}, 0);", cWinStr)
    #
    #         printAutoInd(f, "PsychPortAudio('Start', {0}, {1}, predictedVisOnset, 0); %\n", cSoundIdxStr,
    #                      repetitionsStr)
    #         printAutoInd(f, "{0}({1}).onsetTime = Screen('Flip', {2}, {3}); %\n", getWidgetName(cWidget.widget_id),
    #                      cOpRowIdxStr, cWinStr, clearAfter)
    #     else:
    #         printAutoInd(f, "predictedVisOnset = PredictVisualOnsetForTime({0}, nextEvFlipReqTime);", cWinStr)
    #         printAutoInd(f, "% schedule start of audio at exactly the predicted time caused by the next flip")
    #         printAutoInd(f, "PsychPortAudio('Start', {0}, {1}, predictedVisOnset, 0); %\n",
    #                      cSoundIdxStr, repetitionsStr)
    #         printAutoInd(f, "{0}({1}).onsetTime = Screen('Flip',{2},nextEvFlipReqTime, {3}); %#ok<*STRNU>\n",
    #                      getWidgetName(cWidget.widget_id), cOpRowIdxStr, cWinStr, clearAfter)
    # else:
    #     if getWidgetPos(cWidget.widget_id) == 0:
    #         printAutoInd(f, "% for first event, play the audio immediately.. ")
    #         printAutoInd(f, "{0}({1}).onsetTime = PsychPortAudio('Start', {2}, {3}, 0, 1); % wait for start and get the real start time\n",
    #                      getWidgetName(cWidget.widget_id), cOpRowIdxStr, cSoundIdxStr, repetitionsStr)
    #     else:
    #         printAutoInd(f, "% for multiple screens, use the maximum of the predicted onset time")
    #         printAutoInd(f,
    #                      "{0}({1}).onsetTime = PsychPortAudio('Start', {2}, {3}, max(cDurs + lastScrOnsetTime), 1); % % wait for start and get the real start time\n",
    #                      getWidgetName(cWidget.widget_id), cOpRowIdxStr, cSoundIdxStr, repetitionsStr)


def genCheckResponse(cWidget, f, cLoopLevel, attributesSetDict, allWidgetCodes):
    global outputDevNameIdxDict, historyPropDict, isDummyPrint, queueDevIdxValueStr

    # for video related widget, will do this during the flip loop
    # if isVideoRelatedWidget(cWidget):
    #     return allWidgetCodes

    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"
    cWidgetName = getWidgetName(cWidget.widget_id)

    cOutDeviceDict = historyPropDict.get('cOutDevices', {})
    historyPropDict.update({'cOutDevices': {}})

    outDevCountsDict = getOutputDevCountsDict()

    # get screen cWinIdx and cWinStr: winIds(idx)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    cInputDevices = cWidget.getInputDevice()

    # -------------------------------------------------------------------------------
    # Step 1: check parameters that should not be a citation value
    # -------------------------------------------------------------------------------
    nKbs = 0
    nMouses = 0

    for key, value in cInputDevices.items():
        shouldNotBeCitationCheck('RT Window', value['RT Window'])
        shouldNotBeCitationCheck('End Action', value['End Action'])

        shouldNotBeEmptyCheck(f"the allow able keys in the event {cWidgetName}:{value['Device Name']}", value['Allowable'])

        # check if the end action and rt window parameters are compatible
        if value.get('End Action').startswith('Terminate'):
            if value.get('RT Window') != '(Same as duration)':
                throwCompileErrorInfo(
                    f"{cWidgetName}:{value.get('Device Name')} when 'End Action' is {value.get('End Action')}, 'RT Window' should be '(Same as duration)'")

        if value['Device Type'] == Info.DEV_KEYBOARD:
            nKbs += 1

        if value['Device Type'] == Info.DEV_MOUSE:
            nMouses += 1

        value.update({'Widget Name': cWidgetName})
        cInputDevices.update({key: value})

    # under windows: all keyboards and mouses will be treated as a single device
    if Info.PLATFORM == 'windows':
        if nKbs > 1 or nMouses > 1:
            tobeShowStr = 'Input devices: \n For windows, specify multiple kbs or mice separately are not allowed!\n you can specify only one keyboard and/or one mouse here!'
            throwCompileErrorInfo(f"{cWidgetName}: {tobeShowStr}")
    #
    if len(cInputDevices) > 0:

        iRespDev = 1
        # printAutoInd(f, "% make respDev structure for the event {0}", cWidgetName)
        for cInputDev, cProperties in cInputDevices.items():
            # get allowable keys
            allowableKeysStr, isRefValue, cRefValueSet = getRefValueSet(cWidget, cProperties.get('Allowable'),
                                                                        attributesSetDict)
            allowableKeysStr = parseRespKeyCodesStr(allowableKeysStr, isRefValue, cProperties['Device Type'])

            # update the allowableKeysList
            if cProperties['Device Type'] != Info.DEV_RESPONSE_BOX:

                if isRefValue:
                    for allowableKey in cRefValueSet:
                        updateEnableKbKeysList(allowableKey)
                else:
                    updateEnableKbKeysList(allowableKeysStr)

            # get corRespCode
            corRespStr, isRefValue, cRefValueSet = getRefValueSet(cWidget, cProperties['Correct'], attributesSetDict)
            corRespStr = parseRespKeyCodesStr(corRespStr, isRefValue, cProperties['Device Type'])

            # update the allowableKeysList for Correct keys
            if cProperties['Device Type'] != Info.DEV_RESPONSE_BOX:

                if isRefValue:
                    for allowableKey in cRefValueSet:
                        updateEnableKbKeysList(allowableKey)
                else:
                    updateEnableKbKeysList(allowableKeysStr)




            if not corRespStr:
                corRespStr = addSquBrackets(corRespStr)

            if corRespStr.find(',') == -1:
                corRespStr = removeSquBrackets(corRespStr)

            # get response time window
            rtWindowStr = parseRTWindowStr(cProperties['RT Window'])

            # get end action
            endActionStr = parseEndActionStr(cProperties['End Action'])

            # get Right
            rightStr = dataStrConvert(*getRefValue(cWidget, cProperties['Right'], attributesSetDict), True)

            # get Wrong
            wrongStr = dataStrConvert(*getRefValue(cWidget, cProperties['Wrong'], attributesSetDict), True)

            # get No Resp
            noRespStr = dataStrConvert(*getRefValue(cWidget, cProperties['No Resp'], attributesSetDict), True)

            # get start rect
            startRectStr = parseRectStr(*getRefValue(cWidget, cProperties['Start'], attributesSetDict))

            # get end rect
            endRectStr = parseRectStr(*getRefValue(cWidget, cProperties['End'], attributesSetDict))

            # get mean rect
            meanRectStr = parseRectStr(*getRefValue(cWidget, cProperties['Mean'], attributesSetDict))

            # get os oval
            isOvalStr = parseBooleanStr(cProperties['Is Oval'])

            # get resp output dev name
            respOutDevNameStr, isRefValue = getRefValue(cWidget, cProperties['Output Device'], attributesSetDict)

            # devIndexesVarName = None
            # get dev type and devIndexesVarName
            cInputDevIndexValueStr, cIsQueue, cDevType = inputDevNameIdxDict[cProperties['Device Name']]

            # if the response code send port is a parallel
            if respOutDevNameStr == '' or respOutDevNameStr == 'none':
                needTobeRetStr = 'false'
                respCodeDevIdxStr = '0'
                respCodeDevTypeStr = '[]'
            else:
                # cOutDeviceDict[cDevName] = [devType, pulseDur, devPort]
                respCodeDevIdxStr = cOutDeviceDict[respOutDevNameStr][2]

                respCodeDevTypeStr = cOutDeviceDict[respOutDevNameStr][0]

                if cOutDeviceDict[respOutDevNameStr][0] == '1':
                    needTobeRetStr = 'true'
                else:
                    needTobeRetStr = 'false'

            beUpdatedVarHandleStr = f"{cWidgetName}({cOpRowIdxStr})"
            # startTimeStr = f"lastScrOnsetTime({cWinIdx})"

            # eye action 82 should not be "Terminate till release"
            if cDevType == 82 and endActionStr == "2":
                endActionStr = "1"

            # printAutoInd(f,
            #              "makeRespStruct_APL({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18});",
            #              beUpdatedVarHandleStr,  # 0 beUpdatedVarHandle
            #              allowableKeysStr,       # 1 allowAble
            #              corRespStr,             # 2 corResp
            #              rtWindowStr,            # 3 rtWindow -1 and -2 for end of duration and timeline
            #              endActionStr,           # 4 endAction
            #              cDevType,               # 5 type
            #              cInputDevIndexValueStr, # 6 index
            #              cIsQueue,               # 7 isQueue
            #              # startTimeStr,         # 8 startTime not needed anymore
            #              '1',                    # 8 checkStatus
            #              needTobeRetStr,         # 9 needTobeReset
            #              rightStr,               # 10 right
            #              wrongStr,               # 11 wrong
            #              noRespStr,              # 12 noResp
            #              respCodeDevTypeStr,     # 13 respCodeDevType
            #              respCodeDevIdxStr,      # 14 respCodeDevIdx
            #              startRectStr,           # 15 start
            #              endRectStr,             # 16 end
            #              meanRectStr,            # 17 mean
            #              isOvalStr,              # 18 isOval
            #              )

            iRespDev += 1

        # if len(queueDevIdxValueStr) > 0:
        #     printAutoInd(f, "isQueueStart = switchQueue_APL({0}, isQueueStart);", queueDevIdxValueStr)

        # printAutoInd(f, "\n")
    else:
        # if len(queueDevIdxValueStr) > 0:
        #     printAutoInd(f, "isQueueStart = switchQueue_APL({0}, isQueueStart);", queueDevIdxValueStr)
        printAutoInd(f," ")
    # if not getFlipType(cWidget):
    #     printAutoInd(f, "[~,~,nextEvFlipReqTime] = checkResp_SendRespTrig_APL(cDurs({0}), nextEvFlipReqTime, false);\n",
    #                  cWinIdx)
    # printAutoInd(f, "if isTerminateStimEvent")
    # printAutoInd(f, "nextEvFlipReqTime = 0;")
    # printAutoInd(f, "end ")
    # printAutoInd(f, "%=================================================\\\n")

    shortPulseDurParallelsDict = outPutTriggerCheck(cWidget)

    return allWidgetCodes

###主要组件输出函数
def genStimWidgetAllCodes(cWidget, attributesSetDict, cLoopLevel, allWidgetCodes):
    cStimCodes = list()
    cFlipCodes = list()
    cStimTriggerCodes = list()
    cUpdateDurCodes = list()
    cRespCodes = list()

    if cWidget is None:
        return allWidgetCodes
    # print comments to indicate the current frame order
    cWidgetName = getWidgetName(cWidget.widget_id)
    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    cWidgetType = getWidgetType(cWidget)

    if isSubWidgetOfIfOrSwitch(cWidget) is False:
        #  update the attributesSetDict only for the main widgets
        cWidgetAddedAttrsList = ['rt', 'resp', 'acc', 'onsetTime', 'respOnsetTime']
        for cAddedAttr in cWidgetAddedAttrsList:
            attributesSetDict.update({
                f"{cWidgetName}.{cAddedAttr}":
                    [cLoopLevel, f"{cWidgetName}({cOpRowIdxStr}).{cAddedAttr}",
                     {f"{cWidgetName}({cOpRowIdxStr}).{cAddedAttr}"}]
            })

    # Step 1: generate codes to draw stim
    if Info.TEXT == cWidgetType:
        drawTextWidget(cWidget, cStimCodes, attributesSetDict, cLoopLevel)
    elif Info.IMAGE == cWidgetType:
        allWidgetCodes, *_ = drawImageWidget(cWidget, cStimCodes, attributesSetDict, cLoopLevel, allWidgetCodes)
    elif Info.SOUND == cWidgetType:
        allWidgetCodes = drawSoundWidget(cWidget, cStimCodes, attributesSetDict, cLoopLevel, allWidgetCodes)
    elif Info.COMBO == cWidgetType:
        allWidgetCodes = drawSliderWidget(cWidget, cStimCodes, attributesSetDict, cLoopLevel, allWidgetCodes)
    elif Info.VIDEO == cWidgetType:
        allWidgetCodes, _ = drawVideoWidget(cWidget, cStimCodes, attributesSetDict, cLoopLevel, allWidgetCodes)

    elif Info.IF == cWidgetType:
        falseWidget = cWidget.getFalseWidget()
        allWidgetCodes = genStimWidgetAllCodes(falseWidget, attributesSetDict, cLoopLevel, allWidgetCodes)

        trueWidget = cWidget.getTrueWidget()
        allWidgetCodes = genStimWidgetAllCodes(trueWidget, attributesSetDict, cLoopLevel, allWidgetCodes)

        # concatenate codes for IF widget
        allWidgetCodes = makeCodes4IfWidget(cWidget, attributesSetDict, cLoopLevel, allWidgetCodes)

        return allWidgetCodes

    elif Info.SWITCH == cWidgetType:
        caseWidgets = cWidget.getCases()

        for cCase in caseWidgets:
            cSubWid = cCase['Sub Wid']

            if cSubWid:
                allWidgetCodes = genStimWidgetAllCodes(Info.WID_WIDGET[cSubWid], attributesSetDict, cLoopLevel,
                                                       allWidgetCodes)

        # concatenate codes for switch widget
        allWidgetCodes = makeCodes4SwitchWidget(cWidget, attributesSetDict, cLoopLevel, allWidgetCodes)

        return allWidgetCodes

    # STEP 2: generate flip code
    if Info.SOUND == cWidgetType:
        flipAudio(cWidget, cFlipCodes, cLoopLevel, attributesSetDict)
    else:
        flipScreen(cWidget, cFlipCodes, cLoopLevel, attributesSetDict, allWidgetCodes)

    # for video related widget, will run step 3-5 (do nothing) in dummy as we already did this in Step 2:
    # if is a video related widget, will do this within flip loop
    if not getFlipType(cWidget):
        # step 3: generate sending trigger codes
        allWidgetCodes = genStimTriggers(cWidget, cStimTriggerCodes, cLoopLevel, attributesSetDict, allWidgetCodes)

        # step 4: generate updating cDurs codes
        allWidgetCodes = genUpdateWidgetDur(cWidget, cUpdateDurCodes, attributesSetDict, allWidgetCodes)

        # step 5: generate response checking codes
        allWidgetCodes = genCheckResponse(cWidget, cRespCodes, cLoopLevel, attributesSetDict, allWidgetCodes)

    # save all codes for the current widget
    cStimExistCodes: list = allWidgetCodes.get(f"{cWidget.widget_id}_cStimCodes", [])
    cStimExistCodes.extend(cStimCodes)
    allWidgetCodes.update({f"{cWidget.widget_id}_cStimCodes": cStimExistCodes})

    cFlipExistCodes: list = allWidgetCodes.get(f"{cWidget.widget_id}_cFlipCodes", [])
    cFlipExistCodes.extend(cFlipCodes)
    allWidgetCodes.update({f"{cWidget.widget_id}_cFlipCodes": cFlipExistCodes})

    cStimTriggerExistCodes: list = allWidgetCodes.get(f"{cWidget.widget_id}_cStimTriggerCodes", [])
    cStimTriggerExistCodes.extend(cStimTriggerCodes)
    allWidgetCodes.update({f"{cWidget.widget_id}_cStimTriggerCodes": cStimTriggerExistCodes})

    cUpdateDurExistCodes: list = allWidgetCodes.get(f"{cWidget.widget_id}_cUpdateDurCodes", [])
    cUpdateDurExistCodes.extend(cUpdateDurCodes)
    allWidgetCodes.update({f"{cWidget.widget_id}_cUpdateDurCodes": cUpdateDurExistCodes})

    cRespExistCodes: list = allWidgetCodes.get(f"{cWidget.widget_id}_cRespCodes", [])
    cRespExistCodes.extend(cRespCodes)
    allWidgetCodes.update({f"{cWidget.widget_id}_cRespCodes": cRespExistCodes})

    return allWidgetCodes


def makeCodes4SwitchWidget(cWidget, attributesSetDict, cLoopLevel, allWidgetCodes):
    if getWidgetType(cWidget) == Info.SWITCH:
        transformStrDict = {'=': '==', '≠': '~=', '≥': '>=', '≤': '<='}
        codeTypesList = ['_cStimCodes', '_cFlipCodes', '_cStimTriggerCodes', '_cUpdateDurCodes', '_cRespCodes']

        switchExp = cWidget.getSwitch()
        switchExp, *_ = getValueInContainRefExp(cWidget, switchExp, attributesSetDict, False, transformStrDict)

        # cases: list = [{'Case Value': '',
        #  'Id Pool': {'Image': 'Image.0', 'Video': '', 'Text': '', 'Sound': '', 'Slider': ''},
        #  'Sub Wid': 'Image.0', 'Stim Type': 'Image', 'Event Name': 'U_Image_6574'},]
        cases = cWidget.getCases()
        otherwiseExp = cases[-1]

        cases = cases[0:-1]

        for cCase in cases:
            if cCase['Case Value']:
                cCaseValueExp, *_ = getValueInContainRefExp(cWidget, cCase['Case Value'], attributesSetDict, False, transformStrDict)
                cCase.update({'Case Value': cCaseValueExp})

        for cCodeType in codeTypesList:
            cTypeCodes = list()

            printAutoInd(cTypeCodes, "switch {0}", switchExp)

            for cCase in cases:
                printAutoInd(cTypeCodes, "case {0}", cCase['Case Value'])

                if cCase['Sub Wid']:
                    cTypeCodes.extend(allWidgetCodes[f"{cCase['Sub Wid']}{cCodeType}"])
                else:
                    printAutoInd(cTypeCodes, "% do nothing")

            if otherwiseExp['Sub Wid']:
                printAutoInd(cTypeCodes, "otherwise")
                cTypeCodes.extend(allWidgetCodes[f"{otherwiseExp['Sub Wid']}{cCodeType}"])

            printAutoInd(cTypeCodes, "end%switch ")

            allWidgetCodes.update({f"{cWidget.widget_id}{cCodeType}": cTypeCodes})

    return allWidgetCodes


def makeCodes4IfWidget(cWidget, attributesSetDict, cLoopLevel, allWidgetCodes):
    if getWidgetType(cWidget) == Info.IF:
        transformStrDict = {'=': '==', '≠': '~=', '≥': '>=', '≤': '<='}
        condStr = cWidget.getCondition()
        condStr, *_ = getValueInContainRefExp(cWidget, condStr, attributesSetDict, False, transformStrDict)

        codeTypesList = ['_cStimCodes', '_cFlipCodes', '_cStimTriggerCodes', '_cUpdateDurCodes', '_cRespCodes']

        trueWidget = cWidget.getTrueWidget()
        falseWidget = cWidget.getFalseWidget()

        # if getWidgetPos(cWidget.widget_id) > 0 and not (isSubWidgetOfIfOrSwitch(cWidget.widget_id)):
        # generate Event Header

        # cHeaderList = list()
        # printAutoInd(cHeaderList, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        # printAutoInd(cHeaderList, '%loop:{0}, event{1}: {2}', cLoopLevel, getWidgetEventPos(cWidget.widget_id) + 1,
        #              getWidgetName(cWidget.widget_id))
        # printAutoInd(cHeaderList, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

        for cCodeType in codeTypesList:
            cTypeCodes = list()

            # if getWidgetPos(cWidget.widget_id) == 0 and cCodeType == '_cStimCodes':
            # cTypeCodes.extend(cHeaderList)

            # if getWidgetPos(cWidget.widget_id) > 0 and cCodeType == '_cFlipCodes':
            # cTypeCodes.extend(cHeaderList)

            cTypeCodes.extend([f"% {getWidgetName(cWidget.widget_id)}{cCodeType}"])

            trueWidgetCodesList = list()
            falseWidgetCodesList = list()

            if trueWidget:
                trueWidgetCodesList = allWidgetCodes[f"{trueWidget.widget_id}{cCodeType}"]

            if falseWidget:
                falseWidgetCodesList = allWidgetCodes[f"{falseWidget.widget_id}{cCodeType}"]

            if len(trueWidgetCodesList) > 0:
                printAutoInd(cTypeCodes, "if {0}", condStr)
                cTypeCodes.extend(trueWidgetCodesList)

                if len(falseWidgetCodesList) > 0:
                    printAutoInd(cTypeCodes, "else")
            else:
                if len(falseWidgetCodesList) > 0:
                    printAutoInd(cTypeCodes, "if ~{0}", condStr)

            if len(falseWidgetCodesList) > 0:
                cTypeCodes.extend(falseWidgetCodesList)

            if len(trueWidgetCodesList) + len(falseWidgetCodesList) > 0:
                printAutoInd(cTypeCodes, "end ")

            allWidgetCodes.update({f"{cWidget.widget_id}{cCodeType}": cTypeCodes})

    return allWidgetCodes


def printGeneratedCodes(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes):
    # print comments to indicate the current frame order
    cHeaderList = list()
    # printAutoInd(cHeaderList, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # printAutoInd(cHeaderList, '%loop:{0}, event{1}: {2}', cLoopLevel, getWidgetEventPos(cWidget.widget_id) + 1,
    #              getWidgetName(cWidget.widget_id))
    # printAutoInd(cHeaderList, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # ====================
    # PRINT ALL CODES
    # ===================
    preStimWId = getPreStimWID(cWidget.widget_id)

    printPreRespCodesFirst = False
    transformStrDict = {'=': '==', '≠': '~=', '≥': '>=', '≤': '<='}

    if getWidgetType(cWidget) == Info.SWITCH:
        # switch expression
        _, _, referObNameList = getValueInContainRefExp(cWidget, cWidget.getSwitch(), attributesSetDict, False, transformStrDict)

        # case values
        for cCaseDict in cWidget.getCases():
            cCaseValueStr = cCaseDict['Case Value']
            if len(cCaseValueStr) > 0:
                _, _, cValueReferObNameList = getValueInContainRefExp(cWidget, cCaseValueStr, attributesSetDict, False, transformStrDict)
                referObNameList.extend(cValueReferObNameList)

        if preStimWId and getWidgetName(preStimWId) in referObNameList:
            printPreRespCodesFirst = True

    elif getWidgetType(cWidget) == Info.IF:
        condStr = cWidget.getCondition()

        condStr, haveRef, referObNameList = getValueInContainRefExp(cWidget, condStr, attributesSetDict, False, transformStrDict)

        if preStimWId and getWidgetName(preStimWId) in referObNameList:
            printPreRespCodesFirst = True

    # todo to be continued ...

    if getWidgetPos(cWidget.widget_id) == 0:
        printPreRespCodesFirst = True

    if printPreRespCodesFirst or len(allWidgetCodes.get(f"{preStimWId}_cRespCodes", [])) == 0:
        # draw previous widget's resp code first
        # step 2: print response codes of the previous widget if possible
        printInAllWidgetCodesByKey(f, allWidgetCodes, f"{preStimWId}_cRespCodes")

        printOutList(f, cHeaderList)
        # step 1: print stim codes of the current widget
        printInAllWidgetCodesByKey(f, allWidgetCodes, f"{cWidget.widget_id}_cStimCodes")
    else:
        # step 1: print stim codes of the current widget
        printInAllWidgetCodesByKey(f, allWidgetCodes, f"{cWidget.widget_id}_cStimCodes")

        if preStimWId:
            # step 2: print response codes of the previous widget if possible
            printInAllWidgetCodesByKey(f, allWidgetCodes, f"{preStimWId}_cRespCodes")

        printOutList(f, cHeaderList)

    # step 3: print flip codes of the current widget
    printInAllWidgetCodesByKey(f, allWidgetCodes, f"{cWidget.widget_id}_cFlipCodes")
    # step 4: print stim trigger codes of the current widget if possible
    printInAllWidgetCodesByKey(f, allWidgetCodes, f"{cWidget.widget_id}_cStimTriggerCodes")
    # step 5: print stim update duration codes of the current widget if possible
    printInAllWidgetCodesByKey(f, allWidgetCodes, f"{cWidget.widget_id}_cUpdateDurCodes")

    #  if the last stim widget print the resp codes here
    if isLastStimWidgetInTL(cWidget.widget_id):
        printInAllWidgetCodesByKey(f, allWidgetCodes, f"{cWidget.widget_id}_cRespCodes")

    return allWidgetCodes


def printStimWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes):
    # step 1: generate all codes (stim, flip ,send stim trigger, update cDurs, response check)
    allWidgetCodes = genStimWidgetAllCodes(cWidget, attributesSetDict, cLoopLevel, allWidgetCodes)

    # step 2: print out the generated codes
    allWidgetCodes = printGeneratedCodes(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes)

    return allWidgetCodes


def genUpdateWidgetDur(cWidget, f, attributesSetDict, allWidgetCodes, nextEventFlipReqTimeStr='nextEvFlipReqTime'):
    global outputDevNameIdxDict, historyPropDict

    # get screen index
    _, cWinIdx, _ = getScreenInfo(cWidget, attributesSetDict)

    # Step 1: get the current screen duration that determined by the next flip
    # after drawing the next widget's stimuli, get the duration first
    durStr, isRefValue, cRefValueSet = getRefValueSet(cWidget, cWidget.getDuration(), attributesSetDict)
    durStr = parseDurationStr(durStr)

    # updated the screen flip times in matlab
    # printAutoInd(f, "%%%")
    # printAutoInd(f, "% get cDur and the required flip time of the next event")
    # printAutoInd(f, "%%%")
    # if Func.isWidgetType(cWidget.widget_id, Info.SOUND):
    #     if re.fullmatch(r"\d+,\d+", durStr):
    #         printAutoInd(f, "cDurs(:)          = getDurValue_APL([{0}],winIFIs({1}), true);", durStr, cWinIdx)
    #     else:
    #         printAutoInd(f, "cDurs(:)          = getDurValue_APL({0},winIFIs({1}), true);", durStr, cWinIdx)
    # else:
    #     if re.fullmatch(r"\d+,\d+", durStr):
    #         printAutoInd(f, "cDurs({0})          = getDurValue_APL([{1}],winIFIs({0}));", cWinIdx, durStr)
    #     else:
    #         printAutoInd(f, "cDurs({0})          = getDurValue_APL({1},winIFIs({0}));", cWinIdx, durStr)

    # printAutoInd(f, "(not the real flip time) ")
    # printAutoInd(f, "{0} = cDurs({1}) + lastScrOnsetTime({1}) - flipComShiftDur({1}); "
    #                 "% get the required time of the  Flip for the next event \n",
    #              nextEventFlipReqTimeStr, cWinIdx)

    return allWidgetCodes  # O for successful


def genStimTriggers(cWidget, f, cLoopLevel, attributesSetDict, allWidgetCodes):
    global outputDevNameIdxDict, historyPropDict

    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"
    cWidgetName = getWidgetName(cWidget.widget_id)
    cWidgetType = getWidgetType(cWidget)

    # get screen index
    _, cWinIdx, _ = getScreenInfo(cWidget, attributesSetDict)

    # ---------------------------------------------------------------------------------------
    # Step 1: print out previous widget's codes that suppose to be print just after the Flip
    # ----------------------------------------------------------------------------------------
    for cRowStr in allWidgetCodes['codesAfFlip']:
        printAutoInd(f, cRowStr)
    # clear out the print buffer
    allWidgetCodes.update({'codesAfFlip': []})

    '''
    # ------------------------------------------------------------
    # Step 2: send output triggers and messages
    # ------------------------------------------------------------
    '''
    output_device = cWidget.getOutputDevice()
    if len(output_device) > 0:
        printAutoInd(f, "% -- send output trigger and msg: --/")

    # initializing the outDevices that could be used to store the outDev info
    cOutDeviceDict = dict()

    for device, properties in output_device.items():
        msgValue = dataStrConvert(*getRefValue(cWidget, properties['Value Or Msg'], attributesSetDict), True)
        pulseDur = dataStrConvert(*getRefValue(cWidget, properties['Pulse Duration'], attributesSetDict), False)

        cDevName = properties.get("Device Name", "")
        devType = properties.get("Device Type", "")

        if devType == Info.DEV_PARALLEL_PORT:
            # currently only ppl need to be reset to zero
            cOutDeviceDict[cDevName] = ['1', pulseDur, outputDevNameIdxDict.get(cDevName)]

            printAutoInd(f, "parWrite_APL({0},{1});", outputDevNameIdxDict.get(cDevName), msgValue)

        elif devType == Info.DEV_NETWORK_PORT:
            printAutoInd(f, "pnet({0},'write',{1});", outputDevNameIdxDict.get(cDevName), msgValue)
            cOutDeviceDict[cDevName] = ['2', pulseDur, outputDevNameIdxDict.get(cDevName)]

        elif devType == Info.DEV_SERIAL_PORT:
            printAutoInd(f, "[ign, when] = IOPort('Write', {0}, {1});", outputDevNameIdxDict.get(cDevName), msgValue)
            cOutDeviceDict[cDevName] = ['3', pulseDur, outputDevNameIdxDict.get(cDevName)]

    historyPropDict.update({'cOutDevices': cOutDeviceDict})

    if len(output_device) > 0:
        printAutoInd(f, "{0}({1}).msgEndTime = GetSecs;", cWidgetName, cOpRowIdxStr)
        printAutoInd(f, "% ----------------------------------\\\n")

    # print out event onset marker for eyelink
    if allWidgetCodes.get('isEyeLinkStartRecord'):
        printAutoInd(f, "Eyelink('Message', '{0}_onsetTime');", cWidgetName)

    # updated the screen flip times in matlab
    if Info.SOUND == cWidgetType:
        # printAutoInd(f, "% for event type of sound, make it to all lastScrOnsetime")
        # printAutoInd(f, "lastScrOnsetTime(:) = {0}({1}).onsetTime; % temp store the last screen onset time\n",
        #              getWidgetName(cWidget.widget_id),
        #              cOpRowIdxStr)
        printAutoInd(f," ")
    else:
        # printAutoInd(f, "lastScrOnsetTime({0}) = {1}({2}).onsetTime; % temp store the last screen onset time\n",
        #              cWinIdx,
        #              getWidgetName(cWidget.widget_id),
        #              cOpRowIdxStr)
        printAutoInd(f," ")
    return allWidgetCodes


def printTimelineWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes) -> dict:
    global cInfoDict, isDummyPrint
    #得到一个timeline中所有的widget的widget_id的list，按顺序放置
    cTimelineWidgetIds = getWidgetIDInTimeline(cWidget.widget_id)

    if Info.IMAGE_LOAD_MODE == "before_trial":
        printAutoInd(f, " ")

    for cWidgetId in cTimelineWidgetIds:
        cWidget = Info.WID_WIDGET[cWidgetId]

        # for dummyPrint get the last widget id and loopNum
        if isDummyPrint:
            cInfoDict.update({'lastWidgetId': cWidgetId})

        cWidgetType = getWidgetType(cWidget)

        if Info.LOOP == cWidgetType:
            allWidgetCodes = printCycleWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes)
        elif cWidgetType in [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO, Info.IF, Info.SWITCH]:
            allWidgetCodes = printStimWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes)
        elif Info.DC == cWidgetType:
            allWidgetCodes = printETDcCorrectWidget(cWidget, f, allWidgetCodes)
        elif Info.CALIBRATION == cWidgetType:
            allWidgetCodes = printETCalibWidget(cWidget, f, allWidgetCodes)
        elif Info.STARTR == cWidgetType:
            allWidgetCodes = printETStartRWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes)
        elif Info.ENDR == cWidgetType:
            allWidgetCodes = printETEndRWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes)
        elif Info.LOG == cWidgetType:
            allWidgetCodes = printETLogWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes)
        elif Info.QUEST_UPDATE == cWidgetType:
            allWidgetCodes = printQuestUpdateWidget(cWidget, f, attributesSetDict, allWidgetCodes, cLoopLevel)
    return allWidgetCodes


def printETLogWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes):
    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    cProperties = Func.getWidgetProperties(cWidget.widget_id)

    # print previous widget's response code
    preStimWid = getPreStimWID(cWidget.widget_id)
    allWidgetCodes = printInAllWidgetCodesByKey(f, allWidgetCodes, f'{preStimWid}_respCodes')

    printAutoInd(f, '%eyetracker: logging variables')

    shouldNotBeCitationCheck('Pause between messages', cWidget.getPauseBetweenMessages())

    usedAttributesList = cProperties.get('Used Variables', [])

    printAutoInd(f, "Eyelink('Message', '!V TRIAL_VAR index %s', {0});", cOpRowIdxStr)

    if len(usedAttributesList) > 0:

        varValueStrList = []

        for varName in usedAttributesList:
            varValueStr, _ = getRefValue(cWidget, addSquBrackets(varName), attributesSetDict)
            varValueStrList.append(varValueStr)

        bePrintLogVarStr = "{" + "".join(f"'{varName}'," for varName in usedAttributesList)[0:-1] + "}"
        bePrintLogVarValueStr = "{" + "".join(f"{varName}," for varName in varValueStrList)[0:-1] + "}"

        printAutoInd(f, "logVarNames  = {0};", bePrintLogVarStr)
        printAutoInd(f, "logVarValues = {0};", bePrintLogVarValueStr)
        printAutoInd(f, "eyelinkLog(logVarNames, logVarValues, {0});", float(cWidget.getPauseBetweenMessages()) / 1000)
    '''
        to be continue ...
    '''
    printAutoInd(f, "Eyelink('Message', 'TRIAL_RESULT 0');\n\n")

    return allWidgetCodes


def printQuestUpdateWidget(cWidget, f, attributesSetDict, allWidgetCodes, cLoopLevel):
    global outputDevNameIdxDict
    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    cProperties = Func.getWidgetProperties(cWidget.widget_id)

    # print previous widget's response code
    preStimWid = getPreStimWID(cWidget.widget_id)
    allWidgetCodes = printInAllWidgetCodesByKey(f, allWidgetCodes, f'{preStimWid}_respCodes')

    shouldNotBeCitationCheck('Quest Name', cProperties['Quest Name'])

    cQuestName, isRef = getRefValue(cWidget, cProperties['Quest Name'], attributesSetDict)

    respVarStr, isRef = getRefValue(cWidget, cProperties['Is Correct'], attributesSetDict)

    respVarStr = parseBooleanStr(respVarStr, isRef)

    cQuestIdx = outputDevNameIdxDict.get('quest-' + cQuestName, 'random selected Quest')

    printAutoInd(f, "% update {0}: questStructs({1})", cQuestName, cQuestIdx)

    if cQuestName == "quest_rand":
        # define the cRandQuestIdx at where we used the cValue
        # printAutoInd(f, "cUsedQuestId_APL;")
        printAutoInd(f, "cUsedQuestId_APL.updateQuestValue(cUsedQuestId_APL.cValue, {0}, opRowIdx); % update and get the next cValue",
                     respVarStr)

    else:
        printAutoInd(f, "questStructs({0}).updateQuestValue(questStructs({0}).cValue, {1}, opRowIdx);  % update and get the next cValue",
                     cQuestIdx, respVarStr)


    printAutoInd(f, "\n")

    return allWidgetCodes


def printETDcCorrectWidget(cWidget, f, allWidgetCodes):
    # cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    # cProperties = Func.getWidgetProperties(cWidget.widget_id)
    allWidgetCodes.update({"isEyeLinkStartRecord": True})
    # print previous widget's response code
    preStimWid = getPreStimWID(cWidget.widget_id)
    allWidgetCodes = printInAllWidgetCodesByKey(f, allWidgetCodes, f'{preStimWid}_respCodes')

    nextWidgetId = getNextWID(cWidget.widget_id)

    printAutoInd(f, "EyelinkDoDriftCorrection(el);% do drift correction")

    if nextWidgetId and Func.isWidgetType(nextWidgetId, Info.STARTR):
        printAutoInd(f, "% start recording eye position (preceded by a short pause so that")
        printAutoInd(f, "% the tracker can finish the mode transition)")
        printAutoInd(f, "WaitSecs(0.05);")
    # printAutoInd(f, "Eyelink('Command', 'set_idle_mode');")
    printAutoInd(f, " ")

    return allWidgetCodes


def printETCalibWidget(cWidget, f, allWidgetCodes):
    # cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    # cProperties = Func.getWidgetProperties(cWidget.widget_id)

    allWidgetCodes.update({"isEyeLinkStartRecord": True})
    # print previous widget's response code
    preStimWid = getPreStimWID(cWidget.widget_id)
    # if preStimWid:
    allWidgetCodes = printInAllWidgetCodesByKey(f, allWidgetCodes, f'{preStimWid}_respCodes')

    printAutoInd(f, "EyelinkDoTrackerSetup(el); % eyelink setup: adjust the camera,calibration and validation")

    return allWidgetCodes


def printETStartRWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes):
    # cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    # cProperties = Func.getWidgetProperties(cWidget.widget_id)

    allWidgetCodes.update({"isEyeLinkStartRecord": True})
    cCodesForResp = allWidgetCodes.get('respCodes', [])

    if len(cCodesForResp) > 0:
        haveRespCodes = True
    else:
        haveRespCodes = False

    cLoopStr = f"iLoop_{cLoopLevel}"

    cMessageStr = cWidget.getStatusMessage()

    if len(cMessageStr) == 0:
        cMessageStr = "''"

    printAutoInd(f, '%--- Eye tracker: start to record ---/')
    printAutoInd(f, "% Sending a 'TRIALID' message to mark the start of a trial in Data Viewer")
    if haveRespCodes:
        printAutoInd(f, "sendStartRecordComTime = GetSecs;")
    printAutoInd(f, "Eyelink('Message','TRIALID %d',{0});", cLoopStr)

    printAutoInd(f, "% This status message will be displayed at the bottom of the eyetracker display")
    printAutoInd(f, "Eyelink('Command','record_status_message \"TRIAL\" %d: %s',{0},{1});", cLoopStr, cMessageStr)
    printAutoInd(f, "Eyelink('StartRecording');")
    printAutoInd(f, '%-----------------------------------\\\n')

    # print previous widget's response code
    preStimWid = getPreStimWID(cWidget.widget_id)
    allWidgetCodes = printInAllWidgetCodesByKey(f, allWidgetCodes, f'{preStimWid}_respCodes')

    printAutoInd(f, "% record a few samples before we actually start displaying")
    printAutoInd(f, "% otherwise you may lose a few msec of data")

    if haveRespCodes:
        printAutoInd(f, "if GetSecs < sendStartRecordComTime + 0.1")
        printAutoInd(f, "WaitSecs('UntilTime', sendStartRecordComTime + 0.1);")
        printAutoInd(f, "end")
    else:
        printAutoInd(f, "WaitSecs(0.1);")

    printAutoInd(f, "% mark zero-plot time in data file")
    printAutoInd(f, "Eyelink('message', 'SYNCTIME');\n")

    return allWidgetCodes


def printETEndRWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes):
    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    cProperties = Func.getWidgetProperties(cWidget.widget_id)

    allWidgetCodes.update({"isEyeLinkStartRecord": False})

    # print previous widget's response code
    preStimWid = getPreStimWID(cWidget.widget_id)
    allWidgetCodes = printInAllWidgetCodesByKey(f, allWidgetCodes, f'{preStimWid}_respCodes')

    printAutoInd(f, '%- eyetracker: stoprecord ---/')
    printAutoInd(f, "Eyelink('StopRecording');")
    printAutoInd(f, '%----------------------------\\\n')

    return allWidgetCodes


def drawSliderWidget(cWidget, sliderStimCodes, attributesSetDict, cLoopLevel, allWidgetCodes):
    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint, haveGaborStim, haveSnowStim, haveDotMotion, haveArcStim

    cVSLCodes = allWidgetCodes.get('forVideoSliderLoopCodes', [])
    beClosedTxAFCycleList = allWidgetCodes.get(f"beClosedTextures_{cLoopLevel}", [])

    if Info.IMAGE_LOAD_MODE == "before_exp":
        bePrintLoopLevel = 1
        xedTxAFCycleWidgetFilenameList: list = allWidgetCodes.get(f"xedTxAFCycleWidgetFilenameList_{bePrintLoopLevel}", [])
    elif Info.IMAGE_LOAD_MODE == "before_trial":
        bePrintLoopLevel = cLoopLevel
        xedTxAFCycleWidgetFilenameList: list = allWidgetCodes.get(f"xedTxAFCycleWidgetFilenameList_{bePrintLoopLevel}", [])

    iVideoNum = 1

    cWidgetName = getWidgetName(cWidget.widget_id)
    cSliderProperties = Func.getWidgetProperties(cWidget.widget_id)
    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)
    # ------------------------------------------------
    # Step 2: draw eachItem
    # -------------------------------------------------
    cItems = cSliderProperties['Items']

    cCloseIdxesStr = ""

    cCloseImaWidgetNames: list = []
    cCloseImaFilenames: list = []

    cCloseRefImaWidgetNames: list = []
    cCloseRefImaFilenames: list = []
    # zVlaues = [value['z'] for value in cItems.values()]
    # the items were already sorted in descend order
    itemIds = getSliderItemIds(cWidget)
    itemIds.reverse()  # reverse the key id order
    # itemIds = itemIds[-1::-1] # reverse the key id order in ascend

    if isContainItemType(itemIds, Info.ITEM_SOUND):
        printAutoInd(sliderStimCodes, "% prepare audio materials for widget {0}", cWidgetName)
        printAutoInd(sliderStimCodes, "predictedVisOnset = PredictVisualOnsetForTime({0}, cDurs({1}) + lastScrOnsetTime({1}) - flipComShiftDur({1}));",
                     cWinStr, cWinIdx)
    # loop twice, once for audio and once for all visual stimuli
    '''
    ---------------------------------------
    # handle all audio stimuli
    ---------------------------------------
    '''
    iSoundSlave = 1

    for cItemId in itemIds:
        cItemProperties = cItems[cItemId]

        if getItemType(cItemId) == Info.ITEM_SOUND:
            printAutoInd(sliderStimCodes, "% create item: {0} in {1}", cItemId, cWidgetName)
            if iSoundSlave == 1:
                printAutoInd(sliderStimCodes,
                             "% schedule start of audio at exactly the predicted time of the next flip")

            allWidgetCodes = drawSoundWidget(cWidget, sliderStimCodes, attributesSetDict, cLoopLevel, allWidgetCodes,
                                             cItemProperties, iSoundSlave)
            iSoundSlave += 1
        else:
            pass

    # remove sound items
    itemIds = [cItemId for cItemId in itemIds if getItemType(cItemId) != Info.ITEM_SOUND]

    # draw background frame effects

    drawFrameEffect(cWidget, cVSLCodes, cSliderProperties['Properties'], attributesSetDict)
    '''
    --------------------------------------
    loop to handle all visual stimuli
    --------------------------------------
    '''
    printAutoInd(cVSLCodes, "% draw item {0} in {1}", itemIds, cWidgetName)

    for cItemId in itemIds:
        cItemType = getItemType(cItemId)
        cItemProperties = cItems[cItemId]
        isItemRef = False

        if cItemType in [Info.ITEM_GABOR, Info.ITEM_IMAGE, Info.ITEM_SNOW, Info.ITEM_TEXT, Info.ITEM_VIDEO]:
            printAutoInd(sliderStimCodes, "% prepare materials for item {0} in {1}", cItemId, cWidgetName)

        # printAutoInd(cVSLCodes, "% draw item {0} in {1}", cItemId, cWidgetName)

        cItemId = cWidgetName + '_' + cItemId
        cItemId = re.sub(r'[ .]+', '_', cItemId)

        if cItemType == Info.ITEM_LINE:
            borderColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Color'], attributesSetDict))
            lineWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Width'], attributesSetDict))
            cX1 = dataStrConvert(*getRefValue(cWidget, cItemProperties['X1'], attributesSetDict))
            cY1 = dataStrConvert(*getRefValue(cWidget, cItemProperties['Y1'], attributesSetDict))
            cX2 = dataStrConvert(*getRefValue(cWidget, cItemProperties['X2'], attributesSetDict))
            cY2 = dataStrConvert(*getRefValue(cWidget, cItemProperties['Y2'], attributesSetDict))

            printAutoInd(cVSLCodes, "Screen('DrawLine', {0}, {1}, {2}, {3}, {4}, {5}, {6});", cWinStr, borderColor, cX1,
                         cY1, cX2, cY2, lineWidth)

        elif cItemType == Info.ITEM_RECT:

            centerX = dataStrConvert(*getRefValue(cWidget, cItemProperties['Center X'], attributesSetDict))
            centerY = dataStrConvert(*getRefValue(cWidget, cItemProperties['Center Y'], attributesSetDict))
            cWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Width'], attributesSetDict))
            cHeight = dataStrConvert(*getRefValue(cWidget, cItemProperties['Height'], attributesSetDict))
            lineWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Width'], attributesSetDict))

            fillColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Fill Color'], attributesSetDict))
            borderColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Color'], attributesSetDict))

            if fillColor == "[0,0,0,0]":
                printAutoInd(cVSLCodes,
                             "Screen('FrameRect' ,{0} ,{1} ,CenterRectOnPointd([0,0,{2},{3}], {4}, {5}) ,{6});",
                             cWinStr, borderColor, cWidth, cHeight, centerX, centerY, lineWidth)
            elif lineWidth == '0' or fillColor == borderColor:
                printAutoInd(cVSLCodes, "Screen('FillRect',{0} ,{1}, CenterRectOnPointd([0,0,{2},{3}], {4}, {5}));",
                             cWinStr, fillColor, cWidth, cHeight, centerX, centerY)
            else:
                printAutoInd(sliderStimCodes, "{0}cRect = CenterRectOnPointd([0, 0, {1}, {2}], {3}, {4});", cItemId,
                             cWidth, cHeight,
                             centerX, centerY)
                printAutoInd(cVSLCodes, "Screen('FillRect' ,{0} ,{1} ,{2}cRect);", cWinStr, fillColor, cItemId)
                printAutoInd(cVSLCodes, "Screen('FrameRect' ,{0} ,{1} ,{2}cRect ,{3});", cWinStr, borderColor, cItemId, lineWidth)

        elif cItemType == Info.ITEM_CIRCLE:
            centerX = dataStrConvert(*getRefValue(cWidget, cItemProperties['Center X'], attributesSetDict))
            centerY = dataStrConvert(*getRefValue(cWidget, cItemProperties['Center Y'], attributesSetDict))
            cWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Width'], attributesSetDict))
            cHeight = dataStrConvert(*getRefValue(cWidget, cItemProperties['Height'], attributesSetDict))
            lineWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Width'], attributesSetDict))

            fillColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Fill Color'], attributesSetDict))
            borderColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Color'], attributesSetDict))

            if fillColor == "[0,0,0,0]":
                printAutoInd(cVSLCodes,
                             "Screen('FrameOval', {0}, {1}, CenterRectOnPointd([0, 0, {2}, {3}], {4}, {5}) ,{6}, {6});",
                             cWinStr, borderColor, cWidth, cHeight, centerX, centerY, lineWidth)
            elif lineWidth == '0' or fillColor == borderColor:
                printAutoInd(cVSLCodes, "Screen('FillOval', {0}, {1}, CenterRectOnPointd([0, 0, {2}, {3}], {4}, {5}));",
                             cWinStr, fillColor, cWidth, cHeight, centerX, centerY)
            else:
                printAutoInd(sliderStimCodes, "{0}cRect = CenterRectOnPointd([0, 0, {1}, {2}], {3}, {4});", cItemId,
                             cWidth, cHeight,
                             centerX, centerY)
                printAutoInd(cVSLCodes, "Screen('FillOval',{0}, {1}, {2}cRect);", cWinStr, fillColor, cItemId)
                printAutoInd(cVSLCodes, "Screen('FrameOval',{0}, {1}, {2}cRect, {3}, {3});", cWinStr, borderColor,
                             cItemId, lineWidth)

        elif cItemType == Info.ITEM_POLYGON:
            lineWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Width'], attributesSetDict))

            fillColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Fill Color'], attributesSetDict))
            borderColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Color'], attributesSetDict))

            points = cItemProperties['Points']
            parsedPoints = []
            for cXY in points:
                cX = getRefValue(cWidget, cXY[0], attributesSetDict)
                cY = getRefValue(cWidget, cXY[1], attributesSetDict)

                parsedPoints.append([cX[0], cY[0]])

            pointListStr = "".join(cXY[0] + "," + cXY[1] + ";" for cXY in parsedPoints)
            pointListStr = addSquBrackets(pointListStr[0:-1])

            if fillColor == "[0,0,0,0]":
                printAutoInd(cVSLCodes, "Screen('FramePoly', {0}, {1}, {2}, {3});", cWinStr, borderColor, pointListStr,
                             lineWidth)
            elif lineWidth == '0' or fillColor == borderColor:
                printAutoInd(cVSLCodes, "Screen('FillPoly', {0}, {1}, {2});", cWinStr, fillColor, pointListStr)
            else:
                printAutoInd(sliderStimCodes, "{0}cPointList = {1};", cItemId, pointListStr)
                printAutoInd(cVSLCodes, "Screen('FillPoly', {0}, {1}, {2}cPointList);", cWinStr, fillColor, cItemId)
                printAutoInd(cVSLCodes, "Screen('FramePoly', {0}, {1}, {2}cPointList, {3});", cWinStr, borderColor,
                             cItemId, lineWidth)

        elif cItemType == Info.ITEM_ARC:
            centerXStr, isCenterXRef = getRefValue(cWidget, cItemProperties['Center X'], attributesSetDict)
            centerX = dataStrConvert(centerXStr, isCenterXRef)

            centerYStr, isCenterYRef = getRefValue(cWidget, cItemProperties['Center Y'], attributesSetDict)
            centerY = dataStrConvert(centerYStr, isCenterYRef)

            cWidthStr, isWidthRef = getRefValue(cWidget, cItemProperties['Width'], attributesSetDict)
            cWidth = dataStrConvert(cWidthStr, isWidthRef)

            cHeightStr, isHeightRef = getRefValue(cWidget, cItemProperties['Height'], attributesSetDict)
            cHeight = dataStrConvert(cHeightStr, isHeightRef)

            lineWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Width'], attributesSetDict))

            fillColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Fill Color'], attributesSetDict))
            borderColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Color'], attributesSetDict))

            angleStartStr, isAngleStartRef = getRefValue(cWidget, cItemProperties['Angle Start'], attributesSetDict)
            angleStart = dataStrConvert(angleStartStr, isAngleStartRef)

            angleLengthStr, isanglelengthRef = getRefValue(cWidget, cItemProperties['Angle Length'], attributesSetDict)
            angleLength = dataStrConvert(angleLengthStr, isanglelengthRef)

            if isCenterXRef + isCenterYRef + isWidthRef + isHeightRef + isAngleStartRef + isanglelengthRef:
                haveArcStim = 2
                xysStr = "getArcLinePs_APL({0},{1},{2},{3});".format(cWidth, cHeight, angleStart, angleLength)
            else:
                haveArcStim = 1
                xysStr = getCrossAngleLineXYsInArc(cWidth, cHeight, angleStart, angleLength)

            if fillColor == "[0,0,0,0]":
                printAutoInd(cVSLCodes, "Screen('FrameArc', {0}, {1}, CenterRectOnPointd([0, 0, {2}, {3}], {4}, {5}), {6}, {7} ,{8}, {8});",
                             cWinStr, borderColor, cWidth, cHeight, centerX, centerY, angleStart, angleLength, lineWidth)
                printAutoInd(cVSLCodes, "Screen('DrawLines', {0}, {1}, {2}, {3}, [{4}, {5}]);", cWinStr, xysStr,
                             lineWidth, borderColor, centerX, centerY)

            elif lineWidth == '0' or fillColor == borderColor:
                printAutoInd(cVSLCodes,
                             "Screen('FillArc', {0}, {1}, CenterRectOnPointd([0, 0, {2}, {3}], {4}, {5}), {6}, {7});",
                             cWinStr, fillColor, cWidth, cHeight, centerX, centerY, angleStart, angleLength)
            else:
                printAutoInd(sliderStimCodes, "{0}cRect = CenterRectOnPointd([0, 0, {1}, {2}], {3}, {4});", cItemId,
                             cWidth, cHeight,
                             centerX, centerY)
                printAutoInd(cVSLCodes, "Screen('FillArc', {0}, {1}, {2}cRect, {3}, {4});", cWinStr, fillColor, cItemId,
                             angleStart, angleLength)

                printAutoInd(cVSLCodes, "Screen('FrameArc', {0}, {1}, {2}cRect, {3}, {4}, {5}, {5});", cWinStr,
                             borderColor, cItemId, angleStart, angleLength, lineWidth)
                printAutoInd(cVSLCodes, "Screen('DrawLines', {0}, {1}, {2}, {3}, [{4}, {5}]);", cWinStr, xysStr,
                             lineWidth, borderColor, centerX, centerY)

        elif cItemType == Info.ITEM_GABOR:  # 'gabor':
            haveGaborStim = True
            centerX, isCenterXRef = getRefValue(cWidget, cItemProperties['Center X'], attributesSetDict)
            centerX = dataStrConvert(centerX, isCenterXRef)

            centerY, isCenterYRef = getRefValue(cWidget, cItemProperties['Center Y'], attributesSetDict)
            centerY = dataStrConvert(centerY, isCenterYRef)

            cWidth, isWidthRef = getRefValue(cWidget, cItemProperties['Width'], attributesSetDict)
            cWidth = dataStrConvert(cWidth, isWidthRef)

            cHeight, isHeightRef = getRefValue(cWidget, cItemProperties['Height'], attributesSetDict)
            cHeight = dataStrConvert(cHeight, isHeightRef)

            cSpatialFreq, isSpatialFreqRef = getRefValue(cWidget, cItemProperties['Spatial'], attributesSetDict)
            cSpatialFreq = dataStrConvert(cSpatialFreq, isSpatialFreqRef)

            cContrast, isContrastRef = getRefValue(cWidget, cItemProperties['Contrast'], attributesSetDict)
            cContrast = dataStrConvert(cContrast, isContrastRef)

            cPhase, isPhaseRef = getRefValue(cWidget, cItemProperties['Phase'], attributesSetDict)
            cPhase = dataStrConvert(cPhase, isPhaseRef)

            cOrientation, isOrientationRef = getRefValue(cWidget, cItemProperties['Orientation'], attributesSetDict)
            cOrientation = dataStrConvert(cOrientation, isOrientationRef)

            cRotation, isRotationRef = getRefValue(cWidget, cItemProperties['Rotation'], attributesSetDict)
            cRotation = dataStrConvert(cRotation, isRotationRef)

            cSDx, isSDxRef = getRefValue(cWidget, cItemProperties['SDx'], attributesSetDict)
            cSDx = dataStrConvert(cSDx, isSDxRef)

            cSDy, isSDyRef = getRefValue(cWidget, cItemProperties['SDy'], attributesSetDict)
            cSDy = dataStrConvert(cSDy, isSDyRef)

            cBackColor, isBkColorRef = getRefValue(cWidget, cItemProperties['Back Color'], attributesSetDict)
            cBackColor = dataStrConvert(cBackColor, isBkColorRef)

            cTransparency = dataStrConvert(*getRefValue(cWidget, cItemProperties['Transparency'], attributesSetDict))

            isItemRef = isCenterYRef + isCenterXRef + isWidthRef + isHeightRef + isSpatialFreqRef + isContrastRef + isPhaseRef + isOrientationRef + isRotationRef + isSDxRef + isSDyRef + isBkColorRef

            if isItemRef == 0 and cLoopLevel > 0:
                # if its not ref and should be under cycling
                printAutoInd(sliderStimCodes, "if ~exist('{0}_Mx','var')", cItemId)
                printAutoInd(sliderStimCodes, "{0}_Mx  = makeGabor_APL({1}, {2}, {3}, {4}, {5}, [{6},{7}], {8}, {9});",
                             cItemId, cSpatialFreq, cContrast, cPhase, cOrientation, cBackColor, cWidth, cHeight, cSDx, cSDy)
                printAutoInd(sliderStimCodes, "{0}_idx = Screen('MakeTexture', {1}, {0}_Mx);", cItemId, cWinStr)
                printAutoInd(sliderStimCodes, "end ")

                beClosedTxAFCycleList.append(f"{cItemId}_idx")
            else:
                printAutoInd(sliderStimCodes, "{0}_Mx  = makeGabor_APL({1}, {2}, {3}, {4}, {5}, [{6},{7}], {8}, {9});",
                             cItemId, cSpatialFreq, cContrast, cPhase, cOrientation, cBackColor, cWidth, cHeight, cSDx, cSDy)
                printAutoInd(sliderStimCodes, "{0}_idx = Screen('MakeTexture', {1}, {0}_Mx);", cItemId, cWinStr)

                cCloseIdxesStr += f"{cItemId}_idx, "

            printAutoInd(cVSLCodes,
                         "Screen('DrawTexture', {0}, {1}_idx, [], CenterRectOnPointd([0,0,size({1}_Mx,2),size({1}_Mx,1)], {2}, {3}), {4}, [], abs({5}) );",
                         cWinStr, cItemId, centerX, centerY,
                         cRotation,
                         cTransparency)

        elif cItemType == Info.ITEM_SNOW:
            haveSnowStim = True
            centerX, isCenterXRef = getRefValue(cWidget, cItemProperties['Center X'], attributesSetDict)
            centerX = dataStrConvert(centerX, isCenterXRef)

            centerY, isCenterYRef = getRefValue(cWidget, cItemProperties['Center Y'], attributesSetDict)
            centerY = dataStrConvert(centerY, isCenterYRef)

            cWidth, isWidthRef = getRefValue(cWidget, cItemProperties['Width'], attributesSetDict)
            cWidth = dataStrConvert(cWidth, isWidthRef)

            cHeight, isHeightRef = getRefValue(cWidget, cItemProperties['Height'], attributesSetDict)
            cHeight = dataStrConvert(cHeight, isHeightRef)

            cScale, isScaleRef = getRefValue(cWidget, cItemProperties['Scale'], attributesSetDict)
            cScale = dataStrConvert(cScale, isScaleRef)

            isItemRef = isCenterXRef + isCenterYRef + isWidthRef + isHeightRef + isScaleRef

            cRotation = dataStrConvert(*getRefValue(cWidget, cItemProperties['Rotation'], attributesSetDict))

            cTransparency = dataStrConvert(*getRefValue(cWidget, cItemProperties['Transparency'], attributesSetDict))

            if isItemRef == 0 and cLoopLevel > 0:
                # printAutoInd(sliderStimCodes, "if ~exist('{0}_Mx','var')", cItemId)
                printAutoInd(sliderStimCodes, "{0}_Mx  = makeSnow_APL({1}, {2}, {3});", cItemId, cWidth, cHeight,
                             cScale)
                printAutoInd(sliderStimCodes, "{0}_idx = Screen('MakeTexture', {1}, {0}_Mx);", cItemId, cWinStr)
                # printAutoInd(sliderStimCodes, "end")

                cCloseIdxesStr += f"{cItemId}_idx, "
            else:
                printAutoInd(sliderStimCodes, "{0}_Mx  = makeSnow_APL({1}, {2}, {3});", cItemId, cWidth, cHeight,
                             cScale)
                printAutoInd(sliderStimCodes, "{0}_idx = Screen('MakeTexture', {1}, {0}_Mx);", cItemId, cWinStr)
                # for possible to be closed textures
                cCloseIdxesStr += f"{cItemId}_idx, "

            printAutoInd(cVSLCodes, "Screen('DrawTexture', {0}, {1}_idx, [], CenterRectOnPointd([0,0,{2},{3}], {4}, {5}), {6}, [], abs({7}));",
                         cWinStr, cItemId, cWidth, cHeight, centerX, centerY, cRotation, cTransparency)

        elif Info.ITEM_DOT_MOTION == cItemType:
            haveDotMotion = True

            centerX, isCenterXRef = getRefValue(cWidget, cItemProperties['Center X'], attributesSetDict)
            centerX = dataStrConvert(centerX, isCenterXRef)

            centerY, isCenterYRef = getRefValue(cWidget, cItemProperties['Center Y'], attributesSetDict)
            centerY = dataStrConvert(centerY, isCenterYRef)

            cWidth, isWidthRef = getRefValue(cWidget, cItemProperties['Width'], attributesSetDict)
            cWidth = dataStrConvert(cWidth, isWidthRef)

            cHeight, isHeightRef = getRefValue(cWidget, cItemProperties['Height'], attributesSetDict)
            cHeight = dataStrConvert(cHeight, isHeightRef)

            nDots, isnDotsRef = getRefValue(cWidget, cItemProperties['Dot Num'], attributesSetDict)
            nDots = dataStrConvert(nDots, isnDotsRef)

            dotSize, isDotSizeRef = getRefValue(cWidget, cItemProperties['Dot Size'], attributesSetDict)
            dotSize = dataStrConvert(dotSize, isDotSizeRef)

            dotType, isDotTypeRef = getRefValue(cWidget, cItemProperties['Dot Type'], attributesSetDict)
            dotType = dataStrConvert(dotType, isDotTypeRef)

            cDirection, isDirectionRef = getRefValue(cWidget, cItemProperties['Move Direction'], attributesSetDict)
            cDirection = dataStrConvert(cDirection, isDirectionRef)

            cSpeed, isSpeedRef = getRefValue(cWidget, cItemProperties['Speed'], attributesSetDict)
            cSpeed = dataStrConvert(cSpeed, isSpeedRef)

            cCoherence, isCoherenceRef = getRefValue(cWidget, cItemProperties['Coherence'], attributesSetDict)
            cCoherence = dataStrConvert(cCoherence, isCoherenceRef)

            cDotColor, isDotColorRef = getRefValue(cWidget, cItemProperties['Dot Color'], attributesSetDict)
            cDotColor = dataStrConvert(cDotColor, isDotColorRef)

            isOval = parseBooleanStr(*getRefValue(cWidget, cItemProperties['Is Oval'], attributesSetDict))

            printAutoInd(sliderStimCodes, "{0}_xys  = initialDotPos_APL({1}, {2}, {3}, {4}, {5}, {6});",
                         cItemId, nDots, cDirection, cCoherence, isOval, cWidth, cHeight)

            printAutoInd(sliderStimCodes, "{0}_cxy  = repmat([{1};{2}],1,{3});", cItemId, centerX, centerY, nDots)

            printAutoInd(cVSLCodes, "Screen('DrawDots', {0}, {1}_xys(1:2,{1}_xys(4,:)) + {1}_cxy, {2}, {3}, [], {4});",
                         cWinStr, cItemId, dotSize, cDotColor, dotType)
            printAutoInd(cVSLCodes, "if iFrame > 1")
            printAutoInd(cVSLCodes, "{0}_xys = updateDotPos_APL({0}_xys,{1},predictedDurToNextFlip(winIFIs({2}),nearestPrevFrameOnsetTime),{3},{4},{5}); ",
                         cItemId, cSpeed, cWinIdx, isOval, cWidth, cHeight)

            printAutoInd(cVSLCodes, "end \n")

        elif Info.ITEM_TEXT == cItemType:
            cVSLCodes = drawTextForSlider(cWidget, sliderStimCodes, attributesSetDict, cLoopLevel, cItemProperties, cVSLCodes)
        elif cItemType == Info.ITEM_VIDEO:
            allWidgetCodes, cVSLCodes = drawVideoWidget(cWidget, sliderStimCodes, attributesSetDict, cLoopLevel,
                                                        allWidgetCodes, cItemProperties, cVSLCodes, iVideoNum)
            iVideoNum += 1

        elif cItemType == Info.ITEM_IMAGE:
            allWidgetCodes, cVSLCodes, isImFileNameRef, cFileNameStr, cPossFilenames = drawImageWidget(
                cWidget, sliderStimCodes, attributesSetDict,
                cLoopLevel, allWidgetCodes, cItemProperties, cVSLCodes)

            cPrefixStr = cItemId
            # here for image item in scene widget
            if cLoopLevel == 0 or Info.IMAGE_LOAD_MODE == "before_event":
                if isImFileNameRef:
                    cCloseRefImaFilenames.append(cFileNameStr)
                    cCloseRefImaWidgetNames.append(cPrefixStr)
                else:
                    cCloseImaFilenames.append(cFileNameStr)
                    cCloseImaWidgetNames.append(cPrefixStr)

            elif cLoopLevel > 0:
                for cPossFilename in cPossFilenames:
                    xedTxAFCycleWidgetFilenameList.append({cPrefixStr: cPossFilename})

    if not getFlipType(cWidget):
        clearAfter = getClearAfterInfo(cWidget, attributesSetDict)

        # for no video scene, extend the content of cVSLCodes
        sliderStimCodes.extend(cVSLCodes)
        cVSLCodes = []

        printAutoInd(sliderStimCodes, "% give the GPU a break", cWinStr, clearAfter)
        printAutoInd(sliderStimCodes, "Screen('DrawingFinished',{0},{1});\n", cWinStr, clearAfter)

    '''
    # ------------------------------------------
    # the last step: upload the delayed codes
    # ------------------------------------------
    '''
    if len(cCloseIdxesStr) > 0 or len(cCloseRefImaFilenames) > 0 or len(cCloseImaWidgetNames) > 0:
        cAfEndVideoFlipCodes = allWidgetCodes.get('codesJustBeRespCodes', [])

        if len(cCloseRefImaFilenames) > 0 or len(cCloseImaWidgetNames) > 0:
            cAfEndVideoFlipCodes.append("% close image textures")

            if len(cCloseImaWidgetNames) > 0:
                cAfEndVideoFlipCodes.append(f"CloseTexture_APL({getImaIndexStr(cCloseImaFilenames)}, {getWidNameIndexStr(cCloseImaWidgetNames)}, false);\n")

            if len(cCloseRefImaFilenames) > 0:
                tempCellImaVarStr = ''.join(cImaVarStr+', ' for cImaVarStr in cCloseRefImaFilenames)
                tempCellImaVarStr = '{'+tempCellImaVarStr[0:-2]+'}'
                cAfEndVideoFlipCodes.append(f"CloseTexture_APL({tempCellImaVarStr}, {getWidNameIndexStr(cCloseRefImaWidgetNames)}, false);\n")

        if len(cCloseIdxesStr) > 0:
            cAfEndVideoFlipCodes.append("% close textures of stim generated by MATLAB (e.g., Gabor, Snow)")
            if len(re.split(',', cCloseIdxesStr[0:-2])) > 1:
                cAfEndVideoFlipCodes.append(f"Screen('Close', [{cCloseIdxesStr[0:-2]}]);\n")
            else:
                cAfEndVideoFlipCodes.append(f"Screen('Close', {cCloseIdxesStr[0:-2]});\n")

        allWidgetCodes.update({'codesJustBeRespCodes': cAfEndVideoFlipCodes})

    allWidgetCodes.update({'forVideoSliderLoopCodes': cVSLCodes})

    allWidgetCodes.update({f"beClosedTextures_{cLoopLevel}": beClosedTxAFCycleList})

    if Info.IMAGE_LOAD_MODE in ["before_exp", "before_trial"]:
        allWidgetCodes.update({f"xedTxAFCycleWidgetFilenameList_{bePrintLoopLevel}": xedTxAFCycleWidgetFilenameList})
    return allWidgetCodes


def drawSoundWidget(cWidget, soundStimCodes, attributesSetDict, cLoopLevel, allWidgetCodes, cProperties=None, iSlave=1):
    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint

    if cProperties is None:
        cProperties = []

    # cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output variable's row num

    if len(cProperties) == 0:
        isNotInSlide = True
        cProperties = Func.getWidgetProperties(cWidget.widget_id)
    else:
        isNotInSlide = False

    # data and buffer prefixStr e.g., slider_1_sound_1_Dat
    if isNotInSlide:
        cPrefixStr = getWidgetName(cWidget.widget_id)
    else:
        cPrefixStr = getWidgetName(cWidget.widget_id) + '_' + cProperties['Name']

    # if getWidgetPos(cWidget.widget_id) == 0 and isNotInSlide and not(isSubWidgetOfIfOrSwitch(cWidget.widget_id)):
    #     # Step 2: print out help info for the current widget
    #     printAutoInd(soundStimCodes, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    #     printAutoInd(soundStimCodes, '%loop:{0}, event{1}: {2}', cLoopLevel, getWidgetEventPos(cWidget.widget_id) + 1,
    #                  getWidgetName(cWidget.widget_id))
    #     printAutoInd(soundStimCodes, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    # cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    # 2) handle file name:
    # cFileNameStr, isFileNameRef = getRefValue(cWidget, cProperties['File Name'], attributesSetDict)
    cFileNameStr = trans2relativePath(cProperties['File Name'])
    if not cFileNameStr:
        throwCompileErrorInfo(f'You did not specify the audio file for the event/item: {cPrefixStr}')

    cFileNameStr, isFileNameRef, _ = getValueInContainRefExp(cWidget, cFileNameStr, attributesSetDict, True)

    cFileNameStr = genAppropriatePathSplitter(cFileNameStr, Info.PLATFORM == 'windows')

    # # # 3) check the Buffer Size parameter:
    # # bufferSizeStr, isRef = getRefValue(cWidget, cWidget.getBufferSize(), attributesSetDict)
    #
    # # 3) check the Stream Refill parameter:
    # streamRefillStr, isRef = getRefValue(cWidget, cProperties['Stream Refill'], attributesSetDict)
    #
    # # 4) check the start offset in ms parameter:
    # startOffsetStr, isRef = getRefValue(cWidget, cProperties['Start Offset'], attributesSetDict)
    #
    # # 5) check the stop offset in ms parameter:
    # StopOffsetStr, isRef = getRefValue(cWidget, cProperties['Stop Offset'], attributesSetDict)
    #
    # # # 6) check the repetitions parameter:
    # # repetitionsStr, isRef = getRefValue(cWidget, cWidget.getRepetitions(), attributesSetDict)
    #
    # # 7) check the volume control parameter:
    # isVolumeControl, isRef = getRefValue(cWidget, cProperties['Volume Control'], attributesSetDict)
    #
    # # 8) check the volume parameter:
    # volumeStr, isRef = getRefValue(cWidget, cProperties['Volume'], attributesSetDict)
    #
    # # 9) check the latencyBias control parameter:
    # isLatencyBiasControl, isRef = getRefValue(cWidget, cProperties['Latency Bias'], attributesSetDict)
    #
    # # 10) check the volume parameter:
    # latencyBiasStr, isRef = getRefValue(cWidget, cProperties['Bias Time'], attributesSetDict)
    #
    # # 11) check the sound device name parameter:
    # shouldNotBeCitationCheck('Sound Device', cProperties['Sound Device'])
    # cSoundDevName, isRef = getRefValue(cWidget, cProperties['Sound Device'], attributesSetDict)
    #
    # cSoundIdxStr = f"{outputDevNameIdxDict.get(cSoundDevName)}({iSlave})"
    # cSoundFsStr = f"{outputDevNameIdxDict.get(cSoundDevName+'_fs')}"
    # cSoundnChansStr = f"{outputDevNameIdxDict.get(cSoundDevName+'_nChans')}"
    #
    # # 12) check the volume parameter:
    # waitForStartStr = parseBooleanStr(*getRefValue(cWidget, cProperties['Wait For Start'], attributesSetDict))

    printAutoInd(soundStimCodes,"    var {0} = ",cPrefixStr)
    soundStimCodes.append("{")
    printAutoInd(soundStimCodes,"type: 'audio-keyboard-response',")
    printAutoInd(soundStimCodes,"  stimulus: {0}",mypathform(cFileNameStr))
    soundStimCodes.append("};")
    printAutoInd(soundStimCodes,"timeline.push({0});",cPrefixStr)
    # read audio file
    # if isFileNameRef is False and cLoopLevel > 0:
    #     printAutoInd(soundStimCodes, "if ~exist({0}_Dat,'var')", cPrefixStr)
    #     printAutoInd(soundStimCodes, "[{0}_Dat, {0}_fs] = audioread(fullfile(cFolder,{1}) );", cPrefixStr, cFileNameStr)
    #     printAutoInd(soundStimCodes, "% check the sampling rate")
    #     printAutoInd(soundStimCodes, "if {0}_fs ~= {1}", cPrefixStr, cSoundFsStr)
    #     printAutoInd(soundStimCodes, "error(['The fs of current audio file (',num2str({0}_fs),') is not matched with the defined audio device(',num2str({1}),').']);", cPrefixStr, cSoundFsStr)
    #     printAutoInd(soundStimCodes, "end")
    #
    #     # make audio buffer
    #     # printAutoInd(f, "{0}_idx = PsychPortAudio('CreateBuffer', {1}, cAudioData);",cPrefixStr,cSoundIdxStr)
    #     printAutoInd(soundStimCodes, "end")
    # else:
    #     printAutoInd(soundStimCodes, "[{0}_Dat, {0}_fs] = audioread(fullfile(cFolder,{1}) );", cPrefixStr, cFileNameStr)
    #     printAutoInd(soundStimCodes, "if {0}_fs ~= {1}", cPrefixStr, cSoundFsStr)
    #     printAutoInd(soundStimCodes, "error(['The fs of current audio file (', num2str({0}_fs) ,') is not matched with the defined audio device(',num2str({1}),').']);", cPrefixStr, cSoundFsStr)
    #     printAutoInd(soundStimCodes, "end")
    #     # make audio buffer
    #     # printAutoInd(f, "{0}_idx = PsychPortAudio('CreateBuffer', {1}, cAudioData);",cPrefixStr,cSoundIdxStr)
    #
    # #  draw buffer to  hw
    # # printAutoInd(f, "PsychPortAudio('FillBuffer', {0}, {1}_idx, {2});",cSoundIdxStr,cPrefixStr, streamRefillStr)
    #
    # printAutoInd(soundStimCodes, "PsychPortAudio('FillBuffer', {0}, {1}_Dat(1 + round({2}*{3}/1000):end - round({4}*{3}/1000),:)', {5});",
    #              cSoundIdxStr,
    #              cPrefixStr,
    #              startOffsetStr,
    #              cSoundFsStr,
    #              StopOffsetStr,
    #              streamRefillStr)
    #
    # if isVolumeControl:
    #     printAutoInd(soundStimCodes, "PsychPortAudio('Volume', {0}, {1});", cSoundIdxStr, volumeStr)
    #
    # if isLatencyBiasControl:
    #     printAutoInd(soundStimCodes, "PsychPortAudio('LatencyBias', {0}, {1}/1000);", cSoundIdxStr, latencyBiasStr)
    #
    # if isVolumeControl or isLatencyBiasControl:
    #     printAutoInd(soundStimCodes, "")

    if isNotInSlide:
        pass
        # printAutoInd(soundStimCodes, "% check the 'esc' key to abort the exp")
        # printAutoInd(soundStimCodes, "detectAbortKey_APL(abortKeyCode);\n")
    else:
        # for sounds in slider
        # check the repetitions parameter:
        repetitionsStr, isRef = getRefValue(cWidget, cProperties['Repetitions'], attributesSetDict)
        # printAutoInd(soundStimCodes, "PsychPortAudio('Start', {0}, {1}, predictedVisOnset, 0); %\n", cSoundIdxStr,
        #              repetitionsStr)

    # ------------------------------------------
    # the last step: upload the delayed codes
    # ------------------------------------------

    return allWidgetCodes


def drawImageWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes, cProperties=None, cVSLCodes=None):
    if cVSLCodes is None:
        cVSLCodes = []
    if cProperties is None:
        cProperties = []

    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint
    isNotInSlide = True

    if len(cProperties) == 0:
        cProperties = Func.getWidgetProperties(cWidget.widget_id)
    else:
        isNotInSlide = False

    cWidgetName = getWidgetName(cWidget.widget_id)

    if isNotInSlide:
        cPrefixStr = cWidgetName
    else:
        cPrefixStr = cWidgetName + '_' + cProperties['Name']

    cRespCodes = allWidgetCodes.get(f"{cWidget.widget_id}_cRespCodes", [])

    if Info.IMAGE_LOAD_MODE == "before_exp":
        bePrintLoopLevel = 1
        xedTxAFCycleWidgetFilenameList: list = allWidgetCodes.get(f"xedTxAFCycleWidgetFilenameList_{bePrintLoopLevel}", [])
    elif Info.IMAGE_LOAD_MODE == "before_trial":
        bePrintLoopLevel = cLoopLevel
        xedTxAFCycleWidgetFilenameList: list = allWidgetCodes.get(f"xedTxAFCycleWidgetFilenameList_{bePrintLoopLevel}", [])

    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    # 2) handle file name:
    cFileNameStr = trans2relativePath(cProperties['File Name'])
    if not cFileNameStr:
        throwCompileErrorInfo(f'You did not specify the image file for the event/item: {cPrefixStr}')

    cPossFilenames: set = getWidgetPossFilenames(cWidget, cFileNameStr)

    cFileNameStr, isFileNameRef, _ = getValueInContainRefExp(cWidget, cFileNameStr, attributesSetDict, True)

    # cFileNameStr, isFileNameRef = getRefValue(cWidget, cProperties['File Name'], attributesSetDict)
    cFileNameStr = genAppropriatePathSplitter(cFileNameStr, Info.PLATFORM == 'windows')

    # 3) check the mirror up/down parameter:
    isMirrorUpDownStr = parseBooleanStr(cProperties['Mirror Up/Down'])

    # 3) check the mirror left/right parameter:
    isMirrorLeftRightStr = parseBooleanStr(cProperties['Mirror Left/Right'])

    # 4) check the rotate parameter:
    rotateStr, isRef = getRefValue(cWidget, cProperties['Rotate'], attributesSetDict)

    # 5) check the stretch mode parameter:
    if cProperties['Stretch']:
        # ""、Both、Horizontal、UpDown、[attr]
        stretchModeStr = parseStretchModeStr(*getRefValue(cWidget, cProperties['Stretch Mode'], attributesSetDict))
    else:
        stretchModeStr = "0"

    # 6) check the Transparent parameter:
    imageTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Transparent'], attributesSetDict))

    # 7) check the parameter winRect
    sx = dataStrConvert(*getRefValue(cWidget, cProperties['Center X'], attributesSetDict))
    sy = dataStrConvert(*getRefValue(cWidget, cProperties['Center Y'], attributesSetDict))

    cWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Width'], attributesSetDict))
    cHeight = dataStrConvert(*getRefValue(cWidget, cProperties['Height'], attributesSetDict))

    # if isNotInSlide:
    #     # draw background frame effects
    #     drawFrameEffect(cWidget, f, cProperties, attributesSetDict)
    #
    # else:
    #     # make the dest Rect
    #     printAutoInd(f, "{0}_fRect = makeFrameRect_APL({1}, {2}, {3}, {4}, fullRects({5},:));", cPrefixStr, sx, sy,
    #                  cWidth,
    #                  cHeight, cWinIdx)

    # make texture
    # printAutoInd(f, "[{0}_idx, {0}_size]    = makeTexture_APL({1}, winIds(1), true);", cPrefixStr, cFileNameStr)
    # printAutoInd(f, "[{0}_dRect, {0}_sRect] = makeImDestRect_APL({0}_fRect, {0}_size, {1});", cPrefixStr, stretchModeStr)
    printAutoInd(f,"    var {0} = ",cWidgetName)
    f.append("{")
    printAutoInd(f,"type: 'image-keyboard-response',")
    printAutoInd(f,"  stimulus: {0}",mypathform(cFileNameStr))
    f.append("};")
    printAutoInd(f,"timeline.push({0});",cWidgetName)


    # if isNotInSlide:
    #     '''
    #     for no-slider image that means the image widget
    #     '''
    #     if isMirrorUpDownStr == '1' or isMirrorLeftRightStr == '1':
    #         printAutoInd(f, "[{0}xc, {0}yc] = RectCenter({0}_dRect);        % get the center of the {0}_dRect",
    #                      cPrefixStr)
    #         printAutoInd(f, "Screen('glPushMatrix', {0});             % enter into mirror mode", cWinStr)
    #         printAutoInd(f,
    #                      "Screen('glTranslate', {0}, {1}xc, {1}yc, 0);   % translate origin into the center of {1}_dRect",
    #                      cWinStr, cPrefixStr)
    #         if isMirrorLeftRightStr == '1':
    #             leftRightStr = '-1'
    #         else:
    #             leftRightStr = '1'
    #
    #         if isMirrorUpDownStr == '1':
    #             upDownStr = '-1'
    #         else:
    #             upDownStr = '1'
    #
    #         printAutoInd(f, "Screen('glScale', {0}, {1}, {2}, 1);     % mirror the drawn image", cWinStr, leftRightStr,
    #                      upDownStr)
    #         printAutoInd(f, "Screen('glTranslate', {0}, -{1}xc, -{1}yc, 0); % undo the translations", cWinStr,
    #                      cPrefixStr)
    #
    #     printAutoInd(f, "Screen('DrawTexture', {0}, {1}_idx, {1}_sRect, {1}_dRect, {2}, [], abs({3}));",
    #                  cWinStr,
    #                  cPrefixStr,
    #                  rotateStr,
    #                  imageTransparent)
    #
    #     if isMirrorUpDownStr == '1' or isMirrorLeftRightStr == '1':
    #         printAutoInd(f, "Screen('glPopMatrix', {0}); % restore to non mirror mode", cWinStr)
    # else:
    #     '''
    #     for image item in slider
    #     '''
    #     if isMirrorUpDownStr == '1' or isMirrorLeftRightStr == '1':
    #         printAutoInd(f, "[{0}xc, {0}yc] = RectCenter({0}_dRect);        % get the center of the {0}_dRect",
    #                      cPrefixStr)
    #
    #         printAutoInd(cVSLCodes, "Screen('glPushMatrix', {0});             % enter into mirror mode", cWinStr)
    #         printAutoInd(cVSLCodes, "Screen('glTranslate', {0}, {1}xc, {1}yc, 0);   % translate origin into the center of {1}_dRect",
    #                      cWinStr, cPrefixStr)
    #         if isMirrorLeftRightStr == '1':
    #             leftRightStr = '-1'
    #         else:
    #             leftRightStr = '1'
    #
    #         if isMirrorUpDownStr == '1':
    #             upDownStr = '-1'
    #         else:
    #             upDownStr = '1'
    #
    #         printAutoInd(cVSLCodes, "Screen('glScale', {0}, {1}, {2}, 1);     % mirror the drawn image", cWinStr,
    #                      leftRightStr,
    #                      upDownStr)
    #         printAutoInd(cVSLCodes, "Screen('glTranslate', {0}, -{1}xc, -{1}yc, 0); % undo the translations", cWinStr,
    #                      cPrefixStr)
    #
    #     printAutoInd(cVSLCodes, "Screen('DrawTexture', {0}, {1}_idx, {1}_sRect, {1}_dRect, {2}, [], abs({3}));",
    #                  cWinStr, cPrefixStr, rotateStr, imageTransparent)
    #
    #     if isMirrorUpDownStr == '1' or isMirrorLeftRightStr == '1':
    #         printAutoInd(cVSLCodes, "Screen('glPopMatrix', {0}); % restore to non mirror mode", cWinStr)
    #
    #     '''
    #     -------------------------------------------------------------------------
    #     # in slider, handle close texture within slider widget instead of here
    #     -------------------------------------------------------------------------
    #     '''
    # if isNotInSlide:
    #     clearAfter = getClearAfterInfo(cWidget, attributesSetDict)
    #     printAutoInd(f, "% give the GPU a break", cWinStr, clearAfter)
    #     printAutoInd(f, "Screen('DrawingFinished',{0},{1});\n", cWinStr, clearAfter)
    #
    #     if cLoopLevel == 0 or Info.IMAGE_LOAD_MODE == "before_event":
    #         printAutoInd(cRespCodes, "% close the texture corresponding to {0}", cPrefixStr)
    #
    #         if isFileNameRef:
    #             printAutoInd(cRespCodes, "CloseTexture_APL({0}, {1}, false);\n",
    #                          f"{cFileNameStr}",
    #                          getWidNameIndexStr(cPrefixStr))
    #         else:
    #             printAutoInd(cRespCodes, "CloseTexture_APL({0}, {1}, false);\n",
    #                          getImaIndexStr(cFileNameStr),
    #                          getWidNameIndexStr(cPrefixStr))
    #
    #     elif cLoopLevel > 0:
    #         for cPossFilename in cPossFilenames:
    #             xedTxAFCycleWidgetFilenameList.append({cPrefixStr: cPossFilename})
    #
    # '''
    # # ------------------------------------------
    # # the last step: upload the delayed codes
    # # ------------------------------------------
    # '''
    # allWidgetCodes.update({f"{cWidget.widget_id}_cRespCodes": cRespCodes})
    #
    # if Info.IMAGE_LOAD_MODE in ["before_exp", "before_trial"]:
    #     allWidgetCodes.update({f"xedTxAFCycleWidgetFilenameList_{bePrintLoopLevel}": xedTxAFCycleWidgetFilenameList})
    # elif Info.IMAGE_LOAD_MODE == "before_event":
    # no need here since we need to close the texture after each event
    return allWidgetCodes, cVSLCodes, isFileNameRef, cFileNameStr, list(cPossFilenames)


def drawVideoWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes, cProperties=None, cVSLCodes=None,
                    iVideoNum=0):
    # cVSLCode: codes for current video slider loop
    if cVSLCodes is None:
        cVSLCodes = []
    if cProperties is None:
        cProperties = []

    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint
    isNotInSlide = True

    if len(cProperties) == 0:
        cProperties = Func.getWidgetProperties(cWidget.widget_id)
    else:
        isNotInSlide = False

    cWidgetName = getWidgetName(cWidget.widget_id)
    if isNotInSlide:
        cItemOrWidgetNameStr = cWidgetName
    else:
        cItemOrWidgetNameStr = cProperties['Name']

    cVideoItemNums = getSliderItemTypeNums(cWidget, Info.ITEM_VIDEO)
    cDotMotionItemNums = getSliderItemTypeNums(cWidget, Info.ITEM_DOT_MOTION)

    cBeFlipCodes = allWidgetCodes.get('codesBeFlip', [])

    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    # 2) handle file name:
    cFileNameStr = trans2relativePath(cProperties['File Name'])
    if not cFileNameStr:
        throwCompileErrorInfo(f'You did not specify the video file for the event/item: {cWidgetName}_{cItemOrWidgetNameStr}')
    cFileNameStr, isFileNameRef, _ = getValueInContainRefExp(cWidget, cFileNameStr, attributesSetDict, True)

    # cFileNameStr, isFileNameRef = getRefValue(cWidget, cProperties['File Name'], attributesSetDict)
    cFileNameStr = genAppropriatePathSplitter(cFileNameStr, Info.PLATFORM == 'windows')

    # 2) handle aspect ration name:
    # stretchModeStr, isRef = getRefValue(cWidget, cProperties['Aspect Ratio'], attributesSetDict)
    # stretchModeStr = parseAspectRationStr(stretchModeStr, isRef)
    #
    # # 3) check the playback rate parameter:
    # playbackRateStr = dataStrConvert(*getRefValue(cWidget, cProperties['Playback Rate'], attributesSetDict))
    # # 4) check the Start position parameter:

    # startPositionStr, isRef = getRefValue(cWidget, cProperties['Start Position'], attributesSetDict)
    # startPositionStr = parseStartEndTimeStr(startPositionStr, isRef)
    #
    # endPositionStr, isRef = getRefValue(cWidget, cProperties['End Position'], attributesSetDict)
    # endPositionStr = parseStartEndTimeStr(endPositionStr, isRef)

    # 4) check the parameter winRect
    # sx = dataStrConvert(*getRefValue(cWidget, cProperties['Center X'], attributesSetDict))
    # sy = dataStrConvert(*getRefValue(cWidget, cProperties['Center Y'], attributesSetDict))
    #
    # cWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Width'], attributesSetDict))
    # cHeight = dataStrConvert(*getRefValue(cWidget, cProperties['Height'], attributesSetDict))

    # if isNotInSlide:
    #     # draw background frame effects
    #     drawFrameEffect(cWidget, f, cProperties, attributesSetDict)
    # else:
    #     printAutoInd(f, "{0}_fRect = makeFrameRect_APL({1}, {2}, {3}, {4}, fullRects({5},:));", cItemOrWidgetNameStr,
    #                  sx,
    #                  sy,
    #                  cWidth, cHeight, cWinIdx)
    #
    # # make texture
    # if isNotInSlide:
    #     printAutoInd(f, "% preload movie for widget: {0}", cItemOrWidgetNameStr)
    #
    # if Info.PLATFORM == 'linux':
    #     printAutoInd(f,
    #                  "% For linux, to use movie playback and PsychPortAudio at the same time, set specialFlags1 to 2")
    #     printAutoInd(f,
    #                  "Screen('OpenMovie', {0}, fullfile(cFolder,{1}), 1, [], 2); % Preloading the movie in background...\n",
    #                  cWinStr, cFileNameStr)
    # else:
    #     printAutoInd(f, "Screen('OpenMovie', {0}, fullfile(cFolder,{1}), 1); % Preloading the movie in background...\n",
    #                  cWinStr, cFileNameStr)
    #
    # '''
    # get the durStr to calculate the end movie times
    # '''
    durStr, isRefValue, cRefValueSet = getRefValueSet(cWidget, cWidget.getDuration(), attributesSetDict)
    durStr = parseDurationStr(durStr)

    # if isNotInSlide is True:
    #     cBeFlipCodes.append(f"% Really start to handle movie file in widget {cWidgetName}")
    # else:
    #     cBeFlipCodes.append(f"% Really start to handle movie item: {cItemOrWidgetNameStr} in slider {cWidgetName}")

    # printAutoInd(cVSLCodes, "% get and draw each video frame of {0}", cItemOrWidgetNameStr)

    # if cVideoItemNums <= 1:
    #     '''
    #     ----------------------------------------------------------
    #     for video widget or slider containing only one video item
    #     ----------------------------------------------------------
    #     '''
    #     cBeFlipCodes.append(f"{cWidgetName}_sMTime = {startPositionStr}/1000; ")
    #     cBeFlipCodes.append(f"{cWidgetName}_eMTime = {endPositionStr}/1000; ")
    #
    #     if Info.PLATFORM == 'linux':
    #         cBeFlipCodes.append("% For linux, to use movie playback and PsychPortAudio at the same time, set specialFlags1 to 2")
    #         cBeFlipCodes.append(f"[{cWidgetName}_mPtr,{cWidgetName}_mDur, ~,{cItemOrWidgetNameStr}_ImgW, {cItemOrWidgetNameStr}_ImgH] = Screen('OpenMovie',{cWinStr}, fullfile(cFolder,{addSingleQuotes(cFileNameStr)}),[],[],2 );")
    #     else:
    #         cBeFlipCodes.append(f"[{cWidgetName}_mPtr,{cWidgetName}_mDur, ~,{cItemOrWidgetNameStr}_ImgW, {cItemOrWidgetNameStr}_ImgH] = Screen('OpenMovie',{cWinStr}, fullfile(cFolder,{addSingleQuotes(cFileNameStr)}) );")
    #
    #     cBeFlipCodes.append(f"Screen('SetMovieTimeIndex', {cWidgetName}_mPtr, {cWidgetName}_sMTime); % skip the first n seconds")
    #     cBeFlipCodes.append(f"Screen('PlayMovie', {cWidgetName}Ptr, {playbackRateStr});")
    #     cBeFlipCodes.append(f"{cItemOrWidgetNameStr}_dRect = makeImDestRect_APL({cItemOrWidgetNameStr}_fRect, [{cItemOrWidgetNameStr}_ImgW, {cItemOrWidgetNameStr}_ImgH], {stretchModeStr});\n")
    #
    #     if re.fullmatch(r"\d+,\d+", durStr):
    #         cBeFlipCodes.append(f"{cWidgetName}_eMTime = min([{cWidgetName}_eMTime, {cWidgetName}_mDur, cDurs({cWinIdx}) - {cWidgetName}_sMTime]);")
    #     else:
    #         cBeFlipCodes.append(f"{cWidgetName}_eMTime = min([{cWidgetName}_eMTime, {cWidgetName}_mDur, cDurs({cWinIdx}) - {cWidgetName}_sMTime]);")
    #
    #     # printAutoInd(cVSLCodes, "if {0}_tPtr > 0 && {0}_CPt < {0}_eMTime", cWidgetName)
    #
    #     if cDotMotionItemNums > 0:
    #         pass
    #         # slider with dot motion items
    #         # printAutoInd(cVSLCodes, "[{0}_temp_tPtr,{0}_temp_CPt] = Screen('GetMovieImage', {1}, {0}_mPtr, 0); %", cWidgetName, cWinStr)
    #         #
    #         # printAutoInd(cVSLCodes, "if {0}_temp_tPtr > 0 ", cWidgetName)
    #         # printAutoInd(cVSLCodes, "{0}_tPtr = {0}_temp_tPtr;", cWidgetName)
    #         # printAutoInd(cVSLCodes, "{0}_CPt  = {0}_temp_CPt; \n", cWidgetName)
    #         #
    #         # printAutoInd(cVSLCodes, "Screen('DrawTexture', {0}, {1}_tPtr, [], {2}_dRect);", cWinStr, cWidgetName, cItemOrWidgetNameStr)
    #         # printAutoInd(cVSLCodes, "{0}_beClosedMIdx = true; % whether to close the current movie texture or not", cWidgetName)
    #         # printAutoInd(cVSLCodes, "else ")
    #         # printAutoInd(cVSLCodes, "{0}_beClosedMIdx = false; % whether to close the current movie texture or not", cWidgetName)
    #         # printAutoInd(cVSLCodes, "end \n")
    #     else:
    #         pass
    #         # slider without  dot motion item and have only one video item | video widget
    #     #     printAutoInd(cVSLCodes, "[{0}_tPtr,{0}_CPt] = Screen('GetMovieImage', {1}, {0}_mPtr, 1); %", cWidgetName, cWinStr)
    #     #     printAutoInd(cVSLCodes, "Screen('DrawTexture', {0}, {1}_tPtr, [], {2}_dRect);", cWinStr, cWidgetName, cItemOrWidgetNameStr)
    #     # printAutoInd(cVSLCodes, "end ")
    #
    # else:
    #     '''
    #     ------------------------------------------------
    #     for slider containing more than one video items
    #     ------------------------------------------------
    #     '''
    #     if Info.PLATFORM == 'linux':
    #         cBeFlipCodes.append("% For linux, to use movie playback and PsychPortAudio at the same time, set specialFlags1 to 2")
    #         cBeFlipCodes.append(f"[{cWidgetName}_mPtrs({iVideoNum}),{cWidgetName}_mDurs({iVideoNum}), ~, {cWidgetName}_ImgWs({iVideoNum}), {cWidgetName}_ImgHs({iVideoNum})] = Screen('OpenMovie', {cWinStr}, fullfile(cFolder,{cFileNameStr}),[],[],2 );")
    #     else:
    #         cBeFlipCodes.append(f"[{cWidgetName}_mPtrs({iVideoNum}),{cWidgetName}_mDurs({iVideoNum}), ~, {cWidgetName}_ImgWs({iVideoNum}), {cWidgetName}_ImgHs({iVideoNum})] = Screen('OpenMovie',{cWinStr}, fullfile(cFolder,{cFileNameStr}) );")
    #
    #     cBeFlipCodes.append(f"{cWidgetName}_sMTimes({iVideoNum}) = {endPositionStr}/1000; ")
    #     cBeFlipCodes.append(f"Screen('SetMovieTimeIndex', {cWidgetName}Ptrs({iVideoNum}), {cWidgetName}_sMTimes({iVideoNum})); % skip the first n seconds")
    #     cBeFlipCodes.append(f"{cWidgetName}_eMTimes({iVideoNum}) = {endPositionStr}/1000; ")
    #     cBeFlipCodes.append(f"Screen('PlayMovie', {cWidgetName}Ptrs({iVideoNum}), {playbackRateStr});")
    #     cBeFlipCodes.append(
    #         f"{cItemOrWidgetNameStr}_dRect = makeImDestRect_APL({cItemOrWidgetNameStr}_fRect, [{cWidgetName}_ImgWs({iVideoNum}), {cWidgetName}_ImgHs({iVideoNum})], {stretchModeStr});\n")
    #
    #     if re.fullmatch(r"\d+,\d+", durStr):
    #         cBeFlipCodes.append(f"{cWidgetName}_eMTimes({iVideoNum}) = min([{cWidgetName}_eMTimes({iVideoNum}), {cWidgetName}_mDurs({iVideoNum}), getDurValue_APL([{durStr}],winIFIs({cWinIdx})) - {cWidgetName}_sMTimes({iVideoNum})]);")
    #     else:
    #         cBeFlipCodes.append(f"{cWidgetName}_eMTimes({iVideoNum}) = min([{cWidgetName}_eMTimes({iVideoNum}), {cWidgetName}_mDurs({iVideoNum}), getDurValue_APL({durStr},winIFIs({cWinIdx})) - {cWidgetName}_sMTimes({iVideoNum})]);")
    #
    #     # printAutoInd(cVSLCodes, "if {0}_tPtrs({1}) > 0 && {0}_CPts({1}) < {0}_eMTimes({1})", cWidgetName, iVideoNum)
    #     # printAutoInd(cVSLCodes, "[{0}_temp_tPtr, {0}_temp_CPt] = Screen('GetMovieImage',{2}, {0}_mPtrs({1}), 0);", cWidgetName, iVideoNum, cWinStr)
    #     # printAutoInd(cVSLCodes, "if {0}_temp_tPtr > 0 ", cWidgetName)
    #     # printAutoInd(cVSLCodes, "{0}_tPtrs({1}) = {0}_temp_tPtr;", cWidgetName, iVideoNum)
    #     # printAutoInd(cVSLCodes, "{0}_CPts({1})  = {0}_temp_CPt; \n", cWidgetName, iVideoNum)
    #     # printAutoInd(cVSLCodes, "Screen('DrawTexture', {0}, {1}_tPtrs({1}), [], {2}_dRect);", cWinStr, iVideoNum, cItemOrWidgetNameStr)
    #     # printAutoInd(cVSLCodes, "{0}_beClosedMIdx({2}) = true; % whether close the current movie texture", cWidgetName, iVideoNum)
    #     # printAutoInd(cVSLCodes, "else ")
    #     # printAutoInd(cVSLCodes, "{0}_beClosedMIdx({2}) = false; % whether close the current movie texture", cWidgetName, iVideoNum)
    #     # printAutoInd(cVSLCodes, "end \n")
    #     #
    #     # printAutoInd(cVSLCodes, "end ")

    printAutoInd(f,"    var {0} = ",cWidgetName)
    f.append("{")
    printAutoInd(f,"type: 'video-keyboard-response',")
    printAutoInd(f,"  stimulus: [{0}]",mypathform(cFileNameStr))
    f.append("};")
    printAutoInd(f,"timeline.push({0});",cWidgetName)
    # if isNotInSlide:
    #     # for video widget , upload the cVSLCodes into allWidgetCodes
    #     allWidgetCodes.update({'forVideoSliderLoopCodes': cVSLCodes})

    # ------------------------------------------
    # the last step: upload the delayed codes
    # ------------------------------------------

    allWidgetCodes.update({'codesBeFip': cBeFlipCodes})

    return allWidgetCodes, cVSLCodes


def drawPngForSliderText(cWidget, f, attributesSetDict, cLoopLevel, cProperties, cVSLCodes):
    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint

    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    # 2) handle the current_text content
    inputStr, isContainRef, _ = getValueInContainRefExp(cWidget, cProperties['Text'], attributesSetDict, True)
    cTextContentStr = parseTextContentStrNew(inputStr)

    # 3) check the alignment X parameter:
    leftX = dataStrConvert(*getRefValue(cWidget, cProperties['Left X'], attributesSetDict))

    # 4) check the alignment X parameter:
    topY = dataStrConvert(*getRefValue(cWidget, cProperties['Top Y'], attributesSetDict))

    # 5) check the color parameter:
    fontColorStr = dataStrConvert(*getRefValue(cWidget, cProperties['Fore Color'], attributesSetDict))
    fontTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Transparent'], attributesSetDict))

    # 6) check the right to left parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Right To Left'], attributesSetDict)
    rightToLeft = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    # 7) set the font name size color style:
    fontName = dataStrConvert(*getRefValue(cWidget, cProperties['Font Family'], attributesSetDict))
    fontSize = dataStrConvert(*getRefValue(cWidget, cProperties['Font Size'], attributesSetDict))
    fontStyle = dataStrConvert(*getRefValue(cWidget, cProperties['Style'], attributesSetDict))
    fontStyle = parseFontStyleStr(fontStyle)

    fontBkColor = dataStrConvert(*getRefValue(cWidget, cProperties['Back Color'], attributesSetDict))

    # isChangeFontPars = False
    #  font name
    # if historyPropDict['fontName'] != fontName:
    #     printAutoInd(f, "Screen('TextFont',{0},{1});", cWinStr, fontName)
    #     historyPropDict.update({'fontName': fontName})
    #     isChangeFontPars = True
    #
    # # font size
    # if historyPropDict['fontSize'] != fontSize:
    #     printAutoInd(f, "Screen('TextSize',{0},{1});", cWinStr, fontSize)
    #     historyPropDict.update({'fontSize': fontSize})
    #     isChangeFontPars = True
    #
    # # font style
    # if historyPropDict['fontStyle'] != fontStyle:
    #     printAutoInd(f, "Screen('TextStyle',{0},{1});", cWinStr, fontStyle)
    #     historyPropDict.update({'fontStyle': fontStyle})
    #     isChangeFontPars = True

    # printAutoInd(cVSLCodes, "Screen('DrawText',{0},{1},{2},{3},{4},{5},{6},{7});",
    #              cWinStr,
    #              cTextContentStr,
    #              leftX,
    #              topY,
    #              addedTransparentToRGBStr(fontColorStr, fontTransparent),
    #              fontBkColor,
    #              0,
    #              rightToLeft)

    # ------------------------------------------
    # the last step: upload the delayed codes
    # ------------------------------------------

    return cVSLCodes


def drawTextForSlider(cWidget, f, attributesSetDict, cLoopLevel, cProperties, cVSLCodes):
    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint

    # cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num

    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    # 2) handle the current_text content
    inputStr, isContainRef, _ = getValueInContainRefExp(cWidget, cProperties['Text'], attributesSetDict, True)
    cTextContentStr = parseTextContentStrNew(inputStr)

    # 3) check the alignment X parameter:
    leftX = dataStrConvert(*getRefValue(cWidget, cProperties['Left X'], attributesSetDict))

    # 4) check the alignment X parameter:
    topY = dataStrConvert(*getRefValue(cWidget, cProperties['Top Y'], attributesSetDict))

    # 5) check the color parameter:
    fontColorStr = dataStrConvert(*getRefValue(cWidget, cProperties['Fore Color'], attributesSetDict))
    fontTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Transparent'], attributesSetDict))

    # 6) check the right to left parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Right To Left'], attributesSetDict)
    rightToLeft = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    # 7) set the font name size color style:
    fontNameStr, isFontNameRef = getRefValue(cWidget, cProperties['Font Family'], attributesSetDict)
    fontName = dataStrConvert(fontNameStr, isFontNameRef)

    fontSizeStr, isFontSizeRef = getRefValue(cWidget, cProperties['Font Size'], attributesSetDict)
    fontSize = dataStrConvert(fontSizeStr, isFontSizeRef )

    fontStyleStr, isFontStyleRef = getRefValue(cWidget, cProperties['Style'], attributesSetDict)
    fontStyle = dataStrConvert(fontStyleStr, isFontStyleRef )
    fontStyle = parseFontStyleStr(fontStyle)

    fontBkColor = dataStrConvert(*getRefValue(cWidget, cProperties['Back Color'], attributesSetDict))

    # printAutoInd(f, "% change the font settings when it's necessary")
    # printAutoInd(f, "changeFontSetting_APL({0}, {1}, {2}, {3}, {4}, true);\n",
    #              cWinStr, fontSize, fontStyle, fontName, fontBkColor)

    # isChangeFontPars = False
    # #  font name
    # if historyPropDict['fontName'] != fontName or isFontNameRef:
    #     printAutoInd(f, "Screen('TextFont',{0},{1});", cWinStr, fontName)
    #     historyPropDict.update({'fontName': fontName})
    #     isChangeFontPars = True
    #
    # # font size
    # if historyPropDict['fontSize'] != fontSize or isFontSizeRef:
    #     printAutoInd(f, "Screen('TextSize',{0},{1});", cWinStr, fontSize)
    #     historyPropDict.update({'fontSize': fontSize})
    #     isChangeFontPars = True
    #
    # # font style
    # if historyPropDict['fontStyle'] != fontStyle or isFontStyleRef:
    #     printAutoInd(f, "Screen('TextStyle',{0},{1});", cWinStr, fontStyle)
    #     historyPropDict.update({'fontStyle': fontStyle})
    #     isChangeFontPars = True

    # printAutoInd(cVSLCodes, "Screen('DrawText',{0},{1},{2},{3},{4},{5},{6},{7});",
    #              cWinStr,
    #              cTextContentStr,
    #              leftX,
    #              topY,
    #              addedTransparentToRGBStr(fontColorStr, fontTransparent),
    #              fontBkColor,
    #              0,
    #              rightToLeft)

    # ------------------------------------------
    # the last step: upload the delayed codes
    # ------------------------------------------

    return cVSLCodes


def drawTextWidget(cWidget, f, attributesSetDict, cLoopLevel):
    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint
    # cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    durStr, isRefValue, cRefValueSet = getRefValueSet(cWidget, cWidget.getDuration(), attributesSetDict)
    cProperties = Func.getWidgetProperties(cWidget.widget_id)
    print("?????????/////")
    print(cProperties)
    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    # 2) handle the current_text content
    inputStr, isContainRef, _ = getValueInContainRefExp(cWidget, cProperties['Text'], attributesSetDict, True)
    cTextContentStr = parseTextContentStrNew(inputStr)

    # 3) check the alignment X parameter:
    alignmentX = dataStrConvert(*getRefValue(cWidget, cProperties['Alignment X'], attributesSetDict))

    # 4) check the alignment X parameter:
    alignmentY = dataStrConvert(*getRefValue(cWidget, cProperties['Alignment Y'], attributesSetDict))

    # 5) check the color parameter:
    fontColorStr = dataStrConvert(*getRefValue(cWidget, cProperties['Fore Color'], attributesSetDict, True))
    print(*getRefValue(cWidget, cProperties['Fore Color'], attributesSetDict, True))
    print(cProperties['Fore Color'])
    print("!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(fontColorStr)
    fontTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Transparent'], attributesSetDict, True))

    # 7) check the flip hor parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Flip Horizontal'], attributesSetDict)
    flipHorStr = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    # 8) check the flip ver parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Flip Vertical'], attributesSetDict)
    flipVerStr = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    # 10) check the right to left parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Right To Left'], attributesSetDict)
    rightToLeft = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    # 11) check the parameter winRect
    # sx = dataStrConvert(*getRefValue(cWidget, cProperties['Center X'], attributesSetDict))
    # sy = dataStrConvert(*getRefValue(cWidget, cProperties['Center Y'], attributesSetDict))
    # cWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Width'], attributesSetDict))
    # cHeight = dataStrConvert(*getRefValue(cWidget, cProperties['Height'], attributesSetDict))
    #
    # frameRectStr = f"makeFrameRect_APL({sx}, {sy}, {cWidth}, {cHeight}, fullRects({cWinIdx},:))"

    # set the font name size color style:
    fontNameStr, isFontNameRef = getRefValue(cWidget, cProperties['Font Family'], attributesSetDict)
    fontName = dataStrConvert(fontNameStr, isFontNameRef)

    fontSizeStr, isFontSizeRef = getRefValue(cWidget, cProperties['Font Size'], attributesSetDict)
    fontSize = dataStrConvert(fontSizeStr, isFontSizeRef)

    fontStyleStr, isFontStyleRef = getRefValue(cWidget, cProperties['Style'], attributesSetDict)
    fontStyle = dataStrConvert(fontStyleStr, isFontStyleRef)
    fontStyle = parseFontStyleStr(fontStyle)

    fontBkColorStr, isFontBkColorRef = getRefValue(cWidget, cProperties['Back Color'], attributesSetDict)
    fontBkColor = dataStrConvert(fontBkColorStr, isFontBkColorRef)

    drawFrameEffect(cWidget, f, cProperties, attributesSetDict)

    cWidgetName = getWidgetName(cWidget.widget_id)
    #  print out the current_text
    cWidgetfontcolor=addedTransparentToRGBStr(fontColorStr, fontTransparent)

    printAutoInd(f,"    var {0} = ",cWidgetName)
    f.append("{")
    printAutoInd(f,"type: 'html-keyboard-response',")
    printAutoInd(f,"  stimulus:  `")
    printAutoInd(f,"<div style='background:{2};display: flex;flex-direction: row;flex-wrap: wrap;justify-content: {0};align-items: {1};'>",alignmentX,alignmentY,fontBkColor)
    printAutoInd(f,"<p><font style=\"color:{2}\" size=\"{0}\" face=\"{1}\" >{3}</font></p></div>",fontSize,fontName[1:-1],cWidgetfontcolor,cTextContentStr)
    printAutoInd(f,"  `,")
    printAutoInd(f,"post_trial_gap: {0}",durStr)
    f.append("};")
    printAutoInd(f,"timeline.push({0});",cWidgetName)
    clearAfter = getClearAfterInfo(cWidget, attributesSetDict)

    # printAutoInd(f, "% give the GPU a break", cWinStr, clearAfter)
    # printAutoInd(f, "Screen('DrawingFinished',{0},{1});\n", cWinStr, clearAfter)
    # printAutoInd(f, "% check the 'esc' key to abort the exp")
    # printAutoInd(f, "detectAbortKey_APL(abortKeyCode);\n")

    return 0


def drawFrameEffect(cWidget, f, cProperties, attributesSetDict):
    global historyPropDict

    cWidgetName = getWidgetName(cWidget.widget_id)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)
    #
    borderColor = dataStrConvert(*getRefValue(cWidget, cProperties['Border Color'], attributesSetDict))
    borderWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Border Width'], attributesSetDict))
    frameFillColor = dataStrConvert(*getRefValue(cWidget, cProperties['Frame Fill Color'], attributesSetDict))
    frameTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Frame Transparent'], attributesSetDict))

    # # get enable parameter
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Enable'], attributesSetDict)
    isBkFrameEnable = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)
    shouldNotBeCitationCheck('Enable', isBkFrameEnable)

    # 7) check the parameter winRect
    sx = dataStrConvert(*getRefValue(cWidget, cProperties['Center X'], attributesSetDict))
    sy = dataStrConvert(*getRefValue(cWidget, cProperties['Center Y'], attributesSetDict))

    cWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Width'], attributesSetDict))
    cHeight = dataStrConvert(*getRefValue(cWidget, cProperties['Height'], attributesSetDict))

    # printAutoInd(f, "{0}_fRect = makeFrameRect_APL({1}, {2}, {3}, {4}, fullRects({5},:));", cWidgetName, sx, sy,
    #              cWidth,
    #              cHeight, cWinIdx)

    isAnyFrameCode = frameFillColor != historyPropDict[f"{cScreenName}_bkColor"] or borderColor != frameFillColor

    if isBkFrameEnable == '1':

        if isAnyFrameCode:
            printAutoInd(f, "% draw background frame ")

        if frameFillColor != historyPropDict[f"{cScreenName}_bkColor"]:
            printAutoInd(f, "Screen('FillRect',{0},{1}, {2}_fRect);", cWinStr,
                         addedTransparentToRGBStr(frameFillColor, frameTransparent), cWidgetName)

        # draw the frame only when the frame color is different from the frame fill color
        if borderColor != frameFillColor:
            printAutoInd(f, "Screen('FrameRect',{0},{1},{2}_fRect,{3});", cWinStr,
                         addedTransparentToRGBStr(frameFillColor, frameTransparent), cWidgetName, borderWidth)

        if isAnyFrameCode:
            printAutoInd(f, "")
    return 0


def compilePTB():
    global cInfoDict
    cInfoDict.clear()

    compileCode(False)

    cInfoDict.clear()


def compileCode(isDummyCompile):
    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, cIndents, historyPropDict, \
        isDummyPrint, spFormatVarDict, cInfoDict, queueDevIdxValueStr, haveGaborStim, haveArcStim, \
        haveSnowStim, haveDotMotion, haveGammaTable, allPossImaFilenameIdxDict, allPossImaWidNameIdxDict, \
        globalAttributesSetDict, questVarNames

    # -----------initialize global variables ------/
    isDummyPrint = isDummyCompile

    cInfoDict.update({'maximumRows': 1})

    allWidgetCodes = {'codesAfFlip': [], 'respCodes': [], 'codesJustBeRespCodes': []}

    historyPropDict = dict()
    globalAttributesSetDict.clear()

    questVarNames = list()

    historyPropDict.update({'clearAfter': "0"})
    historyPropDict.update({'fontName': "simSun"})
    historyPropDict.update({'fontSize': "12"})
    historyPropDict.update({'fontStyle': "0"})
    historyPropDict.update({'fontBkColor': "[259,0,0]"})  # we give the bkcolor an impossible initial value

    cIndents = 0
    cLoopLevel = 0

    addMakeEventResultsVarFun = True
    isGampadWorksInWIn = True

    inputDevNameIdxDict = dict()
    outputDevNameIdxDict = dict()

    enabledKBKeysSet.clear()

    # eventWidgetList = [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO,Info.IF, Info.SWITCH]

    enabledKBKeysSet.add(parseRespKeyCodesStr('{escape}', False, Info.DEV_KEYBOARD))

    # attributesSetDict 0,1,2 for looplevel, becitedStr,all possible values
    attributesSetDict = {'sessionNum': [0, 'subInfo.session', {'subInfo.session'}],
                         'subAge': [0, 'subInfo.age', {'subInfo.age'}],
                         'subName': [0, 'subInfo.name', {'subInfo.name'}],
                         'subGender': [0, 'subInfo.gender', {'subInfo.gender'}],
                         'subNum': [0, 'subInfo.num', {'subInfo.num'}],
                         'runNum': [0, 'subInfo.run', {'subInfo.run'}],
                         'subHandedness': [0, 'subInfo.hand', {'subInfo.hand'}]}
    spFormatVarDict = dict()
    # -------------------------------------------\

    # only replaced percent vars that will be reffed by % with - value /100
    spFormatVarDict = getSpecialFormatAtts()

    # get save path
    finalMfilename = ".".join(Info.FILE_NAME.split('.')[:-1]) + ".html"

    cFilenameOnly = os.path.split(finalMfilename)[1].split('.')[0]

    # fileDirName, baseName = os.path.split(finalMfilename)

    # create sub folder to contain all compiled files
    # os.makedirs(os.path.join(fileDirName, cFilenameOnly), exist_ok=True)

    # finalMfilename = os.path.join(fileDirName, cFilenameOnly, baseName)
    # finalMfilename = os.path.join(fileDirName, baseName)
    # open file 'utf-8'
    encodingFormat = Info.PTB_PREF.get("M File Encoding Format", "GBK")
    with open(finalMfilename, "w", encoding=encodingFormat) as f:
        # with open(finalMfilename, "w", encoding="GBK") as f:
        #  print function start info
        # cFilenameOnly = os.path.split(finalMfilename)[1].split('.')[0]
        # the help info
        printAutoInd(f,"")
        printAutoInd(f,"<!DOCTYPE html>")
        printAutoInd(f, "<!--% function generated by PsyBuilder 0.1")
        printAutoInd(f, "% If you use PsyBuilder for your research, then we would appreciate your citing our work in your paper:")
        printAutoInd(f, "% Lin, Z., Yang, Z., Feng, C., & Zhang, Y. (2021, Nov. 17). ")
        printAutoInd(f, "% PsyBuilder: an open-source cross-platform graphical experiment builder for Psychtoolbox with built-in performance optimization. ")
        printAutoInd(f, "% Advances in Methods and Practices in Psychological Science. Accepted and in press ")
        printAutoInd(f, "% https://doi.org/10.31234/osf.io/b43vx. \n%")
        printAutoInd(f, "% To report possible bugs and any suggestions please feel free to drop me an E-mail:")
        printAutoInd(f, "% Yang Zhang")
        printAutoInd(f, "% Ph.D., Prof.")
        printAutoInd(f, "% Attention and Perception Lab (APL)")
        printAutoInd(f, "% Department of Psychology, \n% SooChow University")
        printAutoInd(f, "% zhangyang873@gmail.com \n% Or\n% yzhangpsy@suda.edu.cn")
        printAutoInd(f, "% {0}", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # begin of the function
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "%      begin      ")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% -->")
        printAutoInd(f,"<html>")
        printAutoInd(f,"  <head>")
        printAutoInd(f,"    <title> experiment {0} </title>", cFilenameOnly)
        printAutoInd(f,"    <script src=\"jspsych-6.3.0/jspsych.js\"></script>")
        printAutoInd(f,"    <script src=\"jspsych-6.3.0/plugins/jspsych-html-keyboard-response.js\"></script>")
        printAutoInd(f,"    <script src=\"jspsych-6.3.0/plugins/jspsych-html-button-response.js\"></script>")
        printAutoInd(f,"    <script src=\"jspsych-6.3.0/plugins/jspsych-html-slider-response.js\"></script>")
        printAutoInd(f,"    <script src=\"jspsych-6.3.0/plugins/jspsych-audio-keyboard-response.js\"></script>")
        printAutoInd(f,"    <script src=\"jspsych-6.3.0/plugins/jspsych-video-keyboard-response.js\"></script>")
        printAutoInd(f,"    <script src=\"jspsych-6.3.0/plugins/jspsych-image-keyboard-response.js\"></script>")
        printAutoInd(f,"    <script src=\"jspsych-6.3.0/plugins/jspsych-preload.js\"></script>")
        printAutoInd(f,"    <link href=\"jspsych-6.3.0/css/jspsych.css\" rel=\"stylesheet\" type=\"text/css\">")
        printAutoInd(f,"  </head>")
        printAutoInd(f,"  <body></body>")
        printAutoInd(f,"  <script>")
        #/* create timeline */
        printAutoInd(f,"    var timeline = [];")
        if not isDummyCompile:
            output_devices = Info.OUTPUT_DEVICE_INFO
            input_devices = Info.INPUT_DEVICE_INFO
            eyetracker_devices = Info.TRACKER_DEVICE_INFO
            quest_devices = Info.QUEST_DEVICE_INFO



            iQuest = 1
            for quest in quest_devices.values():
                attributesSetDict.update(
                    {f"{quest['Device Name']}.cValue": [0, f"questStructs({iQuest})", {f"questStructs({iQuest})"}]})
                questVarNames.append(f"{quest['Device Name']}.cValue")
                iQuest += 1

            if iQuest > 2:
                attributesSetDict.update(
                    {f"randQuestValue": [0, f"questStructs(Randi(numel(questStructs)))", {f"questStructs(Randi(numel(questStructs)))"}]})
                questVarNames.append("randQuestValue")

            # update all global attributesSetDict
            globalAttributesSetDict.update(attributesSetDict)



            allPossImaFilenamesList, allPossImaWidgetNamesList = getAllPossFilenames(1)

            allImSizeMb = getAllImSizeInMb(allPossImaFilenamesList)

            allPossImaFilenameIdxDict = {allPossImaFilenamesList[i]: i+1 for i in range(0, len(allPossImaFilenamesList))}
            allPossImaWidNameIdxDict = {allPossImaWidgetNamesList[i]: i+1 for i in range(0, len(allPossImaWidgetNamesList))}

            imaNamePossWidgetNamesDict = getFilenamePossWidgetsDict(1)

            globalVarEventStr = list2Str(getAllEventWidgetNamesList(1), ' ', False) + ' '
            globalVarAttStr = list2Str(getAllCycleAttVarNameList(), ' ', False)

            if allPossImaFilenamesList:
                globalVarAttStr = globalVarAttStr + " allImaClasses_APL"

            isEyelink = haveTrackerType('EyeLink')

        '''
        running engine check
        '''


        '''
        running operate system (platform) check
        '''

        '''
        get subject information
        '''




        '''
        the function body try, catch end
        '''

        # Psychtoolbox Preference
        # "Visual Debug Level": "-1: Do nothing",
        # "Suppress All Warnings": "No",
        # "Verbosity Level": "4: More useful info (default)"

        visualDebugLevel = parseViusalDebugLevelStr(Info.PTB_PREF.get("Visual Debug Level", "-1: Do nothing"))
        suppressWarning = dataStrConvert(parseBooleanStr(Info.PTB_PREF.get("Suppress All Warnings", "No")))
        syncTestLevel = parseSyncTestLevelStr(Info.PTB_PREF.get("Syncing Test Level", "0: Enable syncing test (default)"))
        triggerSyncDisplays = dataStrConvert(parseBooleanStr(Info.PTB_PREF.get("Trigger Synchronize Displays", "No")))
        suppressKeypressOutput = dataStrConvert(parseBooleanStr(Info.PTB_PREF.get("Suppress Keypress Output", "No")))
        verbosityLevel = parseVerbosityLevelStr(Info.PTB_PREF.get("Verbosity Level", "4: More useful info (default)"))

        if visualDebugLevel > -1 or \
                suppressWarning > 0 or \
                syncTestLevel > 0 or \
                verbosityLevel != 4 or \
                triggerSyncDisplays >0 or \
                suppressKeypressOutput > 0 :
            havePtbPref = True
        else:
            havePtbPref = False

        '''
        handle all possible image files
        '''


        maximumOpDataRows = getMaximumOpDataRows()

        # get output devices, such as global output devices.
        # you can get each widget's device you selected
        # output_devices = Info.OUTPUT_DEVICE_INFO
        # input_devices = Info.INPUT_DEVICE_INFO
        # eyetracker_devices = Info.TRACKER_DEVICE_INFO
        # quest_devices = Info.QUEST_DEVICE_INFO

        if len(eyetracker_devices) == 0:
            pass
        elif len(eyetracker_devices) == 1:

            for cEyeTracker in eyetracker_devices.keys():
                cEyeTrackerProperty = eyetracker_devices[cEyeTracker]
        else:
            throwCompileErrorInfo(f"Currently number of eye tracker devs should be only one !")

        iQuest = 1
        if len(quest_devices) > 0:


            for quest in quest_devices.values():
                outputDevNameIdxDict.update({f"quest-{quest['Device Name']}": f"{iQuest}"})
                # attributesSetDict 0,1,2 for looplevel, becitedStr,all possible values
                # attributesSetDict.update({f"{quest['Device Name']}.cValue": [0, f"questStructs({iQuest}).cValue", {f"questStructs({iQuest}).cValue"}]})
                iQuest += 1


        iKeyboard = 1
        iGamepad = 1
        iRespBox = 1
        iMouse = 1
        iEyetracker = 1
        iQueueDev = 1

        for inputDevId, cDevice in input_devices.items():

            cIsQueue = cDevice.get('Is KB Queue', False)

            if cDevice['Device Type'] == Info.DEV_KEYBOARD:
                cInputDevIndexStr = f"{iKeyboard}"
                iKeyboard += 1

            elif cDevice['Device Type'] == Info.DEV_MOUSE:
                cInputDevIndexStr = f"{iMouse}"
                iMouse += 1

            elif cDevice['Device Type'] == Info.DEV_GAMEPAD:
                # looks like current the gamepad can be queued
                if Info.PLATFORM == 'windows' and cIsQueue and not isGampadWorksInWIn:
                    throwCompileErrorInfo("In windows OS, using Gamepad for Queue is not allowed!\n")
                cInputDevIndexStr = f"{iGamepad}"
                iGamepad += 1

            elif cDevice['Device Type'] == Info.DEV_RESPONSE_BOX:
                cInputDevIndexStr = f"{iRespBox}"
                iRespBox += 1

            elif cDevice['Device Type'] == Info.DEV_EYE_ACTION:
                # only one eye tracker are allow currently
                cInputDevIndexStr = f"{iEyetracker}"
                cDevice.update({'Device Index': cDevice['Tracker Name']})
                iEyetracker += 1

            if cDevice['Device Type'] in [Info.DEV_MOUSE, Info.DEV_KEYBOARD, Info.DEV_GAMEPAD]:
                if cDevice['Device Index'] != 'auto':
                    cInputDevIndexStr = cDevice['Device Index']

            cInputDevIndexValueStr, cDevTypeNum = makeInputDevIndexValueStr(cDevice['Device Type'], cInputDevIndexStr,
                                                                            cDevice['Device Index'] == 'auto')
            inputDevNameIdxDict.update({cDevice['Device Name']: [cInputDevIndexValueStr, int(cIsQueue), cDevTypeNum]})

            if cIsQueue is True:
                queueDevIdxValueStr = cInputDevIndexValueStr
                iQueueDev += 1

        # check input devs
        if Info.PLATFORM == 'windows':
            if iKeyboard > 2:
                throwCompileErrorInfo("In windows OS, only one keyboard is allowed!\n"
                                      " PTB can not address different keyboard devices!")
            elif iMouse > 2:
                throwCompileErrorInfo("In windows OS, only one mouse is allowed!\n"
                                      " PTB can not address different mice!")

        if iEyetracker > 2:
            throwCompileErrorInfo("Currently, we only support Eyelink(we only have a Eyelink1000 for debugging)!\n"
                                  "For Eyelink only one tracker device is allowed!")
        if iQueueDev > 2:
            throwCompileErrorInfo(f"Only one input device is allowed to be used for the KbQueue\n"
                                  f" (You selected {iQueueDev - 1}) devices!")

        iMonitor = 1
        iParal = 1
        iFakePal = 1
        iNetPort = 1
        iSerial = 1
        iSound = 1

        soundDevSlavesDict = getMaxSlaveSoundDevs()

        # if len(soundDevSlavesDict) > 0 and getSpOutDevTypeNum(Info.DEV_SOUND) < 1:
        #     throwCompileErrorInfo("At least one sound device need to be defined for the current project, please specify it in the output under Device menu!")

        for outDev_Id, cDevice in output_devices.items():

            if cDevice['Device Type'] == Info.DEV_SCREEN:
                outputDevNameIdxDict.update({cDevice['Device Name']: f"{iMonitor}"})

                historyPropDict.update({f"{cDevice['Device Name']}_bkColor": addSquBrackets(cDevice['Back Color'])})
                # historyPropDict.update({f"{cDevice['Device Name']}_lastFlipTimeVar": []})
                cDevResList = parsePhysicSize(cDevice['Resolution'])
                # get filename of the gamma table
                cFileNameStr = trans2relativePath(cDevice['Gamma Filename'])
                cFileNameStr = genAppropriatePathSplitter(cFileNameStr, Info.PLATFORM == 'windows')

                if cFileNameStr:
                    haveGammaTable = True

                iMonitor += 1

            elif cDevice['Device Type'] == Info.DEV_NETWORK_PORT:

                outputDevNameIdxDict.update({cDevice['Device Name']: f"tcpipCons({iNetPort})"})
                iNetPort += 1

            elif cDevice['Device Type'] == Info.DEV_PARALLEL_PORT:
                outputDevNameIdxDict.update({cDevice['Device Name']: f"parPort({iParal}).port"})

                if re.findall('^(UBW:)', cDevice['Device Port']):
                    outputDevNameIdxDict.update({f"{cDevice['Device Name']}_fake": f"parPort({iParal}).isFake"})
                    iFakePal += 1

                iParal += 1

            elif cDevice['Device Type'] == Info.DEV_SERIAL_PORT:

                outputDevNameIdxDict.update({cDevice['Device Name']: f"serialCons({iSerial})"})
                iSerial += 1

            elif cDevice['Device Type'] == Info.DEV_SOUND:

                # soundDevSlavesDict = getMaxSlaveSoundDevs()
                cSoundDevNameStr = cDevice['Device Name']

                if soundDevSlavesDict.get(cSoundDevNameStr, 0) > 0:

                    outputDevNameIdxDict.update({cSoundDevNameStr: f"audioDevs({iSound}).slaveIdxes"})
                    outputDevNameIdxDict.update({cSoundDevNameStr+"_fs": f"audioDevs({iSound}).fs"})
                    outputDevNameIdxDict.update({cSoundDevNameStr+"_nChans": f"audioDevs({iSound}).nChans"})
                    iSound += 1
        # if not isDummyCompile:
        # input parameter 2 will include widget type of LOOP
        allEventWidgets = getAllEventWidgetsList(3)
        allLoopWidgetNames = getAllEventWidgetNamesList(2)

        # get length for left just: only evaluate none loop event widgets
        eNamesLJustLen = getWidgetLeftJustLen(getAllEventWidgetsList(1))
        LoopNamesJustLen = getWidgetLeftJustLen(getAllEventWidgetsList(2))

        if not addMakeEventResultsVarFun:
            eNamesLJustLen = eNamesLJustLen + len(f"({maximumOpDataRows},1)")

        for cWidget in allEventWidgets:
            cWidgetType = getWidgetType(cWidget)
            cWidgetName = getWidgetName(cWidget.widget_id)
            cWidgetLoopLevel = getWidLevel(cWidget.widget_id)

            if cWidgetType in stimWidgetTypesList:
                haveRespDev = cWidget.getUsingDeviceCount() > 0

                if addMakeEventResultsVarFun:
                    printAutoInd(f, "")
                else:
                    if haveOutputDevs(cWidget):
                        if haveRespDev:
                            cFrameVarNameStr = 'eventData_resp_msg_APL'
                        else:
                            cFrameVarNameStr = 'eventData_msg_APL'
                    else:
                        if haveRespDev:
                            cFrameVarNameStr = 'eventData_resp_APL'
                        else:
                            cFrameVarNameStr = 'eventData_APL'
        #%%%%%%#
        printTimelineWidget(Info.WID_WIDGET[f"{Info.TIMELINE}.0"], f, attributesSetDict, cLoopLevel, allWidgetCodes)
        printAutoInd(f,"    jsPsych.init(")
        f.write("    {\n")
        printAutoInd(f,"        timeline: timeline")
        f.write("     });\n  </script>\n</html>")
