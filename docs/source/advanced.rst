Advanced Usage
==============

For the advanced users and everyone who knows their way around a *FOMOD* installer.
In this section you'll find descriptions of the tags and nodes themselves - what they are, how to use them and
examples when needed.

There are no restrictions when using the *Advanced View*, we trust that you know what you're doing.
This is recommended for people who already know how to create/modify XML
installers and are interested in speeding up their work or for users who want more customization options than the
*Basic View* offers.

Advanced View
+++++++++++++

The *Advanced View* can be divided in 4 parts: **Node Tree**, **Previews**, **Property Editor** and **Children Box**.
All of these, with the exception of the **Previews**, can be moved around by the user.

The **Node Tree**, by default situated on the left, contains all the nodes in the installer's two trees: the `Info`_ and
the `Config`_ tree. You can right-click the tree to see all the actions available - some of these, like *Delete*, are
not available for the root nodes. You can also traverse the tree with the arrow keys and use the Enter key or left-click
to select the node, this will update the **Property Editor** and the **Children Box** (and the **Previews** in case that
is enabled).

The **Previews**, situated on the center, has two tabs: *GUI Preview* and *XML Preview*. The *GUI Preview* has a Mod
Organizer-like interface that simulates the current `Install Step`_ - you can choose the options and the bottom half
reflects the flags that would be set and/or the files that would be installed. The *XML Preview* has a preview of the
XML code that that node and its children would output.

The **Property Editor**, by default situated on the top right, contains all the editable properties for the currently
selected node. You can find more information for each node's properties in the `FOMOD Bible`_.

The **Children Box**, by default situated on the bottom right, contains all the available children to add to the
currently selected node. Click on a child button here to add the corresponding node.

Learn you a FOMOD For Great Good
++++++++++++++++++++++++++++++++

This section contains the `FOMOD Bible`_ - a description of all the tags/nodes with examples.
This is not meant to be read from top to bottom but rather as a dictionary or a glossary -
search for the tag/node you need more info on with the search box on the left sidebar.

Tag vs Node
...........

A **Tag** is any item within an xml document. Within the *FOMOD* schema
(the document that defines the rules for installer documents)
all the allowed tags for FOMOD are defined. A tag has the format ``<tag/>`` or
``<tag>text goes here<tag/>`` if it contains text.

Similarly, any item in the *FOMOD Designer*'s *Node Tree* is a **Node**.
Every node has a direct correspondence to a xml tag.
These two terms are use interchangeably in the *FOMOD Bible*.

Attribute vs Property
.....................

An **Attribute** is a way to customize a tag. These are also defined in the *FOMOD* schema and have the format:
``<tag attribute="value"/>``.

A **Property** is the attribute equivalent for nodes. They can be edited via the *Property Editor*. In the *Bible*
the properties are always followed by the corresponding attribute in square brackets (p.e. Name [name]).

.. attention::
    While a tag's text (p.e. ``<tag>text goes here<tag/>``) is not an attribute, in a node it is bundled together
    with its properties for convenience. In order to distinguish text from other properties, it is marked with
    [...] as its attribute.

    So for a node that can have text its properties will have the line:
    Text [...]

Tag Order
.........

Some tags are enforced a specific order by the *FOMOD* schema.
When applicable, the possible/required children listed in each node are ordered.

This enforced order is reflected in the node tree. The user is able to modify the order
of repeatable nodes through drag and drop.

FOMOD Bible
...........

Please take note this isn't a fully comprehensive document (at least so far). If you want something more complete,
feel free to look at the `revised *FOMOD* schema <>`_.

Info
----

Tag
    fomod

Description
    The root node for the document containing all the information relative to the installer.

Children
    ====================== ==========
    Node                   Repeatable
    ====================== ==========
    :ref:`info_name_label` **No**
    `Author`_              **No**
    :ref:`info_desc_label` **No**
    `ID`_                  **No**
    `Categories Group`_    **No**
    `Version`_             **No**
    `Website`_             **No**
    ====================== ==========

Properties
    *None*

-------------------------------------

.. _info_name_label:

Name
----

Tag
    Name

Description
    The node that holds the mod's name.

Children
    *None*

Properties
    =============== =============== ===============================
    Property        Attribute       Description
    =============== =============== ===============================
    Text            [...]           The name of the mod.
    =============== =============== ===============================

-------------------------------------

Author
------

Tag
    Author

Description
    The node that holds the mod's author(s).

Children
    *None*

Properties
    =============== =============== ===============================
    Property        Attribute       Description
    =============== =============== ===============================
    Text            [...]           The author(s) of the mod.
    =============== =============== ===============================

-------------------------------------

.. _info_desc_label:

Description
-----------

Tag
    Description

Description
    The node that holds the mod's description.

Children
    *None*

Properties
    =============== =============== ===============================
    Property        Attribute       Description
    =============== =============== ===============================
    Text            [...]           The description of the mod.
    =============== =============== ===============================

-------------------------------------

ID
--

Tag
    Id

Description
    The node that holds the mod's ID.
    The ID is the last part of the nexus' link. Example:

    Nexus mod link: http://www.nexusmods.com/skyrim/mods/548961 -> ID's text is 548961

Children
    *None*

Properties
    =============== =============== ===============================
    Property        Attribute       Description
    =============== =============== ===============================
    Text            [...]           The ID of the mod.
    =============== =============== ===============================

-------------------------------------

Categories Group
----------------

Tag
    Groups

Description
    This node's purpose is solely to group the categories this mod belongs to together.

Children
    ====================== ==========
    Node                   Repeatable
    ====================== ==========
    `Category`_            **Yes**
    ====================== ==========

Properties
    *None*

-------------------------------------

Category
--------

Tag
    element

Description
    The node that holds one of the mod's category.

Children
    *None*

Properties
    =============== =============== ===============================
    Property        Attribute       Description
    =============== =============== ===============================
    Text            [...]           A category this mod belongs to.
    =============== =============== ===============================

-------------------------------------

Version
-------

Tag
    Version

Description
    The node that holds the mod's version.

Children
    *None*

Properties
    =============== =============== ===============================
    Property        Attribute       Description
    =============== =============== ===============================
    Text            [...]           This mod's version.
    =============== =============== ===============================

-------------------------------------

Website
-------

Tag
    Website

Description
    The node that holds the mod's home website.

Children
    *None*

Properties
    =============== =============== ===============================
    Property        Attribute       Description
    =============== =============== ===============================
    Text            [...]           The mod's home website.
    =============== =============== ===============================

-------------------------------------

Config
------

Tag
    config

Description
    The main element containing the module configuration info.

Children
    =========================== ========== ================================================
    Node                        Repeatable Notes
    =========================== ========== ================================================
    :ref:`config_name_label`    **No**
    :ref:`mod_image_label`      **No**
    `Mod Dependencies`_         **No**     At least one of the following is required
                                           for the installer to have any effect:
                                           `Mod Dependencies`_, `Installation Steps`_,
                                           `Mod Requirements`_, `Conditional Installation`_
    `Installation Steps`_       **No**     At least one of the following is required
                                           for the installer to have any effect:
                                           `Mod Dependencies`_, `Installation Steps`_,
                                           `Mod Requirements`_, `Conditional Installation`_
    `Mod Requirements`_         **No**     At least one of the following is required
                                           for the installer to have any effect:
                                           `Mod Dependencies`_, `Installation Steps`_,
                                           `Mod Requirements`_, `Conditional Installation`_
    `Conditional Installation`_ **No**     At least one of the following is required
                                           for the installer to have any effect:
                                           `Mod Dependencies`_, `Installation Steps`_,
                                           `Mod Requirements`_, `Conditional Installation`_
    =========================== ========== ================================================

Properties
    =============== ==================================================================== ===============================
    Property        Attribute                                                            Description
    =============== ==================================================================== ===============================
    *N/A*           {http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation This attribute contains the
                                                                                         namespace for this file.

                                                                                         This property is not editable.

                                                                                         The value should always be:
                                                                                         ``"http://qconsulting.ca/fo3/ModConfig5.0.xsd"``
    =============== ==================================================================== ===============================

-------------------------------------

.. _config_name_label:

Name
----

Tag
    moduleName

Description
    The name of the module. Used to describe the display properties of the module title.

Children
    *None*

Properties
    =============== =============== =================================================================
    Property        Attribute       Description
    =============== =============== =================================================================
    Text            [...]           The name of the mod.
    Position        position        The position of the mod's name in the header.

                                    Accepts the values: ``"Left"``, ``"Right"`` or ``"RightOfImage"``
    Colour          colour          The colour of the mod's name in the header.

                                    Accepts RGB hex values.
    =============== =============== =================================================================

-------------------------------------

.. _mod_image_label:

Image
-----

Tag
    moduleImage

Description
    The module logo/banner.

    *[Ignored in Mod Organizer]*

Children
    *None*

Properties
    =============== =============== ======================================
    Property        Attribute       Description
    =============== =============== ======================================
    Path            path            The path to the image file.
    Show Image      showImage       Whether the image is visible.

                                    Accepts ``true`` or ``false``
    Show Fade       showFade        Whether the image's opacity is fixed.

                                    Accepts ``true`` or ``false``
    Height          height          The maximum height of the image.

                                    Accepts any integer larger than ``-1``
    =============== =============== ======================================

-------------------------------------

Mod Dependencies
----------------

Tag
    moduleDependencies

Description
    Items upon which the module depends. The installation process will only start after these conditions have been met.

    While flag dependencies are allowed they should not be used since no flag will have been set at the time these
    conditions are checked.

Children
    =========================== ==========
    Node                        Repeatable
    =========================== ==========
    `File Dependency`_          **Yes**
    `Flag Dependency`_          **Yes**
    `Game Dependency`_          **No**
    `Dependencies`_             **Yes**
    =========================== ==========

Properties
    =============== =============== =============================================
    Property        Attribute       Description
    =============== =============== =============================================
    Type            operator        The type of the dependency: ``And`` or ``Or``

                                    If the type is ``And``, all conditions under
                                    this node must be met.

                                    If the type is ``Or``, only one condition
                                    must be met.
    =============== =============== =============================================

-------------------------------------

File Dependency
---------------

Tag
    fileDependency

Description
    Specifies that a mod must be in a specified state.

Children
    *None*

Properties
    =============== =============== ======================================
    Property        Attribute       Description
    =============== =============== ======================================
    File            file            The path to the file to be checked.
    State           state           The supposed state of the file.
    =============== =============== ======================================

-------------------------------------

Flag Dependency
---------------

Tag
    flagDependency

Description
    Specifies that a condition flag must have a specific value.

Children
    *None*

Properties
    =============== =============== =========================================
    Property        Attribute       Description
    =============== =============== =========================================
    Flag            flag            The flag where this condition falls upon.
    Value           value           The value of the flag to be checked.
    =============== =============== =========================================

-------------------------------------

Game Dependency
---------------

Tag
    gameDependency

Description
    Specifies a minimum required version of the installed game.

    *[Ignored in Mod Organizer]*

Children
    *None*

Properties
    =============== =============== ======================================
    Property        Attribute       Description
    =============== =============== ======================================
    Version         version         The minimum version of the game.
    =============== =============== ======================================

-------------------------------------

Installation Steps
------------------

Tag
    installSteps

Description
    The list of install steps that determine which files (or plugins) that may optionally be installed for this module.

Children
    =========================== ========== ============================================
    Node                        Repeatable Notes
    =========================== ========== ============================================
    `Install Step`_             **Yes**    At least one of `Install Step`_ is required.
    =========================== ========== ============================================

Properties
    =============== =============== ======================================
    Property        Attribute       Description
    =============== =============== ======================================
    Order           order           The order of the install steps beneath
                                    this node.
                                    ``"Explicit"`` follows document
                                    order while the others order
                                    alphabetically.

                                    Accepts ``"Ascending"``,
                                    ``"Descending"`` or ``"Explicit"``
    =============== =============== ======================================

-------------------------------------

Install Step
------------

Tag
    installStep

Description
    A step in the install process containing groups of optional plugins.

Children
    =========================== ========== ============================================
    Node                        Repeatable Notes
    =========================== ========== ============================================
    `Visibility`_               **No**
    `Option Group`_             **No**     At least one of `Option Group`_ is required.
    =========================== ========== ============================================

Properties
    =============== =============== ======================================
    Property        Attribute       Description
    =============== =============== ======================================
    Name            name            The name of this install step.
    =============== =============== ======================================

-------------------------------------

Visibility
----------

Tag
    visible

Description
    The pattern against which to match the conditional flags and installed files.
    If the pattern is matched, then the install step will be visible.

Children
    =========================== ==========
    Node                        Repeatable
    =========================== ==========
    `File Dependency`_          **Yes**
    `Flag Dependency`_          **Yes**
    `Game Dependency`_          **No**
    `Dependencies`_             **Yes**
    =========================== ==========

Properties
    =============== =============== =============================================
    Property        Attribute       Description
    =============== =============== =============================================
    Type            operator        The type of the dependency: ``And`` or ``Or``

                                    If the type is ``And``, all conditions under
                                    this node must be met.

                                    If the type is ``Or``, only one condition
                                    must be met.
    =============== =============== =============================================

-------------------------------------

Dependencies
------------

Tag
    dependencies

Description
    A dependency that is made up of one or more dependencies.

Children
    =========================== ==========
    Node                        Repeatable
    =========================== ==========
    `File Dependency`_          **Yes**
    `Flag Dependency`_          **Yes**
    `Game Dependency`_          **No**
    `Dependencies`_             **Yes**
    =========================== ==========

Properties
    =============== =============== =============================================
    Property        Attribute       Description
    =============== =============== =============================================
    Type            operator        The type of the dependency: ``And`` or ``Or``

                                    If the type is ``And``, all conditions under
                                    this node must be met.

                                    If the type is ``Or``, only one condition
                                    must be met.
    =============== =============== =============================================

-------------------------------------

Option Group
------------

Tag
    optionalFileGroups

Description
    The list of optional files (or plugins) that may optionally be installed for this module.

Children
    =========================== ========== =====================================
    Node                        Repeatable Notes
    =========================== ========== =====================================
    `Group`_                    **Yes**    At least one of `Group`_ is required.
    =========================== ========== =====================================

Properties
    =============== =============== ======================================
    Property        Attribute       Description
    =============== =============== ======================================
    Order           order           The order of the install steps beneath
                                    this node.
                                    ``"Explicit"`` follows document
                                    order while the others order
                                    alphabetically.

                                    Accepts ``"Ascending"``,
                                    ``"Descending"`` or ``"Explicit"``
    =============== =============== ======================================

-------------------------------------

Group
-----

Tag
    group

Description
    A group of plugins for the mod.

Children
    =========================== ========== =======================================
    Node                        Repeatable Notes
    =========================== ========== =======================================
    `Plugins`_                  **No**     At least one of `Plugins`_ is required.
    =========================== ========== =======================================

Properties
    =============== =============== ======================================
    Property        Attribute       Description
    =============== =============== ======================================
    Name            name            The name of this group.
    Type            type            The selection type for this group.

                                    Accepts ``"SelectAny"``,
                                    ``"SelectAtMostOne"``,
                                    ``"SelectExactlyOne"``,
                                    ``"SelectAll"`` or
                                    ``"SelectAtLeastOne"``
    =============== =============== ======================================

-------------------------------------

Plugins
-------

Tag
    plugins

Description
    The list of plugins in the group.

Children
    =========================== ========== ======================================
    Node                        Repeatable Notes
    =========================== ========== ======================================
    `Plugin`_                   **Yes**    At least one of `Plugin`_ is required.
    =========================== ========== ======================================

Properties
    =============== =============== ======================================
    Property        Attribute       Description
    =============== =============== ======================================
    Order           order           The order of the plugins beneath
                                    this node.
                                    ``"Explicit"`` follows document
                                    order while the others order
                                    alphabetically.

                                    Accepts ``"Ascending"``,
                                    ``"Descending"`` or ``"Explicit"``
    =============== =============== ======================================

-------------------------------------

Plugin
------

Tag
    plugin

Description
    A mod plugin belonging to a group.

Children
    =========================== ========== =====================================================
    Node                        Repeatable Notes
    =========================== ========== =====================================================
    :ref:`config_desc_label`    **No**     At least one of :ref:`config_desc_label` is required.
    :ref:`plugin_image_label`   **No**
    `Files`_                    **No**
    `Flags`_                    **No**
    `Type Descriptor`_          **No**     At least one of `Type Descriptor`_ is required.
    =========================== ========== =====================================================

Properties
    =============== =============== ======================================
    Property        Attribute       Description
    =============== =============== ======================================
    Name            name            The name of this plugin.
    =============== =============== ======================================

-------------------------------------

.. _config_desc_label:

Description
-----------

Tag
    description

Description
    A description of the plugin.

Children
    *None*

Properties
    =============== =============== ===============================
    Property        Attribute       Description
    =============== =============== ===============================
    Description     [...]           The plugin's description.
    =============== =============== ===============================

-------------------------------------

.. _plugin_image_label:

Image
-----

Tag
    image

Description
    The optional image associated with a plugin.

Children
    *None*

Properties
    =============== =============== ===============================
    Property        Attribute       Description
    =============== =============== ===============================
    Path            path            The path to the image.
    =============== =============== ===============================

-------------------------------------

Files
-----

Tag
    files

Description
    A list of files and folders to be installed.

Children
    =========================== ==========
    Node                        Repeatable
    =========================== ==========
    `File`_                     **Yes**
    `Folder`_                   **Yes**
    =========================== ==========

Properties
    *None*

-------------------------------------

File
----

Tag
    file

Description
    A file belonging to the plugin or module.

Children
    *None*

Properties
    ================= =============== ===================================
    Property          Attribute       Description
    ================= =============== ===================================
    Source            source          The path to the file.
    Destination       destination     The path from the game's mod folder
                                      to the destination of this file.
    Priority          priority        The priority of the file.

                                      Higher priority means the file will
                                      overwrite other files with lower
                                      priority.
    Always Install    alwaysInstall   If ``true``, this file will be
                                      always installed, regardless of the
                                      user's choice.

                                      Accepts ``true`` or ``false``
    Install If Usable installIfUsable If ``true``, this file will be
                                      installed unless the plugin's type
                                      is ``NotUsable``, regardless of the
                                      user's choice.

                                      Accepts ``true`` or ``false``
    ================= =============== ===================================

-------------------------------------

Folder
------

Tag
    folder

Description
    A folder belonging to the plugin or module.

Children
    *None*

Properties
    ================= =============== ===================================
    Property          Attribute       Description
    ================= =============== ===================================
    Source            source          The path to the folder.
    Destination       destination     The path from the game's mod folder
                                      to the destination of this folder.
    Priority          priority        The priority of the folder.

                                      Higher priority means the folder
                                      will
                                      overwrite other files with lower
                                      priority.
    Always Install    alwaysInstall   If ``true``, this folder will be
                                      always installed, regardless of the
                                      user's choice.

                                      Accepts ``true`` or ``false``
    Install If Usable installIfUsable If ``true``, this folder will be
                                      installed unless the plugin's type
                                      is ``NotUsable``, regardless of the
                                      user's choice.

                                      Accepts ``true`` or ``false``
    ================= =============== ===================================

-------------------------------------

Flags
-----

Tag
    conditionFlags

Description
    The list of condition flags to set if the plugin is in the appropriate state.

Children
    =========================== ========== ====================================
    Node                        Repeatable Notes
    =========================== ========== ====================================
    `Flag`_                     **Yes**    At least one of `Flag`_ is required.
    =========================== ========== ====================================

Properties
    *None*

-------------------------------------

Flag
----

Tag
    flag

Description
    A condition flag to set if the plugin is selected.

Children
    *None*

Properties
    =============== =============== ===============================
    Property        Attribute       Description
    =============== =============== ===============================
    Label           name            The flag's identifying label.
    Value           [...]           The flag's new value.
    =============== =============== ===============================

-------------------------------------

Type Descriptor
---------------

Tag
    typeDescriptor

Description
    Describes the type of a plugin.

Children
    =========================== ========== ==================================================
    Node                        Repeatable Notes
    =========================== ========== ==================================================
    `Dependency Type`_          **No**     Either `Dependency Type`_ or `Type`_ must be used.
    `Type`_                     **No**     Either `Dependency Type`_ or `Type`_ must be used.
    =========================== ========== ==================================================

Properties
    *None*

-------------------------------------

Dependency Type
---------------

Tag
    dependencyType

Description
    Used when the plugin type is dependent upon the state of other mods.

Children
    =========================== ========== ===================================================
    Node                        Repeatable Notes
    =========================== ========== ===================================================
    :ref:`depend_patterns`      **No**     At least one of :ref:`depend_patterns` is required.
    `Default Type`_             **No**     At least one of `Default Type`_ is required.
    =========================== ========== ===================================================

Properties
    *None*

-------------------------------------

.. _depend_patterns:

Patterns
--------

Tag
    patterns

Description
    The list of dependency patterns against which to match the user's installation.
    The first pattern that matches the user's installation determines the type of the plugin.

Children
    =========================== ========== ==================================================
    Node                        Repeatable Notes
    =========================== ========== ==================================================
    :ref:`depend_pattern`       **Yes**    At least one of :ref:`depend_pattern` is required.
    =========================== ========== ==================================================

Properties
    *None*

-------------------------------------

.. _depend_pattern:

Pattern
-------

Tag
    pattern

Description
    A specific pattern of mod files and condition flags against which to match the user's installation.

Children
    =========================== ========== ============================================
    Node                        Repeatable Notes
    =========================== ========== ============================================
    `Dependencies`_             **No**     At least one of `Dependencies`_ is required.
    `Type`_                     **No**     At least one of `Type`_ is required.
    =========================== ========== ============================================

Properties
    *None*

-------------------------------------

Type
----

Tag
    type

Description
    The type of the plugin.

Children
    *None*

Properties
    =============== =============== ===============================
    Property        Attribute       Description
    =============== =============== ===============================
    Type            name            Describes the plugin's type.

                                    Accepts ``Required``,
                                    ``Recommended``, ``Optional``,
                                    ``CouldBeUsable`` or
                                    ``NotUsable``
    =============== =============== ===============================

-------------------------------------

Default Type
------------

Tag
    defaultType

Description
    The default type of the plugin used if none of the specified dependency states are satisfied.

Children
    *None*

Properties
    =============== =============== ===============================
    Property        Attribute       Description
    =============== =============== ===============================
    Type            name            Describes the plugin's type.

                                    Accepts ``Required``,
                                    ``Recommended``, ``Optional``,
                                    ``CouldBeUsable`` or
                                    ``NotUsable``
    =============== =============== ===============================

-------------------------------------

Mod Requirements
----------------

Tag
    requiredInstallFiles

Description
    The list of files and folders that must be installed for this module.

Children
    =========================== ==========
    Node                        Repeatable
    =========================== ==========
    `File`_                     **Yes**
    `Folder`_                   **Yes**
    =========================== ==========

Properties
    *None*

-------------------------------------

Conditional Installation
------------------------

Tag
    conditionalFileInstalls

Description
    The list of optional files that may optionally be installed for this module, based on condition flags.

Children
    =========================== ========== =================================================
    Node                        Repeatable Notes
    =========================== ========== =================================================
    :ref:`cond_patterns`        **No**     At least one of :ref:`cond_patterns` is required.
    =========================== ========== =================================================

Properties
    *None*

-------------------------------------

.. _cond_patterns:

Patterns
--------

Tag
    patterns

Description
    The list of patterns against which to match the conditional flags and installed files.
    All matching patterns will have their files installed.

Children
    =========================== ========== ================================================
    Node                        Repeatable Notes
    =========================== ========== ================================================
    :ref:`cond_pattern`         **Yes**    At least one of :ref:`cond_pattern` is required.
    =========================== ========== ================================================

Properties
    *None*

-------------------------------------

.. _cond_pattern:

Pattern
-------

Tag
    pattern

Description
    A specific pattern of mod files and condition flags against which to match the user's installation.

Children
    =========================== ========== ============================================
    Node                        Repeatable Notes
    =========================== ========== ============================================
    `Files`_                    **No**     At least one of `Files`_ is required.
    `Dependencies`_             **No**     At least one of `Dependencies`_ is required.
    =========================== ========== ============================================

Properties
    *None*
