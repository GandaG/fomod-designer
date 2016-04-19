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


class ParseException(Exception):
    def __init__(self, file):
        self.title = "Parser Error"
        self.message = "Error parsing file " + str(file)
        self.detailed = ""
        Exception.__init__(self, self.message)


class ParseMissingFileException(ParseException):
    def __init__(self):
        self.title = "Parser Error"
        self.message = "Either info.xml or moduleconfig.xml are missing."
        self.detailed = ""
        Exception.__init__(self, self.message)


class ParseSyntaxException(ParseException):
    def __init__(self, file, detail):
        self.title = "Parser Error"
        self.message = str(file) + " file has incorrect syntax."
        self.detailed = detail
        Exception.__init__(self, self.message)
