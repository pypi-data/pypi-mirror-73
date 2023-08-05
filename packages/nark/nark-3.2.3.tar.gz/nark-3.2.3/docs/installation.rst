############
Installation
############

.. |virtualenv| replace:: ``virtualenv``
.. _virtualenv: https://virtualenv.pypa.io/en/latest/

.. |workon| replace:: ``workon``
.. _workon: https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html?highlight=workon#workon

To install system-wide, run as superuser::

    $ pip3 install nark

To install user-local, simply run::

    $ pip3 install -U nark

To install within a |virtualenv|_, try::

    $ mkvirtualenv nark
    (nark) $ pip3 install nark

To develop on the project, link to the source files instead::

    (nark) $ deactivate
    $ rmvirtualenv nark
    $ git clone git@github.com:tallybark/nark.git
    $ cd nark
    $ mkvirtualenv -a $(pwd) --python=/usr/bin/python3.7 nark
    (nark) $ make develop

After creating the virtual environment,
to start developing from a fresh terminal, run |workon|_::

    $ workon nark
    (nark) $ ...

