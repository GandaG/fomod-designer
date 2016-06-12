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

from lxml.etree import XML, tostring
from lxml.objectify import deannotate
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.html import XmlLexer


def highlight_fragment(element):
    """
    Takes a xml element, writes the code, highlights it with inline css and returns the html code.

    :param element: The elements to highlight. Includes the element's children.
    :return: The highlighted element code.
    """
    element.write_attribs()
    new_elem = XML(tostring(element))
    deannotate(new_elem, cleanup_namespaces=True)
    code = tostring(new_elem, encoding="Unicode", pretty_print=True, xml_declaration=False)
    return highlight(code, XmlLexer(), HtmlFormatter(noclasses=True, style="autumn"))
