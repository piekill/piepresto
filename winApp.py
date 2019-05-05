from Ui_mainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QDialogButtonBox, QMessageBox, QTableWidgetItem, QTreeWidget, QTreeWidgetItem
from PyQt5.QtWidgets import QProgressBar, QMenuBar, QAction, QDialog, QHeaderView, QAbstractScrollArea, QFileDialog, QApplication
from PyQt5.QtCore import Qt, QPoint, QDir, QSettings, pyqtSignal

from db import DBEngine
from dblite import DBLite
import syntax
from functools import partial
import pylru
from parser import type_parser
from tunnel import Tunnel
from completer import SQLCompleter
URL = 'URL'
USER = 'USER'
SERVER = 'SERVER'
GATEWAY = 'GATEWAY'
TUNNEL_USER = 'TUNNEL_USER'
KEYFILE = 'KEYFILE'
KEYTYPE = 'KEYTYPE'
TUNNEL_PWD = 'TUNNEL_PWD'


class WinApp(QMainWindow, Ui_MainWindow):
    stmt_signal = pyqtSignal(str)

    def __init__(self):
        super(QMainWindow, self).__init__()

        self.setupUi(self)
        self.connButtonBox.button(QDialogButtonBox.Ok).setText("Connect")
        self.runButtonBox.button(QDialogButtonBox.Ok).setText("Run")
        self.tunnelButton.clicked[bool].connect(self.toggle_tunnel)
        self.tunnelWidget.hide()
        self.keyFileButton.clicked.connect(self.choose_keyfile)
        self.clearButton.clicked.connect(self.clear_tunnel)
        self.keyComboBox.activated[str].connect(self.set_key_type)

        self.db_engine = DBEngine()
        self.db_engine.result_signal.connect(self.show_results)
        self.db_engine.progress_signal.connect(self.set_progress)
        self.db_engine.error_signal.connect(self.show_error)
        self.stmt_signal.connect(self.db_engine.receive_stmt)

        self.db_lite = DBLite()
        self.tunnel = Tunnel()
        self.tunnel_keyfile = ""
        self.data_schema = []
        self.settings = QSettings()
        self.restore_settings()

        history = self.db_lite.history()
        self.historyMenuBar = QMenuBar(self.sqlWidget)
        self.historyMenuBar.setNativeMenuBar(False)
        self.historyMenu = self.historyMenuBar.addMenu(
            '     &History   ⇲    ')
        actions = [QAction(sql, self.historyMenu) for sql in history]
        for action in actions:
            action.triggered.connect(partial(self.use_history, action))
        self.historyMenu.addActions(actions)

        self.history_cache = pylru.lrucache(20, self.remove_action)
        for i in reversed(range(len(history))):
            self.history_cache[history[i]] = actions[i]

        self.historyMenu.setStyleSheet("""
        QMenu {
            max-width: 1000px;
            font-size: 12px;
        }
        """)
        self.historyMenuBar.setStyleSheet("""
        QMenuBar {
            border: None;
        }
        QMenuBar::item {
            background: #404040;
            color: #ffffff;
            border-radius: 4px;
        }
        QMenuBar::item:selected {
            background: rgba(1, 1, 1, 0.2);;
            color: #404040;
            border-radius: 4px;
        }
        """)
        self.sqlWidgetLayout.insertWidget(0, self.historyMenuBar)

        self.connButtonBox.accepted.connect(self.connect)
        self.connButtonBox.rejected.connect(self.disconnect)
        self.runButtonBox.accepted.connect(self.run)
        self.runButtonBox.rejected.connect(self.cancel)
        self.tablesWidget.itemDoubleClicked.connect(self.get_meta)
        self.tablesWidget.itemExpanded.connect(self.get_meta)

        self.progressBar = QProgressBar()
        self.statusbar.addPermanentWidget(self.progressBar)
        self.progressBar.setValue(100)
        QApplication.processEvents()

        self.highlight = syntax.PrestoHighlighter(self.sqlEdit)

        self.dataWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dataWidget.customContextMenuRequested.connect(
            self.show_table_context_menu)
        self.dataWidget.horizontalHeader().setStretchLastSection(False)
        self.dataWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)

        self.schemaView.header().setStretchLastSection(False)
        self.schemaView.header().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.runButtonBox.button(
            QDialogButtonBox.Ok).setShortcut("Ctrl+Return")

        self.completer = SQLCompleter(self)
        self.sqlEdit.setCompleter(self.completer)

        self.set_key_type(self.keyComboBox.currentText())
        self.sqlEdit.setFocus()

    def connect(self):
        self.tablesWidget.clear()
        self.schemaView.clear()
        try:
            if self.serverEdit.text().strip() and self.gatewayEdit.text().strip() and self.tunnelUserEdit.text().strip():
                self.statusbar.showMessage('starting tunnel')
                QApplication.processEvents()
                self.tunnel.start_tunnel(
                    self.serverEdit.text().strip(), self.gatewayEdit.text().strip(),
                    self.tunnelUserEdit.text().strip(), self.keyComboBox.currentText() == 'KeyFile',
                    self.tunnel_keyfile, self.pwdLineEdit.text(),
                    self.urlEdit.text().strip())

            self.statusbar.showMessage('connecting')
            QApplication.processEvents()
            self.db_engine.connect(
                self.urlEdit.text().strip(),
                self.userEdit.text().strip())
            self.statusbar.showMessage('fetching db info')
            QApplication.processEvents()

            dbs = self.db_engine.dbs()
            for db in dbs:
                db_item = QTreeWidgetItem([db])
                db_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
                self.tablesWidget.addTopLevelItem(db_item)
            self.completer.addItems(dbs)
            self.statusbar.showMessage('connected')

        except Exception as err:
            QMessageBox.critical(self, "Error", str(err))
            self.db_engine.close()
            self.statusbar.showMessage('disconnected')

    def disconnect(self):
        self.db_engine.close()
        self.tunnel.stop_tunnel()
        self.schemaView.clear()
        self.tablesWidget.clear()
        self.statusbar.showMessage('disconnected')

    def get_meta(self, item):
        try:
            if item.parent():
                columns = self.db_engine.columns(
                    item.parent().text(0), item.text(0))
                self.set_columns(columns)
                self.completer.addItems([column[0] for column in columns])
            else:
                if item.childCount() <= 0:
                    tables = self.db_engine.tables(item.text(0))
                    item.addChildren([QTreeWidgetItem([table])
                                      for table in tables])
                    self.completer.addTreeItem(item)
        except Exception as err:
            QMessageBox.critical(self, "Error", str(err))

    def set_columns(self, columns):
        try:
            self.schemaView.clear()
            for column in columns:
                column_item = self.type_tree(
                    column[0], type_parser.parse(column[1]))
                self.schemaView.addTopLevelItem(column_item)
            self.schemaView.expandToDepth(2)
            for j in range(self.schemaView.columnCount()):
                self.schemaView.resizeColumnToContents(j)
        except Exception as err:
            QMessageBox.critical(self, "Error", str(err))

    def run(self):
        self.statusbar.showMessage('running')
        self.dataWidget.setRowCount(0)
        self.dataWidget.setColumnCount(0)
        QApplication.processEvents()
        try:
            self.stmt_signal.emit(
                self.sqlEdit.toPlainText().strip().replace(';', ''))
            self.db_engine.start()
        except Exception as err:
            QMessageBox.critical(self, "Error", str(err))

    def show_results(self, results, columns, sql):
        try:
            num_cols = len(columns)
            num_rows = len(results)
            self.dataWidget.setRowCount(num_rows)
            self.dataWidget.setColumnCount(num_cols)
            for i in range(num_rows):
                for j in range(num_cols):
                    self.dataWidget.setItem(
                        i, j, QTableWidgetItem(str(results[i][j])))
            self.dataWidget.resizeColumnsToContents()
            for j in range(num_cols):
                header_label = columns[j][0]
                # header_width = self.fm.width(header_label)
                # if header_width > self.dataWidget.columnWidth(j):
                #     self.dataWidget.setColumnWidth(j, header_width)
                self.dataWidget.setHorizontalHeaderItem(
                    j, QTableWidgetItem(header_label))
            self.data_schema = [column[1] for column in columns]
            self.save_history(sql)
        except Exception as err:
            QMessageBox.critical(self, "Error", str(err))
        finally:
            self.statusbar.showMessage('finished')

    def cancel(self):
        self.db_engine.cancel()

    def set_progress(self, progress):
        self.progressBar.setValue(progress)
        QApplication.processEvents()

    def save_history(self, sql):
        if sql not in self.history_cache:
            action = QAction(sql, self.historyMenu)
            action.triggered.connect(partial(self.use_history, action))
            self.history_cache[sql] = action
        else:
            action = self.history_cache[sql]
            self.historyMenu.removeAction(action)
        self.historyMenu.insertAction(
            self.historyMenu.actions()[0] if (
                self.historyMenu.actions()) else None, action)
        self.db_lite.upsert(sql)

    def use_history(self, action):
        self.sqlEdit.setText(action.text())

    def remove_action(self, sql, action):
        self.historyMenu.removeAction(action)

    def show_table_context_menu(self, position):
        col = self.dataWidget.columnAt(position.x())
        dialog = QDialog(self, Qt.Popup)
        schema_view = QTreeWidget(dialog)
        schema_view.headerItem().setText(0, "Field")
        schema_view.headerItem().setText(1, "Type")
        root = type_parser.parse(self.data_schema[col])
        schema_tree = self.type_tree(
            self.dataWidget.horizontalHeaderItem(col).text(), root)
        schema_view.addTopLevelItem(schema_tree)
        schema_view.expandToDepth(2)
        schema_view.header().setStretchLastSection(False)
        schema_view.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContentsOnFirstShow)
        schema_view.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        schema_view.setMinimumHeight(30)
        schema_view.setMaximumHeight(400)
        schema_view.adjustSize()
        schema_view.setHeaderHidden(True)

        dialog.move(self.dataWidget.mapToGlobal(position) +
                    QPoint(dialog.width() / 5 * 2, dialog.height() + 5))
        dialog.adjustSize()
        dialog.show()

    def type_tree(self, name, root):
        if root.children[0].data == 'primitive_type':
            return QTreeWidgetItem([name, root.children[0].children[0].value])
        elif root.children[0].data == 'row_type':
            root_widget = QTreeWidgetItem([name, 'row'])
            for i in range(len(root.children[0].children) // 2):
                name = root.children[0].children[i * 2].value
                child_type = root.children[0].children[i * 2 + 1]
                root_widget.addChild(self.type_tree(name, child_type))
            return root_widget
        elif root.children[0].data == 'array_type':
            if root.children[0].children[0].children[0].data == 'primitive_type':
                return QTreeWidgetItem(
                    [name, 'array(' + root.children[0].
                     children[0].children[0].children[0].value + ')'])
            else:
                root_widget = QTreeWidgetItem([name, 'array(row)'])
                for i in range(len(root.children[0].children[0].children[0].children) // 2):
                    name = root.children[0].children[0].children[0].children[i * 2].value
                    child_type = root.children[0].children[0].children[0].children[i * 2 + 1]
                    root_widget.addChild(self.type_tree(name, child_type))
                return root_widget

        elif root.children[0].data == 'map_type':
            root_widget = QTreeWidgetItem([name, 'map'])
            key = self.type_tree('_key', root.children[0].children[0])
            value = self.type_tree('_value', root.children[0].children[1])
            root_widget.addChildren([key, value])
            return root_widget
        else:
            pass

    def toggle_tunnel(self, pressed):
        if pressed:
            self.tunnelWidget.show()
            self.repaint()
        else:
            self.tunnelWidget.hide()

    def choose_keyfile(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Choose Key File", QDir.homePath() + "/.ssh", "All Files (*)")
        if file_name:
            self.tunnel_keyfile = file_name
            self.keyFileButton.setText(file_name.split('/')[-1])

    def clear_tunnel(self):
        self.tunnel_keyfile = None
        self.keyFileButton.setText("Choose Key File...")
        self.serverEdit.clear()
        self.gatewayEdit.clear()
        self.tunnelUserEdit.clear()
        self.pwdLineEdit.clear()

    def close_all(self):
        self.save_settings()
        self.db_engine.close()
        self.tunnel.stop_tunnel()

    def restore_settings(self):
        self.urlEdit.setText(self.settings.value(URL, ""))
        self.userEdit.setText(self.settings.value(USER, ""))
        self.serverEdit.setText(self.settings.value(SERVER, ""))
        self.gatewayEdit.setText(self.settings.value(GATEWAY, ""))
        self.tunnelUserEdit.setText(self.settings.value(TUNNEL_USER, ""))
        self.tunnel_keyfile = self.settings.value(KEYFILE, "")
        if self.tunnel_keyfile:
            self.keyFileButton.setText(self.tunnel_keyfile.split('/')[-1])
        self.pwdLineEdit.setText(self.settings.value(TUNNEL_PWD, ""))
        self.keyComboBox.setCurrentText(self.settings.value(KEYTYPE, "KeyFile"))

    def save_settings(self):
        self.settings.setValue(URL, self.urlEdit.text().strip())
        self.settings.setValue(USER, self.userEdit.text().strip())
        self.settings.setValue(SERVER, self.serverEdit.text().strip())
        self.settings.setValue(GATEWAY, self.gatewayEdit.text().strip())
        self.settings.setValue(TUNNEL_USER, self.tunnelUserEdit.text().strip())
        self.settings.setValue(KEYFILE, self.tunnel_keyfile)
        self.settings.setValue(KEYTYPE, self.keyComboBox.currentText())
        self.settings.setValue(TUNNEL_PWD, self.pwdLineEdit.text())
        self.settings.sync()

    def show_error(self, error):
        QMessageBox.critical(self, "Error", error)

    def set_key_type(self, key_type):
        if key_type == 'KeyFile':
            self.pwdLineEdit.hide()
            self.keyFileButton.show()
        else:
            self.keyFileButton.hide()
            self.pwdLineEdit.show()
