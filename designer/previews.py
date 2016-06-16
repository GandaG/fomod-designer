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

from queue import Queue
from PyQt5.QtCore import QThread
from lxml.etree import XML, tostring
from lxml.objectify import deannotate
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.html import XmlLexer
from .io import sort_elements


class PreviewDispatcherThread(QThread):
    """
    Thread used to dispatch the element to each preview worker thread.

    :param queue: The main queue containing the elements to process.
    :param mo_signal: The signal to pass to the MO preview worker, updates the MO preview.
    :param nmm_signal: The signal to pass to the NMM preview worker, updates the NMM preview.
    :param code_signal: The signal to pass to the code preview worker, updates the code preview.
    """
    def __init__(self, queue, mo_signal, nmm_signal, code_signal):
        super().__init__()
        self.queue = queue
        self.mo_queue = Queue()
        self.nmm_queue = Queue()
        self.code_queue = Queue()

        self.code_thread = PreviewCodeWorker(self.code_queue, code_signal)
        self.code_thread.start()

    def run(self):
        while True:
            # wait for next element
            element = self.queue.get()
            if element is None:  # needed because connecting the signal to the queue adds a NoneType, no idea why.
                continue

            # turn the element into "normal" lxml elements for easier processing.
            element.write_attribs()
            sort_elements(element)
            element = XML(tostring(element))

            # dispatch to every queue
            self.mo_queue.put(element)
            self.nmm_queue.put(element)
            self.code_queue.put(element)


class PreviewCodeWorker(QThread):
    """
    Takes a xml element, writes the code, highlights it with inline css and returns the html code.

    :param queue: The queue that receives the elements to be processed.
    :param return_signal: The signal used to send the return code through.
    :return: The highlighted element html code.
    """
    def __init__(self, queue, return_signal):
        super().__init__()
        self.queue = queue
        self.return_signal = return_signal

    def run(self):
        while True:
            # wait for next element
            element = self.queue.get()

            # process the element
            deannotate(element, cleanup_namespaces=True)
            code = tostring(element, encoding="Unicode", pretty_print=True, xml_declaration=False)
            self.return_signal.emit(highlight(code, XmlLexer(), HtmlFormatter(noclasses=True, style="autumn", linenos="table")))
