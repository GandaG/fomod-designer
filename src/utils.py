#!/usr/bin/env python

# Copyright 2019 Daniel Nunes
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

import io
import sys
import traceback
from pathlib import Path
from typing import Union

from PyQt5 import QtGui, QtWidgets

__version__ = "0.8.1"
__exename__ = "FOMOD Designer"
__arcname__ = "fomod-designer"


if getattr(sys, "frozen", False):
    ROOT_FOLDER = Path(sys._MEIPASS)
    FROZEN = True
else:
    ROOT_FOLDER = Path(__file__).resolve().parent.parent
    FROZEN = False

RESOURCE_FOLDER = ROOT_FOLDER / "dat"


def excepthook(exc_type, exc_value, tracebackobj):
    """
    Global function to catch unhandled exceptions.

    @param exc_type exception type
    @param exc_value exception value
    @param tracebackobj traceback object
    """
    notice = (
        "An unhandled exception occurred. Please report the problem at "
        "<a href = https://github.com/GandaG/fomod-designer/issues>Github</a>."
    )
    version_info = __version__
    icon_path = RESOURCE_FOLDER / "logo_admin.png"

    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = "Error information:\n\nVersion: {}\n{}: {}\n".format(
        version_info, str(exc_type), str(exc_value)
    )
    sections = [errmsg, tbinfo]
    msg = "\n".join(sections)

    errorbox = QtWidgets.QMessageBox()
    errorbox.setText(notice)
    errorbox.setDetailedText(msg)
    errorbox.setWindowTitle("An Error Has Occured")
    errorbox.setIconPixmap(QtGui.QPixmap(str(icon_path)))
    errorbox.exec_()


def file_dialog(
    parent: QtWidgets.QWidget, title: str, selected_file: str, package_path: str
) -> Union[str, None]:
    selected = QtWidgets.QFileDialog.getOpenFileName(
        parent, title, selected_file or package_path
    )
    if not selected[0]:  # user cancelled
        return None
    fpath = Path(selected[0])
    return fpath.relative_to(Path(package_path))
