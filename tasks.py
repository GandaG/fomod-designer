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
def gen_ui():
    from os import listdir, remove
    from os.path import join, isfile
    from PyQt5.uic import compileUiDir

    target_dir = "designer/ui_templates"
    init_fname = "__init__.py"
    for item in listdir(target_dir):
        if item != init_fname and isfile(join(target_dir, item)):
            remove(join(target_dir, item))
    compileUiDir("resources/templates", map=lambda dir, fname: (target_dir, fname), from_imports=True)


@task(gen_ui)
def preview():
    run("python dev/pyinstaller-bootstrap.py")


@task
def clean():
    from shutil import rmtree

    rmtree("dist", ignore_errors=True)
    rmtree("build", ignore_errors=True)
    print("Build caches cleaned.")


@task(clean)
def build():
    from platform import system, architecture
    from shutil import copy
    from os import path, curdir, environ, listdir, remove
    from configparser import ConfigParser
    from zipfile import ZipFile
    from fnmatch import fnmatch

    # set which files will be included within the archive.
    included_files = ["LICENSE", "README.md", "CHANGELOG.md", "CONTRIBUTING.md"]
    archive_name = "designer"  # the archive's name

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

    version = config.get('bumpversion', 'current_version') + "." + str(build_number)
    print("Version: " + version)

    spec_dir = path.join("dev", "pyinstaller-build.spec")
    zip_name = "{}-{}-{}_{}.zip".format(archive_name, version, system().lower(), architecture()[0])
    zip_dir = path.join(curdir, "dist")
    print("Building to \"{}\"".format(path.join(zip_dir, zip_name)))

    run("pyinstaller {}".format(spec_dir))
    for item in included_files:
        copy(item, "dist")
        print("Copying {} to dist/".format(item))

    with ZipFile(path.join(zip_dir, zip_name), "w") as zipfile:
        for item in listdir(zip_dir):
            if item == zip_name:
                continue
            zipfile.write(path.join(zip_dir, item), arcname=path.basename(path.join(zip_dir, item)))
            print("Adding {} to the archive.".format(item))

    for item in listdir(zip_dir):
        if fnmatch(item, "*.zip"):
            continue
        remove(path.join(zip_dir, item))
    print("Dist directory cleaned up.")
