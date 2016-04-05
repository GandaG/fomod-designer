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

import traceback
import io
from PyQt5 import QtWidgets
from .. import __version__


def excepthook(exc_type, exc_value, tracebackobj):
    """
    Global function to catch unhandled exceptions.

    @param exc_type exception type
    @param exc_value exception value
    @param tracebackobj traceback object
    """
    notice = (
        "An unhandled exception occurred. Please report the problem"
        " at <a href = https://github.com/GandaG/fomod-editor/issues>Github</a>,"
        " <a href = http://www.nexusmods.com/skyrim/?>Nexus</a> or"
        " <a href = http://forum.step-project.com/>STEP</a>."
        " <br><br>Error information:<br>")
    version_info = __version__

    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '{}:<br>{}'.format(str(exc_type), str(exc_value))
    sections = [errmsg, tbinfo]
    msg = '<br>'.join(sections)

    errorbox = QtWidgets.QMessageBox()
    errorbox.setText(notice + msg + "<br>" + version_info)
    errorbox.exec_()
