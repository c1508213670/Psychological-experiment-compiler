import re

from PyQt5.QtCore import pyqtSignal, Qt, QDataStream, QIODevice
from PyQt5.QtGui import QKeySequence, QBrush, QColor
from PyQt5.QtWidgets import QShortcut, QTableWidgetItem, QMenu, QInputDialog, QApplication, \
    QAbstractItemView

from app.func import Func
from app.info import Info
from lib import MessageBox, TableWidget
from .attribute_dialog import AttributeDialog
from .attribute_item import AttributeItem
from .repetitions_item import RepetitionsItem
from .timeline_item import TimelineItem


class CycleTable(TableWidget):
    """

    """
    # when timeline is added, emit this signal (widget id, widget_name, index)
    timelineAdded = pyqtSignal(str, str, int)
    timelineDeleted = pyqtSignal(str)

    def __init__(self):
        super(CycleTable, self).__init__(None)
        # col attributes and its default value
        self.attributes = ["Repetitions", "Timeline"]
        self.default_value = {"Repetitions": "1", "Timeline": ""}
        self.alt_key = False
        self.drag_copy_row_col = [-2, -2]
        self.untitled_attribute_count = 1
        # timeline_name : [widget_id, count in this table]
        self.timelines = {}
        # attributes dialog
        self.attribute_dialog = AttributeDialog(self.default_value)
        #
        self.setAcceptDrops(True)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(self.attributes)
        # link signals
        self.linkSignals()
        # set menu and shortcut
        self.setMenuAndShortcut()

    def linkSignals(self):
        """

        @return:
        """
        self.horizontalHeader().sectionDoubleClicked.connect(self.handleHeaderDoubleClicked)
        self.itemChanged.connect(self.handleItemChanged)
        self.attribute_dialog.attributesAdded.connect(self.handleAttributesAdd)
        self.attribute_dialog.attributesChanged.connect(self.handleAttributeChanged)

    def setMenuAndShortcut(self):
        """
        set menu and shortcut
        @return:
        """
        # menu
        self.menu = QMenu()
        # copy action
        self.copy_action = self.menu.addAction(Func.getImageObject("menu/copy.png", 1), "Copy", self.copyActionFunc, QKeySequence())
        self.paste_action = self.menu.addAction(Func.getImageObject("menu/paste.png", 1), "Paste", self.pasteActionFunc, QKeySequence())
        self.insert_row_action = self.menu.addAction(Func.getImageObject("menu/insert_row.png", 1), "Insert Row",  self.insertRowsActionFunc, QKeySequence())
        self.insert_col_action = self.menu.addAction(Func.getImageObject("menu/insert_col.png", 1), "Insert Variable", self.insertAttributesActionFunc, QKeySequence())
        self.delete_rows_action = self.menu.addAction(Func.getImageObject("menu/delete_row.png", 1), "Delete Rows", self.deleteRowsActionFunc, QKeySequence())
        self.delete_cols_action = self.menu.addAction(Func.getImageObject("menu/delete_col.png", 1), "Delete Variables", self.deleteAttributesActionFunc, QKeySequence())
        # shortcut
        self.copy_shortcut = QShortcut(QKeySequence(QKeySequence.Copy), self)
        self.copy_shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        self.copy_shortcut.activated.connect(self.copyActionFunc)
        self.paste_shortcut = QShortcut(QKeySequence(QKeySequence.Paste), self)
        self.paste_shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        self.paste_shortcut.activated.connect(self.pasteActionFunc)

    def addRow(self, index: int = -1):
        """
        add row in timeline
        @param index: row's index, if -1, add in the bottom
        @return:
        """
        if index != -1:
            # insert new row
            self.insertRow(index)
        else:
            index = self.rowCount()
            self.insertRow(index)

        # add items, repetitions, timeline and attributes
        repetitions_item = RepetitionsItem(self.default_value[self.attributes[0]])
        self.setItem(index, 0, repetitions_item)
        timeline_item = TimelineItem()
        self.setItem(index, 1, timeline_item)
        for col in range(2, len(self.attributes)):
            default_value = self.default_value[self.attributes[col]]
            attribute_item = AttributeItem(default_value)
            self.setItem(index, col, attribute_item)

    def deleteRow(self, row: int):
        """
        delete row
        @param row:
        @return:
        """
        # delete row, consider timeline
        timeline = self.item(row, 1).text()
        if timeline:
            self.timelines[timeline][1] -= 1
            if not self.timelines[timeline][1]:
                self.timelineDeleted.emit(self.timelines[timeline][0])
                del self.timelines[timeline]
        self.removeRow(row)

    def addAttribute(self, col: int, attribute_name: str, attribute_value):
        """
        add attribute column
        if col == -1, add last col
        """
        # add new column
        if col == -1:
            col = self.columnCount()
            self.insertColumn(self.columnCount())
        else:
            self.insertColumn(col)
        # set header
        self.setHorizontalHeaderItem(col, QTableWidgetItem(attribute_name))
        # set value
        for row in range(self.rowCount()):
            attribute_item = AttributeItem(attribute_value)
            self.setItem(row, col, attribute_item)
        # related value
        self.attributes.insert(col, attribute_name)
        self.default_value[attribute_name] = attribute_value

    def changeAttributeColumn(self, col: int, attribute_name: str, attribute_value):
        """
        change attribute column: name and default value
        """
        # header
        if attribute_name != self.attributes[col]:
            self.horizontalHeaderItem(col).setText(attribute_name)
            del self.default_value[self.attributes[col]]
        # data
        self.attributes[col] = attribute_name
        self.default_value[attribute_name] = attribute_value
        # value: we just change empty to new default value
        for row in range(self.rowCount()):
            item = self.item(row, col)
            if not item.text():
                item.setText(attribute_value)

    def deleteAttribute(self, col: int):
        """
        delete attribute column
        """
        if col == 0 or col == 1:
            return
        # remove column
        self.removeColumn(col)
        # data
        del self.default_value[self.attributes.pop(col)]

    def renameItem(self, old_timeline_name: str, new_timeline_name: str):
        """
        rename timeline
        """
        self.timelines[new_timeline_name] = self.timelines[old_timeline_name]
        for row in range(self.rowCount()):
            if self.item(row, 1).text() == old_timeline_name:
                self.item(row, 1).setText(new_timeline_name)

    def deleteTimeline(self, timeline: str):
        """
        delete timeline in this cycle
        """
        for row in range(self.rowCount() - 1, -1, -1):
            if self.item(row, 1).text() == timeline:
                # empty timeline in the cycle table instead of delete the whole row
                self.item(row, 1).setText("")
                # self.removeRow(row)
        del self.timelines[timeline]

    def handleItemChanged(self, item):
        """
        when cell changed, we need to make some judgement
        """
        old_edit_triggers = self.editTriggers()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # if text isn't changed, we ignore it
        if item.changed():
            text = item.text()
            if type(item) == RepetitionsItem:
                # only positive number
                if not re.match(Info.RepetitionsPattern[0], text):
                    MessageBox.information(self, "warning", Info.RepetitionsPattern[1])
                    item.redo()
                else:
                    item.save()
            elif type(item) == TimelineItem:
                # empty     => something: maybe add a timeline
                # something => another something: maybe add a timeline, maybe delete a timeline
                # something => empty: maybe delete a timeline
                if not item.old_text:
                    # empty => something, if something is valid and new timeline, emit add signal
                    if not re.match(Info.WidgetPattern[0], text):
                        MessageBox.information(self, "warning", Info.WidgetPattern[1])
                        item.redo()
                    else:
                        if text not in self.timelines:
                            # if it is new timeline in this cycle, but may have existed in other cycles
                            if Func.checkWidgetNameExisted(widget_name=text):
                                MessageBox.information(self, "warning", "Name already exists in other loops.")
                                item.redo()
                            else:
                                # generate new timeline's widget_id
                                widget_id = Func.generateWidgetId(Info.TIMELINE)
                                self.timelineAdded.emit(widget_id, text, -1)
                                # self.timelineAdded.emit(widget_id, text, len(self.timelines))
                                self.timelines[text] = [widget_id, 1]
                                item.save()
                        else:
                            self.timelines[text][1] += 1
                            item.save()
                else:
                    if text:
                        # something => another something
                        if not re.match(Info.WidgetPattern[0], text):
                            MessageBox.information(self, "warning", Info.WidgetPattern[1])
                            item.redo()
                        else:
                            if text not in self.timelines:
                                # new timeline in this cycle
                                if Func.checkWidgetNameExisted(widget_name=text):
                                    # valid
                                    MessageBox.information(self, "warning", "Name already exists in other loops.")
                                    item.redo()
                                else:
                                    # generate new timeline's widget_id
                                    widget_id = Func.generateWidgetId(Info.TIMELINE)
                                    self.timelineAdded.emit(widget_id, text, -1)
                                    self.timelines[text] = [widget_id, 1]
                                    # secondly check old current_text
                                    self.timelines[item.old_text][1] -= 1
                                    if self.timelines[item.old_text][1] <= 0:
                                        # if user delete all this timeline, we delete data
                                        self.timelineDeleted.emit(self.timelines[item.old_text][0])
                                        del self.timelines[item.old_text]
                                    item.save()
                            else:
                                # simply change data and check old current_text
                                self.timelines[text][1] += 1
                                self.timelines[item.old_text][1] -= 1
                                if not self.timelines[item.old_text][1]:
                                    # if user delete all this timeline, we delete data
                                    self.timelineDeleted.emit(self.timelines[item.old_text][0])
                                    del self.timelines[item.old_text]
                                item.save()
                    else:
                        # something => empty
                        self.timelines[item.old_text][1] -= 1
                        if not self.timelines[item.old_text][1]:
                            # if user delete all this timeline, we delete data
                            self.timelineDeleted.emit(self.timelines[item.old_text][0])
                            del self.timelines[item.old_text]
                        item.save()
            elif type(item) == AttributeItem:
                if re.search(r"^\[.*?\]", text):
                    item.setForeground(QBrush(QColor(0, 0, 255)))
                else:
                    item.setForeground(QBrush(QColor(0, 0, 0)))
        self.setEditTriggers(old_edit_triggers)

    def handleHeaderDoubleClicked(self, col: int):
        """

        """
        name = self.attributes[col]
        value = self.default_value[name]
        self.attribute_dialog.showWindow(0, col, name, value)

    def handleAttributesAdd(self, col: int):
        """
        when user want to add new attributes
        """
        attributes = self.attribute_dialog.getAttributes()
        for name, value in attributes:
            self.addAttribute(col, name, value)

    def handleAttributeChanged(self, col: int, attribute_name: str, attribute_value: str):
        """
        when user change some attribute
        """
        if col in (0, 1):
            return
        self.changeAttributeColumn(col, attribute_name, attribute_value)

    def mouseMoveEvent(self, e):
        """
        when dragging the mouse while holding down alt/option
        @param e:
        @return:
        """
        super(CycleTable, self).mouseMoveEvent(e)
        if e.modifiers() == Qt.AltModifier:
            if not self.alt_key:
                row = self.rowAt(e.pos().y())
                col = self.columnAt(e.pos().x())
                if row != -1 and col != -1:
                    self.drag_copy_row_col = [row, col]
                    self.alt_key = True
                    self.setCursor(Qt.CrossCursor)
        # elif e.modifiers() == Qt.AltModifier | Qt.ControlModifier:
        #     self.alt_key = False
        #     self.unsetCursor()

    def mouseReleaseEvent(self, e):
        """
        if mouse pressed with alt
        """
        super(CycleTable, self).mouseReleaseEvent(e)
        if self.alt_key:
            self.alt_key = False
            self.unsetCursor()
            # get range
            start_row, col = self.drag_copy_row_col
            end_row = start_row
            # copy data in selected col
            if self.selectedRanges():
                select_range = self.selectedRanges()[0]
                end_row = select_range.topRow()
                if end_row == start_row:
                    end_row = select_range.bottomRow()
            # copy
            text = self.item(start_row, col).text()
            deleted_texts = []
            if start_row < end_row:
                # drag down
                for row in range(start_row + 1, end_row + 1):
                    item = self.item(row, col)
                    if col == 1 and item.text():
                        deleted_texts.append(item.text())
                    item.setText(text)
            elif start_row > end_row:
                # drag up
                for row in range(end_row, start_row):
                    item = self.item(row, col)
                    if col == 1 and item.text():
                        deleted_texts.append(item.text())
                    item.setText(text)
            # if col == 1, namely user change timeline, we need to check and update data
            # change data
            if col == 1 and text:
                self.timelines[text][1] += abs(end_row - start_row)
            for deleted_text in deleted_texts:
                self.timelines[deleted_text][1] -= 1
                if not self.timelines[deleted_text][1]:
                    # if user delete all this timeline, we delete data
                    self.timelineDeleted.emit(self.timelines[deleted_text][0])
                    del self.timelines[deleted_text]

    def contextMenuEvent(self, e):
        """
        right mouse menu
        """
        # delete row/col, insert row/col, copy, paste
        selected = len(self.selectedRanges())
        if selected:
            self.delete_rows_action.setEnabled(True)
            self.delete_cols_action.setEnabled(True)

            if selected > 1:
                self.insert_row_action.setEnabled(False)
                self.insert_col_action.setEnabled(False)
            else:
                self.insert_row_action.setEnabled(True)
                left = self.selectedRanges()[0].leftColumn()
                if left == 0 or left == 1:
                    self.insert_col_action.setEnabled(False)
                else:
                    self.insert_col_action.setEnabled(True)
            self.copy_action.setEnabled(True)
            self.paste_action.setEnabled(True)
        else:
            self.delete_rows_action.setEnabled(False)
            self.delete_cols_action.setEnabled(False)
            self.insert_row_action.setEnabled(False)
            self.insert_col_action.setEnabled(False)
            self.copy_action.setEnabled(False)
            self.paste_action.setEnabled(False)
        self.menu.exec(self.mapToGlobal(e.pos()))

    def addRowsActionFunc(self):
        """
        add rows through a dialog
        """

        rows, ok = QInputDialog(flags=Qt.WindowCloseButtonHint).getInt(self, "Add Rows",
                                                                       "How many rows to add? ", 1, 1,
                                                                       100, 1)
        if ok:
            # if user press ok
            while rows:
                self.addRow()
                rows -= 1

    def insertRowsActionFunc(self):
        """
        insert row above of the selected range
        """
        top = self.selectedRanges()[0].topRow()
        self.addRow(top)

    def deleteRowsActionFunc(self):
        """
        func to delete rows action
        """
        # get select rows
        delete_rows = [0 for i in range(self.rowCount())]
        for select_range in self.selectedRanges():
            for row in range(select_range.topRow(), select_range.bottomRow() + 1):
                delete_rows[row] = 1
        # delete rows (reverse)
        for row in range(len(delete_rows) - 1, -1, -1):
            if delete_rows[row]:
                self.deleteRow(row)

    def addAttributeActionFunc(self):
        """
        add attribute
        """
        self.attribute_dialog.showWindow(0)

    def addAttributesActionFunc(self):
        """
        add attribute
        """
        self.attribute_dialog.showWindow(1)

    def changeAttributeActionFunc(self):
        """
        add attribute
        """
        self.attribute_dialog.showWindow(0)

    def insertAttributesActionFunc(self):
        """
        insert col left of the selected range
        """
        left = self.selectedRanges()[0].leftColumn()
        self.attribute_dialog.showWindow(0, left)

    def deleteAttributesActionFunc(self):
        """
        func to delete rows action
        """
        # get select cols
        delete_cols = [0 for i in range(self.columnCount())]
        for select_range in self.selectedRanges():
            for col in range(select_range.leftColumn(), select_range.rightColumn() + 1):
                delete_cols[col] = 1
        # delete col (reverse)
        for col in range(len(delete_cols) - 1, -1, -1):
            if delete_cols[col]:
                self.deleteAttribute(col)

    def copyActionFunc(self):
        """
        copy data from table
        """
        # get system's clipboard
        clipboard = QApplication.clipboard()
        # get all selected items
        items = self.selectedItems()
        if items:
            # check the validity of selected items, selected columns must be the same
            # get length, left and right col
            first_item = items[0]
            left = first_item.column()
            current_row = first_item.row()
            rows = [[first_item]]
            length = 1
            for item in items[1:]:
                if item.row() == current_row:
                    rows[0].append(item)
                    length += 1
                else:
                    break
            right = items[length - 1].column()
            # classify remainder items and check validity of selected areas
            current_length = length
            for i in range(length, len(items)):
                item = items[i]
                if item.row() == current_row:
                    current_length += 1
                    rows[-1].append(item)
                else:
                    # check validity
                    if item.column() != left or current_length != length or items[i - 1].column() != right:
                        MessageBox.information(self, "Warning",
                                               "This operation can't be performed on multiple selection areas.")
                    # update
                    current_length = 1
                    current_row = item.row()
                    rows.append([item])
            # check last row
            if current_length != length or items[-1].column() != right:
                MessageBox.information(self, "Warning",
                                       "This operation can't be performed on multiple selection areas.")

            copy_text = ""
            for row in rows:
                for i in range(length):
                    item = row[i]
                    if i == length - 1:
                        if row == rows[-1]:
                            copy_text = copy_text + item.text()
                        else:
                            copy_text = copy_text + item.text() + "\n"
                    else:
                        copy_text = copy_text + item.text() + "\t"
            # output to system's clipboard
            clipboard.setText(copy_text)

    def pasteActionFunc(self):
        """
        paste data to table
        """
        # check the validity of selected area
        select_ranges = self.selectedRanges()
        # none area
        if not len(select_ranges):
            return
        # many areas
        if len(select_ranges) != 1:
            MessageBox.information(self, 'Warning', "This operation can't be performed on multiple selection areas.")
            return
        # get start pos
        start_row = select_ranges[0].topRow()
        start_col = select_ranges[0].leftColumn()
        # get paste current_text from system's clipboard
        clipboard = QApplication.clipboard()
        paste_text = clipboard.text()
        # if current_text is none, we ignore it
        if not paste_text:
            return
        # we only allow excel-like formats
        # check the number of columns of each row is the same firstly
        cols_count = 0
        rows = re.split(r"\n", paste_text)
        # under windows, the data ends with \n, so an invalid \n will be added, which needs to be deleted
        if not rows[-1]:
            rows.pop(-1)
        # split data of each row
        pasted_rows = []
        for row in rows:
            pasted_row = re.split(r'\t', row)
            if not cols_count:
                cols_count = len(pasted_row)
            else:
                if len(pasted_row) != cols_count:
                    MessageBox.information(self, "Warning", "Cols split by '\\t' of each row must be same!")
                    return
            pasted_rows.append(pasted_row)
        # traverse rows_data to cols_data
        pasted_cols = [[] for i in range(cols_count)]
        for i in range(len(pasted_rows)):
            pasted_row = pasted_rows[i]
            for j in range(cols_count):
                # we need format the data
                pasted_cols[j].append(re.sub(r"\r", "", pasted_row[j]))
        # if it affects the repetitions/timeline column, we need to check the value
        end_row = start_row + len(rows) - 1
        end_col = start_col + cols_count - 1
        # add new row into table
        for i in range(self.rowCount(), end_row + 1):
            self.addRow()
        if not start_col:
            # if it affect repetitions column, we only allow positive num
            repetitions_values = pasted_cols[0]
            for repetitions_value in repetitions_values:
                if not re.match(Info.RepetitionsPattern[0], repetitions_value):
                    MessageBox.information(self, "warning", Info.RepetitionsPattern[1])
                    return
        if (not start_col and cols_count > 1) or start_col == 1:
            # if it affect repetitions column, we need to check the value
            timeline_col = 1
            if start_col == 1:
                timeline_col = 0
            timeline_names = pasted_cols[timeline_col]
            for timeline_name in timeline_names:
                # we ignore empty
                if timeline_name:
                    if not re.match(Info.WidgetPattern[0], timeline_name):
                        MessageBox.information(self, "warning", Info.WidgetPattern[1])
                        return
            # now we add timelines into table
            timeline_counter = {}
            for row in range(start_row, end_row + 1):
                old_timeline_name = self.item(row, 1).text()
                if old_timeline_name:
                    if old_timeline_name in timeline_counter:
                        timeline_counter[old_timeline_name] -= 1
                    else:
                        timeline_counter[old_timeline_name] = -1
                new_timeline_name = timeline_names[row - start_row]
                # we ignore empty
                if new_timeline_name:
                    if new_timeline_name in timeline_counter:
                        timeline_counter[new_timeline_name] += 1
                    else:
                        timeline_counter[new_timeline_name] = 1
            # handle timeline counter
            for timeline_name in timeline_counter:
                if timeline_name in self.timelines:
                    self.timelines[timeline_name][1] += timeline_counter[timeline_name]
                    if not self.timelines[timeline_name][1]:
                        # if count of this timeline is zero, we need to delete it
                        self.timelineDeleted.emit(self.timelines[timeline_name][0])
                        del self.timelines[timeline_name]
                else:
                    widget_id = Func.generateWidgetId(Info.TIMELINE)
                    self.timelineAdded.emit(widget_id, timeline_name, -1)
                    self.timelines[timeline_name] = [widget_id, timeline_counter[timeline_name]]
        # add attributes and fill text
        for col in range(start_col, end_col + 1):
            data_col = col - start_col
            if col > self.columnCount() - 1:
                self.addAttribute(-1, f"untitled_var_{self.untitled_attribute_count}", pasted_cols[data_col][0])
                self.untitled_attribute_count += 1
            for row in range(start_row, end_row + 1):
                data = pasted_cols[data_col][row - start_row]
                self.item(row, col).setText(data)

    def dragEnterEvent(self, e):
        """

        """
        if e.mimeData().hasFormat(Info.AttributesToWidget):
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        """

        """
        e.accept()

    def dropEvent(self, e):
        """
        drop in table
        """
        if e.mimeData().hasFormat(Info.AttributesToWidget):
            # get pos
            row = self.rowAt(e.pos().y())
            col = self.columnAt(e.pos().x())
            # can't be repetitions and timeline
            if row != -1 and col >= 2:
                data = e.mimeData().data(Info.AttributesToWidget)
                stream = QDataStream(data, QIODevice.ReadOnly)
                text = f"[{stream.readQString()}]"
                self.item(row, col).setText(text)
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()

    def store(self) -> dict:
        """
        store this widget
        """
        table = [[] for i in range(self.columnCount())]
        for col in range(self.columnCount()):
            for row in range(self.rowCount()):
                table[col].append(self.item(row, col).text())
        return {
            "attributes": self.attributes,
            "default_value": self.default_value,
            "untitled_attribute_count": self.untitled_attribute_count,
            "timelines": self.timelines,
            "table": table
        }

    def restore(self, data: dict):
        """
        restore this widget
        """
        self.attributes = data["attributes"]
        self.default_value = data["default_value"]
        self.attribute_dialog.updateExistAttributes(self.default_value)
        # = AttributeDialog(self.default_value)
        self.untitled_attribute_count = data["untitled_attribute_count"]
        self.timelines = data["timelines"]
        table = data["table"]
        # set row, col and headers
        self.setRowCount(len(table[0]))
        self.setColumnCount(len(table))
        self.setHorizontalHeaderLabels(self.attributes)
        # restore each items
        for col in range(self.columnCount()):
            for row in range(self.rowCount()):
                text = table[col][row]
                if col == 0:
                    item = RepetitionsItem(text)
                elif col == 1:
                    item = TimelineItem()
                else:
                    item = AttributeItem(text)
                self.setItem(row, col, item)
                self.item(row, col).setText(text)
