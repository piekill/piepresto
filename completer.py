from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QCompleter
from syntax import PrestoHighlighter

# https://stackoverflow.com/questions/49930534/how-to-use-pyqt5-qcompleter-for-code-completion


class SQLCompleter(QCompleter):
    ConcatenationRole = Qt.UserRole + 1
    sep = '.'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_model()

    def splitPath(self, path):
        return path.split(self.sep)

    def pathFromIndex(self, ix):
        return ix.data(SQLCompleter.ConcatenationRole)

    def create_model(self):
        model = QStandardItemModel(self)
        for key in [
                key
                for key in PrestoHighlighter.keywords + PrestoHighlighter.functions
                if len(key) > 5]:
            item = QStandardItem(key)
            item.setData(key, SQLCompleter.ConcatenationRole)
            model.appendRow(item)
        self.setModel(model)

    def addItems(self, elements):
        for text in elements:
            if not self.model().findItems(text):
                item = QStandardItem(text)
                item.setData(text, SQLCompleter.ConcatenationRole)
                self.model().appendRow(item)

    def addTreeItem(self, parent):
        root = self.model().findItems(parent.text(0))[0]
        for child in [parent.child(i) for i in range(parent.childCount())]:
            item = QStandardItem(child.text(0))
            item.setData(
                parent.text(0) + self.sep + child.text(0),
                SQLCompleter.ConcatenationRole)
            root.appendRow(item)
