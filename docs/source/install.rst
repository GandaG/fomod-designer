Installation
============

**TL;DR:** All you need to do is `download the package <https://github.com/GandaG/fomod-editor/releases/latest>`_,
extract it somewhere and run the ``FOMOD Designer`` executable.

Pre-Built Executables
+++++++++++++++++++++

There are pre-built, ready-to-use executables always available for
64-bit Windows and often for 64-bit Linux as well.

It is recommended to use the `latest stable version <https://github.com/GandaG/fomod-editor/releases/latest>`_
since it's less likely to have critical bugs. If you need to use a feature that
hasn't made it to the stable builds, feel free to download the `bleeding edge build <>`_.

If there are no builds for your system or you just love to have tons
of work try building from source.

Building from Source
++++++++++++++++++++

1. Download the `repository from Github <>`_;

2. Unpack the archive into a folder;

3. Install `Conda <>`_;

4. Open the command line/terminal in the folder from step 2;

5. Create the necessary environment within Conda:

    * Windows 64-bit:

        .. code-block:: batch

            conda create -y -n fomod-designer^
             -c https://conda.anaconda.org/mmcauliffe^
             pyqt5=5.5.1 python=3.5.1 lxml=3.5.0

    * Linux 64-bit:

        .. code-block:: shell

            conda create -y -n fomod-designer \
             -c https://conda.anaconda.org/mmcauliffe \
             pyqt5=5.5.1 python=3.5.1 lxml=3.5.0

    * For other platforms you'll have to figure out where the correct Conda packages are. As of now, you'll need these:

        ======= =======
        Package Version
        ======= =======
        PyQt5   5.5.1
        lxml    3.5.0
        ======= =======

6. Activate the environment:

    * Windows:

        .. code-block:: batch

            activate fomod-designer

    * Other:

        .. code-block:: shell

            source activate fomod-designer

7. Install other dependencies:

    * Windows:

        .. code-block:: batch

            pip install pip -U
            pip install setuptools -U --ignore-installed
            pip install -r dev\reqs.txt

    * Other:

        .. code-block:: shell

            pip install pip -U
            pip install setuptools -U --ignore-installed
            pip install -r dev/reqs.txt

8. Build the app:

    .. code-block:: shell

        inv build

9. Done! The built package is in the ``dist`` folder within the folder in step 2.
