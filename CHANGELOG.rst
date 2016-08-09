Changelog
=========

**0.7.2 (2016-07-13)**

* Plugin node should now have the correct required child nodes.
* Fixed validation and warning dialogs and ignore process.
* Fixed files processing in preview.

----------------------------------

**0.7.1 (2016-07-12)**

* Fixed preview issue with non-existent nodes under info root.
* Updated validation and children groups.

----------------------------------

**0.7.0 (2016-07-10)**

* Fixed rare bug with the validator.
* Added Dependencies Wizard.
* Children box now lists invalid child nodes greyed out instead of deleting them.
* Fixed issues with saving.
* Nodes should now be properly sorted.
* Added specialized child nodes with colours.
* Added auto-completion for flag labels and their values.
* Fixed recent files issues.
* Properties are now ordered.
* Added node-specific metadata.
* Pattern node's names are now editable.
* Improved Setting's dialog.
* Added Defaults section to settings.
* Added Appearance tab to settings dialog.
* Fixed rare bug with xml preview.
* Disabled Wizards.
* Added user-defined noe sorting with drag and drop.
* Improved logos.
* Added copy and paste functionality. 
* Added undo and redo functionality.
* Loading ui should now be slightly faster - ui is now pre-compiled.
* Full keyboard navigation is now supported on the node tree.
* Added context menu to the node tree.
* Actions should now be properly disabled/enabled when appropriate.
* All nodes should now be correct on their allowed number.
* Added plain text editor to most simple text properties and html editor to plugin's description text.
* Added install step ui preview.
* Added tutorial at startup. Added setting to re-enable the tutorial.

----------------------------------

**0.6.0 (2016-06-13)**

* Added check for updates at startup.
* Added line numbers to code preview.
* Moved previews to separate threads, loading each node should now be much faster.
* Improved button look on object box.

----------------------------------

**0.5.1 (2016-06-12)**

* Fixed versioning issues.

----------------------------------

**0.5.0 (2016-06-12)**

* Added intro window.
* Added Files wizard.
* Added wizard environment setup.
* Updated app and file icons.
* The object box now consists of independent buttons for each child instead of a list.
* A message box asking for confirmation should now appear when trying to open a new installer while there unsaved changes.
* Property editor should now be properly cleared when opening a new installer.
* A message box asking for action should now appear when using the recent files menu and the path no longer exists.
* Fixed relation between view menu and docked widget states.
* Dialog windows should now properly be placed on top of other windows.
* Improved some nodes' names.

----------------------------------

**0.4.1 (2016-05-16)**

* Fixed wrong default attributes in file and folder tags.
* Added wizard framework.

----------------------------------

**0.4.0 (2016-05-14)**

* Added file and window icons.
* Fixed combo boxes not being set at start.
* Added recent files menu.
* Added about dialog.
* Added view menu.
* Closing the main window with unsaved changes should now display a warning.
* Not identified tags should be properly handled now.
* Syntax errors in the xml should be properly handled now.
* File, folder and colour properties now have a proper specific widget.
* Added sorting to xml elements when saving.
* Added xml code preview.
* Added settings window.
* Attribute parsing should now properly ignore the ones that are unknown.
* Validation and warning checks added.
* Multiple bugfixes.

----------------------------------

**0.3.1 (2016-04-17)**

* Tags/item with name/source property now have that as the title instead of the tag's name.
* Fixed all keyboard shortcuts.
* Everything is now included within a single executable.
* Added full linux support.
* Included build number in version.
* Fixed no error raised when no required child exist.
* Window title now includes an asterisk when any content has been modified.
* Missing files in fomod folder are now properly checked.
* Fixed spinbox property.

----------------------------------

**0.3.0 (2016-04-07)**

* All basic functionality is now done.
* Tag properties are now properly displayed and editable.
* XML comments are now ignored by the parser.
* Child objects are now auto-selected when created.
* Fixed error when opening an installer over an already opened one.
* Fixed dependencies tag not being able to be self nested.
* Fixed deployed archive structure.

----------------------------------

**0.2.1 (2016-04-05)**

* In-tag text is now properly parsed and saved along with everything else.

----------------------------------

**0.2.0 (2016-04-05)**

* Users can now modify the installer's objects.

----------------------------------

**0.1.0 (2016-04-03)**

* Users can now open and save FOMOD installers.
* Main windows title now shows which package you are currently working on.

----------------------------------

**0.0.1 (2016-03-15)**

* GUI draft completed.
