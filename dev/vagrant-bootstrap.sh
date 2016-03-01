#!/usr/bin/env bash

sudo apt-get update

# get git - needed for pyenv

sudo apt-get install -y git
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
 libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev
sudo apt-get install -y python-dev

# shorten the command prompt

echo 'parse_git_branch() {
     git branch 2> /dev/null | sed -e '\''/^[^*]/d'\'' -e '\''s/* \(.*\)/ (\1)/'\''
} 
export PS1="\[\033[38;5;10m\]\u@ \$(parse_git_branch)\w\\$ \[$(tput sgr0)\]"' >> /home/vagrant/.bashrc

parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
export PS1="\[\033[38;5;10m\]\u@ \$(parse_git_branch)\w\\$ \[$(tput sgr0)\]"

# configure git so you don't have to go back and forward all the time.

git config --global user.email "gandaganza@gmail.com"
git config --global user.name "Daniel Nunes"
git config --global core.editor nano

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

pyenv install 2.7.11

# make the virtualenv

pyenv virtualenv 2.7.11 fomod-editor

# install external dependencies

sudo apt-get install -y libxml2-dev libxslt-dev

# install sip from source - package for some reason doesn't work in a venv

originaldir="$PWD"
cd /vagrant || exit
wget http://sourceforge.net/projects/pyqt/files/sip/sip-4.17/sip-4.17.tar.gz
tar xzf sip-4.17.tar.gz
cd sip-4.17 || exit
python configure.py
make
make install
cd ..
rm -rf sip-4.17*
cd "$originaldir" || exit

# install pyqt

sudo apt-get install -y qttools5-dev-tools qtcreator python-pyqt5 pyqt5-dev-tools

# link qt to the venv

cp -r /usr/lib/python2.7/dist-packages/PyQt5 \
 /home/vagrant/.pyenv/versions/fomod-editor/lib/python2.7/site-packages/

# move to the project folder and install the pip reqs

cd /vagrant || exit
pip install -r reqs.txt
