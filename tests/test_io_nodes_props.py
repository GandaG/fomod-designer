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

import sys, os, lxml, pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from designer.io import import_, export, module_parser, new, copy_node, node_factory
from designer.exceptions import TagNotFound, ParserError, BaseInstanceException
from designer.nodes import _NodeElement
from designer.props import _PropertyBase


def test_import_export(tmpdir):
    tmpdir = str(tmpdir)

    info_root, config_root = import_(os.path.join(os.path.dirname(__file__), "data", "valid_fomod"))
    info_root.sort()
    config_root.sort()
    export(info_root, config_root, tmpdir)

    with open(os.path.join(os.path.dirname(__file__), "data", "valid_fomod", "fomod", "Info.xml")) as info_base:
        with open(os.path.join(tmpdir, "fomod", "Info.xml")) as info_exported:
            assert info_base.read() == info_exported.read()
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "data",
            "valid_fomod",
            "fomod",
            "ModuleConfig.xml"
        )
    ) as config_base:
        with open(os.path.join(tmpdir, "fomod", "ModuleConfig.xml")) as config_exported:
            assert config_base.read() == config_exported.read()


def test_exceptions():
    invalid_fomod = "<boopity/>"
    with pytest.raises(TagNotFound):
        lxml.etree.fromstring(invalid_fomod, parser=module_parser)

    with pytest.raises(ParserError):
        import_(os.path.join(os.path.dirname(__file__), "data", "invalid_fomod"))

    with pytest.raises(BaseInstanceException):
        _NodeElement()

    with pytest.raises(BaseInstanceException):
        _PropertyBase("test", [])

    assert (None, None) == import_(os.path.join(os.path.dirname(__file__), "data", "incomplete_fomod"))
    assert (None, None) == import_(os.path.join(os.path.dirname(__file__), "boop"))


def test_node_operations():
    base_info = "<fomod/>"
    base_config = "<config xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" " \
                  "xsi:noNamespaceSchemaLocation=\"http://qconsulting.ca/fo3/ModConfig5.0.xsd\"/>"
    info_root, config_root = new()
    info_root.parse_attribs()
    config_root.parse_attribs()
    info_root.write_attribs()
    config_root.write_attribs()

    assert base_info == lxml.etree.tostring(info_root, encoding="unicode")
    assert base_config == lxml.etree.tostring(config_root, encoding="unicode")

    new_elem = node_factory(config_root.allowed_children[0].tag, config_root)
    config_root.add_child(new_elem)
    new_config_root = copy_node(config_root)
    new_config_root.remove_child(new_config_root[0])

    assert base_config == lxml.etree.tostring(new_config_root, encoding="unicode")

    new_config_root.user_sort_order = "5"
    new_sort_order_xml = "<config xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" " \
                         "xsi:noNamespaceSchemaLocation=\"http://qconsulting.ca/fo3/ModConfig5.0.xsd\">" \
                         "<!--<designer.metadata.do.not.edit> {\"user_sort\":\"0000005\"}-->" \
                         "</config>"

    new_config_root.save_metadata()
    new_config_root.load_metadata()

    assert new_sort_order_xml == lxml.etree.tostring(new_config_root, encoding="unicode")
