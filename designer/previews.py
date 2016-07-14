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

from os.path import join, sep, normpath
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
    def __init__(self, queue, code_signal, **kwargs):
        super().__init__()
        self.queue = queue
        self.gui_queue = Queue()
        self.code_queue = Queue()

        self.code_thread = PreviewCodeWorker(self.code_queue, code_signal)
        self.code_thread.start()
        self.gui_thread = PreviewGuiWorker(self.gui_queue, **kwargs)
        self.gui_thread.start()

    def run(self):
        while True:
            # wait for next element
            element = self.queue.get()

            if element is not None:
                element.write_attribs()
                element.load_metadata()
                sort_elements(element)

            # dispatch to every queue
            self.gui_queue.put(element)
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

            if element is None:
                self.return_signal.emit("")
                continue

            element = XML(tostring(element))

            # process the element
            deannotate(element, cleanup_namespaces=True)
            code = tostring(element, encoding="Unicode", pretty_print=True, xml_declaration=False)
            self.return_signal.emit(highlight(code, XmlLexer(), HtmlFormatter(
                noclasses=True, style="autumn", linenos="table"
            )))


class PreviewGuiWorker(QThread):
    class InstallStepData(object):
        def __init__(self, name):
            self.name = name
            self.group_list = []

        def set_group_list(self, group_list):
            self.group_list = group_list

        def sort_ascending(self):
            self.group_list = sorted(self.group_list, key=lambda x: x.name)

        def sort_descending(self):
            self.group_list = sorted(self.group_list, reverse=True, key=lambda x: x.name)

    class GroupData(object):
        def __init__(self, name, group_type):
            self.name = name
            self.type = group_type
            self.plugin_list = []

        def set_plugin_list(self, plugin_list):
            self.plugin_list = plugin_list

        def sort_ascending(self):
            self.plugin_list = sorted(self.plugin_list, key=lambda x: x.name)

        def sort_descending(self):
            self.plugin_list = sorted(self.plugin_list, reverse=True, key=lambda x: x.name)

    class PluginData(object):
        def __init__(self, name, description, image_path, file_list, folder_list, flag_list, plugin_type):
            self.name = name
            self.description = description
            self.image_path = image_path
            self.file_list = file_list
            self.folder_list = folder_list
            self.flag_list = flag_list
            self.type = plugin_type

    class FileData(object):
        def __init__(self, abs_source, rel_source, destination, priority, always_install, install_usable):
            self.abs_source = abs_source
            self.rel_source = rel_source
            self.destination = destination
            self.priority = priority
            self.always_install = always_install
            self.install_usable = install_usable

    class FolderData(FileData):
        pass

    class FlagData(object):
        def __init__(self, label, value):
            self.label = label
            self.value = value

    def __init__(self, queue, **kwargs):
        super().__init__()
        self.queue = queue
        self.kwargs = kwargs

    def run(self):
        while True:
            # wait for next element
            element = self.queue.get()

            if element is None:
                self.kwargs["gui_worker"].invalid_node_signal.emit()
                continue
            elif element.tag == "installStep":
                pass
            elif [elem for elem in element.iterancestors() if elem.tag == "installStep"]:
                element = [elem for elem in element.iterancestors() if elem.tag == "installStep"][0]
            elif not [elem for elem in self.kwargs["config_root"]().iter() if elem.tag == "installStep"]:
                self.kwargs["gui_worker"].missing_node_signal.emit()
                continue
            else:
                self.kwargs["gui_worker"].invalid_node_signal.emit()
                continue

            self.kwargs["gui_worker"].clear_tab_signal.emit()
            self.kwargs["gui_worker"].clear_ui_signal.emit()
            info_name = self.kwargs["info_root"]().find("Name").text \
                if self.kwargs["info_root"]().find("Name") is not None else ""
            info_author = self.kwargs["info_root"]().find("Author").text \
                if self.kwargs["info_root"]().find("Author") is not None else ""
            info_version = self.kwargs["info_root"]().find("Version").text \
                if self.kwargs["info_root"]().find("Version") is not None else ""
            info_website = self.kwargs["info_root"]().find("Website").text \
                if self.kwargs["info_root"]().find("Website") is not None else ""
            self.kwargs["gui_worker"].set_labels_signal.emit(info_name, info_author, info_version, info_website)

            step_data = self.InstallStepData(element.get("name"))
            opt_group_elem = element.find("optionalFileGroups")
            if opt_group_elem is not None:
                group_data_list = []

                for group_elem in opt_group_elem.findall("group"):
                    group_data = self.GroupData(group_elem.get("name"), group_elem.get("type"))

                    plugins_elem = group_elem.find("plugins")
                    if plugins_elem is not None:
                        plugin_data_list = []

                        for plugin_elem in plugins_elem.findall("plugin"):
                            name_ = plugin_elem.get("name")
                            description_ = plugin_elem.find("description").text \
                                if plugin_elem.find("description") is not None else ""
                            image_ = plugin_elem.find("image").get("path") \
                                if plugin_elem.find("image") is not None else ""
                            if image_:
                                # normalize path, for some reason normpath wasn't working
                                image_ = join(self.kwargs["package_path"](), image_).replace("\\", "/")
                                image_ = image_.replace("/", sep)

                            file_data_list = []
                            for file_elem in plugin_elem.findall("files/file"):
                                file_data_list.append(
                                    self.FileData(
                                        normpath(join(
                                            self.kwargs["package_path"](),
                                            file_elem.get("source").replace("\\", "/")
                                        )),
                                        file_elem.get("source"),
                                        normpath(file_elem.get("destination").replace("\\", "/")),
                                        file_elem.get("priority"),
                                        file_elem.get("alwaysInstall"),
                                        file_elem.get("installIfUsable")
                                    )
                                )

                            folder_data_list = []
                            for folder_elem in plugin_elem.findall("files/folder"):
                                folder_data_list.append(
                                    self.FolderData(
                                        normpath(join(
                                            self.kwargs["package_path"](),
                                            folder_elem.get("source").replace("\\", "/")
                                        )),
                                        folder_elem.get("source"),
                                        normpath(folder_elem.get("destination").replace("\\", "/")),
                                        folder_elem.get("priority"),
                                        folder_elem.get("alwaysInstall"),
                                        folder_elem.get("installIfUsable")
                                    )
                                )

                            flag_data_list = []
                            for flag_elem in plugin_elem.findall("conditionFlags/flag"):
                                flag_data_list.append(
                                    self.FlagData(
                                        flag_elem.get("name"),
                                        flag_elem.text
                                    )
                                )

                            type_elem = plugin_elem.find("typeDescriptor/type")
                            default_type_elem = plugin_elem.find("typeDescriptor/dependencyType/defaultType")
                            if type_elem is not None:
                                type_ = type_elem.get("name")
                            elif default_type_elem is not None:
                                type_ = default_type_elem.get("name")
                            else:
                                type_ = "Required"

                            plugin_data_list.append(
                                self.PluginData(
                                    name_,
                                    description_,
                                    image_,
                                    file_data_list,
                                    folder_data_list,
                                    flag_data_list,
                                    type_
                                )
                            )

                        group_data.set_plugin_list(plugin_data_list)
                        if plugins_elem.get("order") == "Ascending":
                            group_data.sort_ascending()
                        elif plugins_elem.get("order") == "Descending":
                            group_data.sort_descending()

                    group_data_list.append(group_data)

                step_data.set_group_list(group_data_list)
                if opt_group_elem.get("order") == "Ascending":
                    step_data.sort_ascending()
                elif opt_group_elem.get("order") == "Descending":
                    step_data.sort_descending()

            self.kwargs["gui_worker"].create_page_signal.emit(step_data)
