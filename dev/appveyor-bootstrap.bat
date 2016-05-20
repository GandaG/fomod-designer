@echo off

set PATH=C:\Miniconda-x64;C:\Miniconda-x64\Scripts;%PATH%

conda create -y -n fomod-designer^
 -c https://conda.anaconda.org/mmcauliffe^
 -c https://conda.anaconda.org/anaconda^
 pyqt5=5.5.1 python=3.5.1 lxml=3.5.0
call activate fomod-designer

pip install pip -U
pip install setuptools -U --ignore-installed
pip install -r dev\reqs.txt
