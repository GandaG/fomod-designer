#!/usr/bin/python

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

import wx
import template


class Mainframe(template.main):
    def __init__(self, parent):
        template.main.__init__(self, parent)


def main():
    # mandatory in wx, create an app, False stands for not deteriction stdin/stdout
    # refer manual for details
    app = wx.App(False)

    # create an object of root
    frame = Mainframe(None)
    # show the frame
    frame.Show(True)
    # start the applications
    app.MainLoop()
