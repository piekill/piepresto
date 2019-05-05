**PiePresto** is a desktop client for [PrestoDB](http://prestodb.github.io/) based on [PyHive](https://github.com/dropbox/PyHive) and [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro).

- Works on Mac and Linux.
- Supports ssh tunnel.
- Syntax highlight and auto completion.
- Displays schema including nested structure.

### How to build

- Python3 (conda env preferred)
- Install dependencies in [requirements.txt](https://github.com/piekill/piepresto/blob/master/requirements.txt)
- Build with pyinstaller: `pyinstaller piepresto.spec`