2.2.0
-----
The is a minor release:

* Improve documentation (README.rst).
* Add test suite on Linux and Windows, setup Travis and Appveyor.
* Add support for Nemo file manager (Linux/Cinnamon).
* Add support for Caja file manager (Linux/MATE).
* Add option to select a specific file manager (Linux).
* Remove unnecessary dependencies.
* Add support for Dolphin file manager (Linux/KDE).

2.1.0
-----
The is a minor release:

* Add support for MacOSX.
* Fix path to python for running scripts on gnome.

2.0.0
-----
The is a major release changing the API:

* Merge installation and removal command into one single commands
  ``start_jupyter_cm`` that takes a ``--remove`` argument.
* Add test suite and continuous integration in travis and appveyor.

1.4.0
-----
* Add support for conda environment on linux.
* Create shortcut only when the executable is installed.
* Drop python 2.7 support.
* Update documentation (README.rst) and installation instructions.

1.3.1
-----
* Tidy up setup scripts to fix conda-forge build on windows

1.3.0
-----
* Add support for single user installation on windows.
* Add support for conda environment on windows.

1.2.0
-----
* Add Jupyter lab entry.
* Change deprecated `gvfs-set-attribute` attribute to `gio set` for gnome.

1.1.2
-----
* Add global variable start_jupyter_cm.windows.WPSCRIPTS_FOLDER to define the WinPython scripts folder.

1.1.0
-----
* Add support for WinPython
* Open jupyter notebook inside selected folder instead of parent directory.
