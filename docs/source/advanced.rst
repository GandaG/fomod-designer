.. include:: <isotech.txt>

Advanced Usage
==============

For the advanced users and everyone who knows their way around a FOMOD installer.
In this section you'll find descriptions of the tags and nodes themselves - what they are, how to use them and
examples when needed.

There are no restrictions when using the ``Advanced View``, we trust that you know what you're doing.
This is recommended for people who already know how to create/modify XML
installers and are interested in speeding up their work or for users who want more customization options than the
``Basic View`` offers.

Advanced View
+++++++++++++

.. Describe the advanced view and how to use it.


Learn you a FOMOD For Great Good
++++++++++++++++++++++++++++++++

This section contains the *FOMOD Bible* - a description of all the tags/nodes with examples.
This is not meant to be read from top to bottom but rather as a dictionary or a glossary -
search for the tag/node you need more info for with the search box on the left sidebar.

Tag vs Node
...........

A **Tag** is any item within an xml document. Within the FOMOD schema
(the document that defines the rules for installer documents)
all the allowed tags for FOMOD are defined. A tag has the format ``<tag/>`` or
``<tag>text goes here<tag/>`` if it contains text.

Similarly, any item in the *FOMOD Designer*'s *Object Tree* is a **Node**.
Every node has a direct correspondence to a xml tag.
These two terms are use interchangeably in the *FOMOD Bible*.

Attribute vs Property
.....................

An **Attribute** is a way to customize a tag. These are also defined in the FOMOD schema and have the format:
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

While this is not strictly enforced with nodes, some tags are enforced a specific order by the FOMOD schema.
When applicable, the possible/required children listed in each node are ordered.

-------------------------------------

Info
....

Tag
    fomod

Description
    The root node for the document containing all the information relative to the installer.

Children
    ====================== =========== ===========
    Nodes                  Minimum No. Maximum No.
    ====================== =========== ===========
    :ref:`info_name_label` 0           |infin|
    `Author`_              0           |infin|
    :ref:`info_desc_label` 0           |infin|
    `ID`_                  0           |infin|
    `Categories Group`_    0           |infin|
    `Version`_             0           |infin|
    `Website`_             0           |infin|
    ====================== =========== ===========

Properties
    *None*

-------------------------------------

.. _info_name_label:

Name
....

Tag
    Name

Description
    The node that holds the mod's name.

Children
    *None*

Properties
    =============== =============== ===============================
    Properties      Attributes      Description
    =============== =============== ===============================
    Text            [...]           The name of the mod.
    =============== =============== ===============================

-------------------------------------

Author
......

Tag
    Author

Description
    The node that holds the mod's author(s).

Children
    *None*

Properties
    =============== =============== ===============================
    Properties      Attributes      Description
    =============== =============== ===============================
    Text            [...]           The author(s) of the mod.
    =============== =============== ===============================

-------------------------------------

.. _info_desc_label:

Description
...........

Tag
    Description

Description
    The node that holds the mod's description.

Children
    *None*

Properties
    =============== =============== ===============================
    Properties      Attributes      Description
    =============== =============== ===============================
    Text            [...]           The description of the mod.
    =============== =============== ===============================

-------------------------------------

ID
..

Tag
    Id

Description
    The node that holds the mod's ID.
    The ID is the last part of the nexus' link. Example:

    Nexus mod link: http://www.nexusmods.com/skyrim/mods/548961 / ID becomes 548961

Children
    *None*

Properties
    =============== =============== ===============================
    Properties      Attributes      Description
    =============== =============== ===============================
    Text            [...]           The ID of the mod.
    =============== =============== ===============================

-------------------------------------

Categories Group
................

Tag
    Groups

Description
    This node's purpose is solely to group the categories this mod belongs to together.

Children
    ====================== =========== ===========
    Nodes                  Minimum No. Maximum No.
    ====================== =========== ===========
    `Category`_            0           |infin|
    ====================== =========== ===========

Properties
    *None*

-------------------------------------

Category
........

Tag
    element

Description
    The node that holds one of the mod's category.

Children
    *None*

Properties
    =============== =============== ===============================
    Properties      Attributes      Description
    =============== =============== ===============================
    Text            [...]           A category this mod belongs to.
    =============== =============== ===============================

-------------------------------------

Version
.......

Tag
    Version

Description
    The node that holds the mod's version.

Children
    *None*

Properties
    =============== =============== ===============================
    Properties      Attributes      Description
    =============== =============== ===============================
    Text            [...]           This mod's version.
    =============== =============== ===============================

-------------------------------------

Website
.......

Tag
    Website

Description
    The node that holds the mod's home website.

Children
    *None*

Properties
    =============== =============== ===============================
    Properties      Attributes      Description
    =============== =============== ===============================
    Text            [...]           The mod's home website.
    =============== =============== ===============================

-------------------------------------

Config
......

Tag
    config

Description
    The main element containing the module configuration info.

Children
    *None*


Properties

-------------------------------------

.. _config_desc_label:

Name
....

Tag
    moduleName

Description
    The name of the module. Used to describe the display properties of the module title.

Children
    *None*


Properties

-------------------------------------

Image
.....

Tag
    moduleImage

Description
    The module logo/banner.

    *[Ignored in Mod Organizer]*

Children
    *None*


Properties

-------------------------------------

Mod Dependencies
................

Tag
    moduleDependencies

Description
    Items upon which the module depends. The installation process will only start after these conditions have been met.

    While flag dependencies are allowed they should not be used since no flag will have been set at the time these
    conditions are checked.

Children
    *None*


Properties

-------------------------------------

File Dependency
...............

Tag
    fileDependency

Description
    Specifies that a mod must be in a specified state.

Children
    *None*


Properties

-------------------------------------

Flag Dependency
...............

Tag
    flagDependency

Description
    Specifies that a condition flag must have a specific value.

Children
    *None*


Properties

-------------------------------------

Game Dependency
...............

Tag
    gameDependency

Description
    Specifies a minimum required version of the installed game.

    *[Ignored in Mod Organizer]*

Children
    *None*


Properties

-------------------------------------

Installation Steps
..................

Tag
    installSteps

Description
    The list of install steps that determine which files (or plugins) that may optionally be installed for this module.

Children
    *None*


Properties

-------------------------------------

Install Step
............

Tag
    installStep

Description
    A step in the install process containing groups of optional plugins.

Children
    *None*


Properties

-------------------------------------

Visibility
..........

Tag
    visible

Description
    The pattern against which to match the conditional flags and installed files.
    If the pattern is matched, then the install step will be visible.

Children
    *None*


Properties

-------------------------------------

Dependencies
............

Tag
    dependencies

Description
    A dependency that is made up of one or more dependencies.

Children
    *None*


Properties

-------------------------------------

Option Group
............

Tag
    optionalFileGroups

Description
    The list of optional files (or plugins) that may optionally be installed for this module.

Children
    *None*


Properties

-------------------------------------

Group
.....

Tag
    group

Description
    A group of plugins for the mod.

Children
    *None*


Properties

-------------------------------------

Plugins
.......

Tag
    plugins

Description
    The list of plugins in the group.

Children
    *None*


Properties

-------------------------------------

Plugin
......

Tag
    plugin

Description
    A mod plugin belonging to a group.

Children
    *None*


Properties

-------------------------------------

Description
...........

Tag
    description

Description
    A description of the plugin.

Children
    *None*


Properties

-------------------------------------

Image
.....

Tag
    image

Description
    The optional image associated with a plugin.

Children
    *None*


Properties

-------------------------------------

Files
.....

Tag
    files

Description
    A list of files and folders to be installed.

Children
    *None*


Properties

-------------------------------------

File
....

Tag
    file

Description
    A file belonging to the plugin or module.

Children
    *None*


Properties

-------------------------------------

Folder
......

Tag
    folder

Description
    A folder belonging to the plugin or module.

Children
    *None*


Properties

-------------------------------------

Flags
.....

Tag
    conditionFlags

Description
    The list of condition flags to set if the plugin is in the appropriate state.

Children
    *None*


Properties

-------------------------------------

Flag
....

Tag
    flag

Description
    A condition flag to set if the plugin is selected.

Children
    *None*


Properties

-------------------------------------

Type Descriptor
...............

Tag
    typeDescriptor

Description
    Describes the type of a plugin.

Children
    *None*


Properties

-------------------------------------

Dependency Type
...............

Tag
    dependencyType

Description
    Used when the plugin type is dependent upon the state of other mods.

Children
    *None*


Properties

-------------------------------------

Patterns
........

Tag
    patterns

Description
    The list of dependency patterns against which to match the user's installation.
    The first pattern that matches the user's installation determines the type of the plugin.

Children
    *None*


Properties

-------------------------------------

Pattern
.......

Tag
    pattern

Description
    A specific pattern of mod files and condition flags against which to match the user's installation.

Children
    *None*


Properties

-------------------------------------

Type
....

Tag
    type

Description
    The type of the plugin.

Children
    *None*


Properties

-------------------------------------

Default Type
............

Tag
    defaultType

Description
    The default type of the plugin used if none of the specified dependency states are satisfied.

Children
    *None*


Properties

-------------------------------------

Mod Requirements
................

Tag
    requiredInstallFiles

Description
    The list of files and folders that must be installed for this module.

Children
    *None*


Properties

-------------------------------------

Conditional Installation
........................

Tag
    conditionalFileInstalls

Description
    The list of optional files that may optionally be installed for this module, based on condition flags.

Children
    *None*


Properties

-------------------------------------

Patterns
........

Tag
    patterns

Description
    The list of patterns against which to match the conditional flags and installed files.
    All matching patterns will have their files installed.

Children
    *None*


Properties

-------------------------------------

Pattern
.......

Tag
    pattern

Description
    A specific pattern of mod files and condition flags against which to match the user's installation.

Children
    *None*


Properties

