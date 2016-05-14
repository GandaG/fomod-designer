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

from traceback import print_tb
from io import StringIO
from . import __version__


def excepthook(exc_type, exc_value, tracebackobj):
    """
    Global function to catch unhandled exceptions.
    :param exc_type: exception type
    :param exc_value: exception value
    :param tracebackobj: traceback object
    """
    from .gui import generic_errorbox

    notice = (
        "An unhandled exception occurred. Please report the problem"
        " at <a href = https://github.com/GandaG/fomod-editor/issues>Github</a>,"
        " <a href = http://www.nexusmods.com/skyrim/?>Nexus</a> or"
        " <a href = http://forum.step-project.com/index.php>STEP</a>.")
    version_info = __version__
    tbinfofile = StringIO()
    print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = 'Error information:\n\nVersion: {}\n{}: {}\n'.format(version_info, str(exc_type), str(exc_value))
    sections = [errmsg, tbinfo]
    msg = '\n'.join(sections)
    generic_errorbox("Nobody Panic!", notice, msg)


class GenericError(Exception):
    def __init__(self):
        self.title = "Generic Error"
        self.detailed = ""
        Exception.__init__(self, "Something happened...")


class MissingFileError(GenericError):
    def __init__(self, file):
        self.title = "I/O Error"
        self.message = "{} is missing.".format(file.capitalize())
        self.file = file
        Exception.__init__(self, self.message)


class ParserError(GenericError):
    def __init__(self, msg):
        self.title = "Parser Error"
        if len(msg.split(",")) <= 2:
            self.msg = "The parser couldn't read the installer file. If you need help visit " \
                       "<a href = http://www.w3schools.com/xml/xml_syntax.asp>W3Schools</a>."
        else:
            self.msg = "The parser couldn't read the installer file, there was an error around" + \
                       msg.split(",")[len(msg.split(",")) - 2] + \
                       ". If you need help visit <a href = http://www.w3schools.com/xml/xml_syntax.asp>W3Schools</a>."
        Exception.__init__(self, self.msg)


class TagNotFound(GenericError):
    def __init__(self, element):
        self.title = "Tag Lookup Error"
        self.message = "Tag {} at line {} could not be matched.".format(element.tag, element.sourceline)
        Exception.__init__(self, self.message)


class BaseInstanceException(Exception):
    def __init__(self, base):
        self.title = "Instance Error"
        self.message = "{} is not meant to be instanced. A subclass should be used instead.".format(type(base))
        Exception.__init__(self, self.message)
