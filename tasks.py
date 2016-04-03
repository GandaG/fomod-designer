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
def create():
    run("vagrant up", pty=True)


@task
def reload():
    run("vagrant destroy -f", pty=True)
    create()


@task
def enter():
    import os
    os.system("vagrant ssh -- -Yt 'cd /vagrant/; /bin/bash'")


@task
def genui():
    from PyQt5 import uic
    from os.path import join

    uic.compileUiDir(join("fomod", "gui", "templates"))


@task
def clean():
    from shutil import rmtree

    rmtree("dist")
    rmtree("build")


@task(clean)
def build():
    from platform import system, architecture
    from shutil import make_archive, move
    from os import path, curdir
    from fomod import __version__

    spec_file = "build-{}.spec".format(system().lower())
    zip_name = "designer-{}-{}_{}".format(__version__, system().lower(), architecture()[0])
    zip_dir = path.join(curdir, "dist", "FOMOD Designer")

    run("pyinstaller -w --clean {}".format(spec_file))
    make_archive(zip_name, "zip", base_dir=zip_dir)
    move(zip_name + ".zip", "dist")
