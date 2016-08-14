@echo off

C:\Miniconda-x64\Scripts\conda.exe create -y -n fomod-designer^
 -c m-labs^
 pyqt5=5.5.1 python=3.5.1 lxml=3.5.0
call C:\Miniconda-x64\Scripts\activate.bat fomod-designer

pip install pip -U
pip install setuptools -U --ignore-installed
pip install -r dev\requirements.txt
pip install -r dev\test-requirements.txt


C:\Miniconda\Scripts\conda.exe create -y -n fomod-designer^
 -c m-labs^
 pyqt5=5.5.1 python=3.5.1 lxml=3.5.0
call C:\Miniconda\Scripts\activate.bat fomod-designer

pip install pip -U
pip install setuptools -U --ignore-installed
pip install -r dev\requirements.txt
pip install -r dev\test-requirements.txt
