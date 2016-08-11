Contributing
============

We love contributions from everyone.
By participating in this project,
you agree to abide by the thoughtbot `code of conduct <https://thoughtbot.com/open-source-code-of-conduct>`_.

Issues
++++++

Before submitting your issue, please make sure that you've provided all the info
required in the issue template.

Pull Requests
+++++++++++++

Before submitting your pull request, please make sure that you've provided all the 
info required in the pull request template.

Contributing Code
+++++++++++++++++

**General Guidelines**:

    * This repo uses the `gitflow <https://github.com/nvie/gitflow>`_ branching model.
      Don't commit directly to the ``master`` or ``develop`` branches.

    * Make sure the tests pass on the CI server. Local tests are not available at the moment.

    * Follow the `style guide <https://www.python.org/dev/peps/pep-0008/>`_.

    * Write `decent commit messages <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.

    * Run :command:`inv docs` to generate documentation locally, :command:`inv build` to build the executable and
      :command:`inv preview` to preview the app without building it.

**Setup the work environment**:

    1. `Fork the repo <https://help.github.com/articles/fork-a-repo/>`_.

    2. `Setup your fork locally <https://help.github.com/articles/fork-a-repo/#keep-your-fork-synced>`_.

    3. This repo uses a ``.settings`` file to define all the necessary settings. This file follows this syntax:

        .. code-block:: ini

            [git]
            user=git_username
            email=git_email

        Create and add this file to your clone's root.

    4. Install `Vagrant <https://www.vagrantup.com/docs/installation/>`_.

    5. Run this in the clone's root:

        * If you have Python available:

            .. code-block:: shell

                pip install invoke
                inv create enter

        * If not:

            .. code-block:: shell

                vagrant up
                vagrant ssh -- -Yt 'cd /vagrant/; /bin/bash'

       It will take a while.

    6. You should now be inside an Ubuntu Trusty virtual machine, this is where you'll work.
       Make, commit and push your changes.

    7. `Create a pull request <https://help.github.com/articles/creating-a-pull-request/>`_.

Thank you, `contributors <https://github.com/GandaG/fomod-editor/graphs/contributors>`_!
