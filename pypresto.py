from PyQt5.QtWidgets import QApplication
import sys
import os
from winApp import WinApp
from PyQt5 import QtGui
from PyQt5.QtCore import QCoreApplication

ORGANIZATION_NAME = 'Piekill'
ORGANIZATION_DOMAIN = 'piekill.com'
APPLICATION_NAME = 'PyPresto'


def main():
    QCoreApplication.setApplicationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the pyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(
        os.path.join(application_path, "pypresto.png")))

    window = WinApp()
    window.show()
    app.aboutToQuit.connect(window.close_all)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
