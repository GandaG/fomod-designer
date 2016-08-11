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

sudo apt-get update


# fix locale issues
{
    echo 'export LANGUAGE=en_US.UTF-8'
    echo 'export LANG=en_US.UTF-8'
    echo 'export LC_ALL=en_US.UTF-8'
    echo 'export LC_CTYPE="en_US.UTF-8"'
} >> /home/vagrant/.bashrc

locale-gen en_US.UTF-8
sudo dpkg-reconfigure locales


# get git - needed for pyenv
sudo apt-get install -y git git-flow
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
 libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev


# shorten the command prompt
echo 'parse_git_branch() {
     git branch 2> /dev/null | sed -e '\''/^[^*]/d'\'' -e '\''s/* \(.*\)/ (\1)/'\''
} 
export PS1="\[\033[38;5;10m\]\u@ \$(parse_git_branch)\w\\$ \[$(tput sgr0)\]"' >> /home/vagrant/.bashrc

parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
export PS1="\[\033[38;5;10m\]\u@ \$(parse_git_branch)\w\\$ \[$(tput sgr0)\]"


# install p4merge
wget http://cdist2.perforce.com/perforce/r15.2/bin.linux26x86_64/p4v.tgz
tar zxvf p4v.tgz
sudo mv p4v-* /opt/p4v
sudo ln -s /opt/p4v/bin/p4merge /usr/local/bin/p4merge


# configure git so you don't have to go back and forward all the time.
python3 - <<END
#!/usr/bin/env python
from configparser import ConfigParser
from os import system

default_settings = {"git": {"user": "",
                            "email": ""}}
config = ConfigParser()
config.read_dict(default_settings)
config.read("/vagrant/.settings")
if config["git"]["user"]:
    print("Git user defined as " + config["git"]["user"])
    system("git config --global user.name \"{}\"".format(config["git"]["user"]))
else:
    print("No git user defined. Please check the readme.")
if config["git"]["email"]:
    print("Git email defined as " + config["git"]["email"])
    system("git config --global user.email \"{}\"".format(config["git"]["email"]))
else:
    print("No git email defined. Please check the readme.")
END
git config --global core.editor nano
git config --global push.default simple
git config --global credential.helper 'cache --timeout=18000'
git config --global alias.l "log --decorate --oneline --graph"
git config --global alias.st status
git config --global alias.ci commit
git config --global merge.keepBackup false
git config --global merge.tool p4merge
git config --global mergetool.prompt false
git config --global mergetool.p4merge.cmd 'p4merge "$BASE" "$LOCAL" "$REMOTE" "$MERGED"'
git config --global mergetool.p4merge.keepTemporaries false
git config --global mergetool.p4merge.trustExitCode false
git config --global mergetool.p4merge.keepBackup false
git config --global diff.tool p4merge
git config --global difftool.prompt false
git config --global difftool.p4merge.cmd 'p4merge "$LOCAL" "$REMOTE"'
git config --global difftool.p4merge.keepTemporaries false
git config --global difftool.p4merge.trustExitCode false
git config --global difftool.p4merge.keepBackup false


# get pyenv - I hate messing with system python on ubuntu
git clone https://github.com/yyuu/pyenv.git /home/vagrant/.pyenv
{
    echo 'export PYENV_ROOT="$HOME/.pyenv"'
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"'
    echo 'eval "$(pyenv init -)"' 
} >> /home/vagrant/.bashrc

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"


# get pyenv-virtualenv instead of plain old virtualenv
git clone https://github.com/yyuu/pyenv-virtualenv.git \
 /home/vagrant/.pyenv/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> /home/vagrant/.bashrc
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


# move to the project folder and install the pip reqs
cd /vagrant || exit
pip install pip -U
pip install setuptools -U --ignore-installed
pip install -r dev/reqs.txt
