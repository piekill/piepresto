**PiePresto** is a desktop client for [PrestoDB](http://prestodb.github.io/) based on [PyHive](https://github.com/dropbox/PyHive) and [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro).

- Works on Mac and Linux.
- Supports ssh tunnel.
- Displays schema including nested structure.
- Syntax highlight and auto completion.
- Query history and result cache.

### How to build

- Python3 (conda env preferred)
- Install dependencies in [requirements.txt](https://github.com/piekill/piepresto/blob/master/requirements.txt)
- Build with pyinstaller
- To conclude, run the following and check `./dist` for binaries:
 ```shell
 git clone https://github.com/piekill/piepresto.git
 cd piepresto
 # conda create -n piepresto python=3.7.3 pip; conda activate piepresto
 pip install -r requirements.txt
 pyinstaller piepresto.spec
 # Note that on Linux you might need: 
 # LD_LIBRARY_PATH=your_path_to_python_lib pyinstaller piepresto.spec
 ```
- Alternatively, go to [release](https://github.com/piekill/piepresto/releases) for pre-built binaries.

### Tunnel config
Refer to the following figure for configuration of ssh tunnel:
```
+-----+         |     +---------+         +--------------+
| URL | <==ssh==|==>  | Gateway |  <===>  | PrestoServer |
+-----+         |     +---------+         +--------------+
```

## Screenshot
![screenshot](https://github.com/piekill/piepresto/blob/master/screenshot.png "Screenshot of PiePresto (MacOS)")
