from pyhive import presto
from PyQt5.QtCore import QThread, pyqtSignal
from timeout import timeout


class DBEngine(QThread):
    result_signal = pyqtSignal(list, list, str)
    progress_signal = pyqtSignal(float)
    error_signal = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.connection = None
        self.cursor = None
        self.stmt = None

    def receive_stmt(self, stmt):
        self.stmt = stmt

    def run(self):
        if not self.connection:
            self.error_signal.emit("No Connection")
            return
        results, columns = self.query(self.stmt)
        if not results or not columns:
            results = []
            columns = []
        self.result_signal.emit(results, columns, self.stmt)

    def connect(self, url, user):
        self.close()
        host_port = url.split(':')
        if len(host_port) < 2:
            raise Exception("Url Port Not Specified")
        self.connection = presto.connect(
            host=host_port[0], port=host_port[1], username=user)

    def report_status(self):
        self.progress_signal.emit(0.0)
        while True:
            try:
                status = self.cursor.poll()
                if status is None:
                    break
                self.progress_signal.emit(
                    status['stats']['progressPercentage'])
            except KeyError:
                self.progress_signal.emit(0.0)
            except Exception as err:
                pass
        self.progress_signal.emit(100.0)

    def cancel(self):
        self.cursor.cancel()

    def query(self, stmt):
        self.cursor = self.connection.cursor()
        self.cursor.execute(stmt)
        self.report_status()
        results = self.cursor.fetchmany(100)
        columns = self.cursor.description
        self.cursor.close()
        return results, columns

    @timeout(6, "Fail to establish connection")
    def dbs(self):
        if not self.connection:
            raise Exception("No Connection")
        self.cursor = self.connection.cursor()
        self.cursor.execute("SHOW SCHEMAS")
        self.report_status()
        return [str(db[0]) for db in self.cursor.fetchall()]

    def tables(self, db):
        self.cursor = self.connection.cursor()
        self.cursor.execute("SHOW TABLES FROM " + db)
        self.report_status()
        return [str(table[0]) for table in self.cursor.fetchall()]

    def columns(self, db, table):
        self.cursor = self.connection.cursor()
        self.cursor.execute("SHOW COLUMNS FROM " + db + "." + table)
        self.report_status()
        return [[str(column[0]), str(column[1])]
                for column in self.cursor.fetchall()]

    def close(self):
        if self.connection:
            self.connection.close()

    def __del__(self):
        self.close()
