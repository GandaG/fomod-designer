#!/usr/bin/env bash

# Copyright 2016 Daniel Nunes
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# get pyenv - I hate messing with system python on ubuntu

git clone https://github.com/yyuu/pyenv.git $HOME/.pyenv

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"


# get pyenv-virtualenv instead of plain old virtualenv

git clone https://github.com/yyuu/pyenv-virtualenv.git \
 $HOME/.pyenv/plugins/pyenv-virtualenv

eval "$(pyenv virtualenv-init -)"


# start installing the python versions

env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install miniconda3-3.19.0


# make the virtualenv

pyenv shell miniconda3-3.19.0
conda create -y -n fomod-designer \
 -c https://conda.anaconda.org/mmcauliffe \
 -c https://conda.anaconda.org/anaconda \
 python=3.5.1 pyqt5=5.5.1 lxml=3.5.0
pyenv shell miniconda3-3.19.0/envs/fomod-designer


# install the pip reqs

pip install pip -U
pip install setuptools -U --ignore-installed
pip install -r dev/reqs.txt
