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

    rmtree("dist", ignore_errors=True)
    rmtree("build", ignore_errors=True)


@task(clean)
def build():
    from platform import system, architecture
    from shutil import make_archive, move
    from os import path, curdir, environ
    from configparser import ConfigParser

    try:
        build_number = environ["APPVEYOR_BUILD_NUMBER"]
    except KeyError:
        try:
            build_number = environ["TRAVIS_BUILD_NUMBER"]
        except KeyError:
            build_number = 0

    config = ConfigParser()
    config.read("setup.cfg")

    config.set("bumpversion", "current_build", str(build_number))

    with open('setup.cfg', 'w') as configfile:
        config.write(configfile)

    version = config.get('bumpversion', 'current_version') + "." + build_number

    spec_file = "build-{}.spec".format(system().lower())
    spec_dir = path.join("dev", spec_file)
    zip_name = "designer-{}-{}_{}".format(version, system().lower(), architecture()[0])
    zip_dir = path.join(curdir, "dist")


    run("pyinstaller -w --clean {}".format(spec_dir))
    make_archive(zip_name, "zip", base_dir="FOMOD Designer", root_dir=zip_dir)
    move(zip_name + ".zip", "dist")
