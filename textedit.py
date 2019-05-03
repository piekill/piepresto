from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QCompleter, QMessageBox, QTextEdit

eow = "~!@#$%^&*()+{}|:\"<>?,/;'[]\\-="


class TextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)

        self._completer = None

    def setCompleter(self, c):
        if self._completer is not None:
            self._completer.activated.disconnect()

        self._completer = c

        c.setWidget(self)
        c.setCompletionMode(QCompleter.PopupCompletion)
        c.setCaseSensitivity(Qt.CaseInsensitive)
        c.activated.connect(self.insertCompletion)

    def completer(self):
        return self._completer

    def insertCompletion(self, completion):
        if self._completer.widget() is not self:
            return

        tc = self.textCursor()
        extra = len(completion) - len(self._completer.completionPrefix())
        # tc.movePosition(QTextCursor.Left)
        # tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        selected = tc.selectedText()
        return selected.split(' ')[-1]

    def focusInEvent(self, e):
        if self._completer is not None:
            self._completer.setWidget(self)

        super(TextEdit, self).focusInEvent(e)

    def keyPressEvent(self, e):
        if self._completer is not None and self._completer.popup().isVisible():
            if e.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                e.ignore()
                return

        # isShortcut = (e.modifiers() &
        #               Qt.ControlModifier) != 0 and e.key() == Qt.Key_Bluetooth
        isShortcut = False
        if self._completer is None or not isShortcut:
            super(TextEdit, self).keyPressEvent(e)

        ctrlOrShift = e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)
        if self._completer is None or (ctrlOrShift and len(e.text()) == 0):
            return

        hasModifier = (e.modifiers() != Qt.NoModifier) and not ctrlOrShift
        completionPrefix = self.textUnderCursor()

        if not isShortcut and(
                hasModifier or len(e.text()) == 0 or len(completionPrefix) < 3
                or e.text()[-1] in eow):
            self._completer.popup().hide()
            return

        if completionPrefix != self._completer.completionPrefix():
            self._completer.setCompletionPrefix(completionPrefix)
            self._completer.popup().setCurrentIndex(
                self._completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self._completer.popup().sizeHintForColumn(
            0) + self._completer.popup().verticalScrollBar().sizeHint().width())
        self._completer.complete(cr)
