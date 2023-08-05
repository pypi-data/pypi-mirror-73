=============
API Reference
=============

.. panels::
   :body: text-center

    :opticon:`file-code,size=24`

    .. link-button:: python-api
        :type: ref
        :text: Python API Reference
        :classes: btn-outline-primary btn-block stretched-link

    ---

    :opticon:`terminal,size=24`

    .. link-button:: command-line-api
        :type: ref
        :text: Command Line API Reference
        :classes: btn-outline-primary btn-block stretched-link


.. _python-api:

Python API Reference
====================

.. currentmodule:: coiled

.. autosummary::
    Cloud
    CoiledCluster

Cloud
-----

.. autoclass:: Cloud
    :members:
    :undoc-members:


CoiledCluster
-------------

.. autoclass:: CoiledCluster
    :members:
    :undoc-members:


.. _command-line-api:

Command Line API Reference
==========================

.. click:: coiled.cli.login:login
   :prog: coiled login
   :show-nested:

.. click:: coiled.cli.env:create
   :prog: coiled env create
   :show-nested:
