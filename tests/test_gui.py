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

import sys
import os
from datetime import datetime
from copy import deepcopy
from io import StringIO
from unittest.mock import patch, Mock
from jsonpickle import encode, decode
from requests import codes
from json import JSONDecodeError
from PyQt5.QtWidgets import QDialogButtonBox, QMessageBox
from PyQt5.QtCore import Qt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import __version__
from src.gui import About, read_settings, default_settings, SettingsDialog, generic_errorbox, IntroWindow, \
    MainFrame


def test_about_dialog(qtbot):
    about_window = About(None)
    about_window.show()
    qtbot.addWidget(about_window)

    copyright_years = "2016-" + str(datetime.now().year) if datetime.now().year != 2016 else "2016"
    copyright_text = "Copyright {} Daniel Nunes".format(copyright_years)

    assert about_window.version.text() == "Version: " + __version__
    assert about_window.copyright.text() == copyright_text
    assert about_window.isVisible()

    qtbot.mouseClick(about_window.button, Qt.LeftButton)
    assert not about_window.isVisible()


@patch('src.gui.open_new_tab')
@patch('src.gui.head')
def test_help(mock_head, mock_new_tab):
    mock_response = Mock(spec='status_code')
    mock_head.return_value = mock_response
    docs_url = "http://fomod-designer.readthedocs.io/en/stable/index.html"
    local_docs = "file://" + \
                 os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "docs", "index.html"))

    mock_response.status_code = codes.ok
    MainFrame.help()
    mock_head.assert_called_once_with(docs_url, timeout=0.5)
    mock_new_tab.assert_called_once_with(docs_url)

    mock_response.status_code = codes.forbidden
    MainFrame.help()
    mock_head.assert_called_with(docs_url, timeout=0.5)
    mock_new_tab.assert_called_with(local_docs)


def test_errorbox(qtbot):
    errorbox = generic_errorbox("Title", "Text", "Detail Text")
    errorbox.show()
    qtbot.addWidget(errorbox)

    assert errorbox.isVisible()
    assert errorbox.windowTitle() == "Title"
    assert errorbox.text() == "Text"
    assert errorbox.detailedText() == "Detail Text"

    qtbot.mouseClick(errorbox.button(QMessageBox.Ok), Qt.LeftButton)
    assert not errorbox.isVisible()


@patch('src.gui.open')
def test_read_settings(mock_open):
    mock_open.return_value = StringIO(encode(default_settings))
    assert read_settings() == default_settings

    broken_settings = deepcopy(default_settings)
    broken_settings["General"] = "random string"  # simulate user messing with settings
    mock_open.return_value = StringIO(encode(broken_settings))
    assert read_settings() == default_settings

    mock_open.side_effect = FileNotFoundError("mock settings file not existing")
    assert read_settings() == default_settings

    mock_open.side_effect = JSONDecodeError(
        "mock settings file not being decodable - someone messed with the file",
        encode(default_settings),
        10  # just a random value
    )
    assert read_settings() == default_settings


@patch('src.gui.read_settings')
@patch('src.gui.open')
def test_settings_dialog(mock_open, mock_read_settings, qtbot, tmpdir):
    with open(os.path.join(str(tmpdir), "settings_file"), "wt") as settings_file:
        settings_file.write(encode(default_settings))
        mock_open.return_value = settings_file
    mock_read_settings.return_value = default_settings
    settings_window = SettingsDialog(None)
    settings_window.show()
    qtbot.addWidget(settings_window)

    # check that default settings are properly loaded.
    assert settings_window.isVisible()
    assert settings_window.settings_dict == default_settings

    assert settings_window.combo_code_refresh.currentIndex() == default_settings["General"]["code_refresh"]
    assert settings_window.check_intro.isChecked() == default_settings["General"]["show_intro"]
    assert settings_window.check_advanced.isChecked() == default_settings["General"]["show_advanced"]
    assert settings_window.check_tutorial.isChecked() == default_settings["General"]["tutorial_advanced"]

    assert settings_window.check_valid_load.isChecked() == default_settings["Load"]["validate"]
    assert settings_window.check_valid_load_ignore.isChecked() == default_settings["Load"]["validate_ignore"]
    assert settings_window.check_warn_load.isChecked() == default_settings["Load"]["warnings"]
    assert settings_window.check_warn_load_ignore.isChecked() == default_settings["Load"]["warn_ignore"]

    assert settings_window.check_valid_save.isChecked() == default_settings["Save"]["validate"]
    assert settings_window.check_valid_save_ignore.isChecked() == default_settings["Save"]["validate_ignore"]
    assert settings_window.check_warn_save.isChecked() == default_settings["Save"]["warnings"]
    assert settings_window.check_warn_save_ignore.isChecked() == default_settings["Save"]["warn_ignore"]

    assert settings_window.check_installSteps.isChecked() == default_settings["Defaults"]["installSteps"].enabled()
    assert settings_window.combo_installSteps.isEnabled() == default_settings["Defaults"]["installSteps"].enabled()
    assert settings_window.combo_installSteps.currentText() == default_settings["Defaults"]["installSteps"].value()
    assert settings_window.check_optionalFileGroups.isChecked() == default_settings["Defaults"][
        "optionalFileGroups"].enabled()
    assert settings_window.combo_optionalFileGroups.isEnabled() == default_settings["Defaults"][
        "optionalFileGroups"].enabled()
    assert settings_window.combo_optionalFileGroups.currentText() == default_settings["Defaults"][
        "optionalFileGroups"].value()
    assert settings_window.check_type.isChecked() == default_settings["Defaults"]["type"].enabled()
    assert settings_window.combo_type.isEnabled() == default_settings["Defaults"]["type"].enabled()
    assert settings_window.combo_type.currentText() == default_settings["Defaults"]["type"].value()
    assert settings_window.check_defaultType.isChecked() == default_settings["Defaults"]["defaultType"].enabled()
    assert settings_window.combo_defaultType.isEnabled() == default_settings["Defaults"]["defaultType"].enabled()
    assert settings_window.combo_defaultType.currentText() == default_settings["Defaults"]["defaultType"].value()

    assert settings_window.button_colour_required.styleSheet() == "background-color: " + default_settings["Appearance"][
        "required_colour"]
    assert settings_window.button_colour_atleastone.styleSheet() == "background-color: " + default_settings[
        "Appearance"]["atleastone_colour"]
    assert settings_window.button_colour_either.styleSheet() == "background-color: " + default_settings["Appearance"][
        "either_colour"]
    assert (not default_settings["Appearance"]["style"] or
            settings_window.combo_style.currentText() == default_settings["Appearance"]["style"])
    assert (not default_settings["Appearance"]["palette"] or
            settings_window.combo_palette.currentText() == default_settings["Appearance"]["palette"])

    # TODO: check if you can simulate clicks on the check boxes, etc. and test new settings.

    os.remove(os.path.join(str(tmpdir), "settings_file"))
    with open(os.path.join(str(tmpdir), "settings_file"), "wt") as settings_file:
        mock_open.return_value = settings_file
        qtbot.mouseClick(settings_window.buttonBox.button(QDialogButtonBox.Ok), Qt.LeftButton)
    assert not settings_window.isVisible()
    with open(os.path.join(str(tmpdir), "settings_file"), "rt") as settings_file:
        assert decode(settings_file.read()) == settings_window.settings_dict


@patch("src.gui.read_settings")
def test_intro(mock_read_settings, qtbot):
    settings_dict = default_settings
    settings_dict["General"]["tutorial_advanced"] = False
    mock_read_settings.return_value = settings_dict
    intro_window = IntroWindow()
    qtbot.addWidget(intro_window)

    assert intro_window.isVisible()
    assert intro_window.version.text() == "Version " + __version__
    assert intro_window.windowTitle() == "FOMOD Designer"

    intro_window.open_path("/")

    assert not intro_window.isVisible()

    settings_dict["General"]["show_intro"] = False
    mock_read_settings.return_value = settings_dict
    intro_window = IntroWindow()
    print(intro_window.settings_dict)
    qtbot.addWidget(intro_window)

    assert not intro_window.isVisible()


def test_mainframe(qtbot):
    main_window = MainFrame()
    main_window.show()
    qtbot.addWidget(main_window)

    assert main_window.isVisible()

    # TODO: actually test this class
