#!/usr/bin/env python

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

from invoke import task, run


@task
def reload():
    run("vagrant destroy -f && vagrant up")


@task
def enter():
    run("vagrant ssh -- -Xt 'cd /vagrant/; /bin/bash'")


@task
def genui():
    from PyQt5 import uic
    uic.compileUiDir("fomod/gui/templates")


@task
def clean():
    run("rm -rf dist/")
    run("rm -rf build/")


@task(clean)
def build():
    import platform
    import fomod

    if platform.system() == "Linux":
        run("pyinstaller -w --clean build-linux.spec")

    elif platform.system() == "Windows":
        run("pyinstaller -w --clean build-windows.spec")
        run("cd .\dist\ && "
            "7z a designer-{}-windows_{}.zip \".\\FOMOD Designer\" && cd ..".format(fomod.__version__,
                                                                                    platform.architecture()[0]))
        return

    else:
        run("pyinstaller -w --clean dev/pyinstaller-bootstrap.py")

    run("(cd dist/; zip -r designer-{}-{}_{}.zip 'FOMOD Designer')".format(fomod.__version__,
                                                                           platform.system().lower(),
                                                                           platform.architecture()[0]))
