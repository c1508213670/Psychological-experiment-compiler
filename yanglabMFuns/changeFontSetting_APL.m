
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
% subfun {0}: changeFontSetting_APL", iSubFunNum)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

changeFontSetting_APL(winIdx, fontSize, fontStyle, fontName, bkColor,isSingleDraw)
persistent oldSize oldStyle oldName OldBkColor

if ~isequal(fontSize,oldSize)
    Screen('TextFont',winIdx, size);
    oldSize = fontSize;
end

if ~isequal(fontStyle, oldStyle)
    Screen('TextStyle',winIdx, fontStyle);
    oldStyle = fontStyle;
end

if ~strcmp(fontName,oldName)
    Screen('TextFont',winIdx, fontStyle);
    oldName = fontName;
end

if isSingleDraw
    OldBkColor = bkColor;
elseif ~isequal(bkColor,OldBkColor)
    Screen('TextBackgroundColor',winIdx, bkColor);
    OldBkColor = bkColor;
end
end
