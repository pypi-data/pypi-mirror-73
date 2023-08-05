===============
Getting started
===============

.. currentmodule:: coiled

Installation
============

Coiled can be installed from PyPI using ``pip`` or from the conda-forge
channel using ``conda``:


.. panels::
    :body: text-center
    :header: text-center h5 bg-white

    Install with pip
    ^^^^^^^^^^^^^^^^

    .. code-block:: bash

        pip install coiled

    ---

    Install with conda
    ^^^^^^^^^^^^^^^^^^

    .. code-block:: bash

        conda install -c conda-forge coiled

Setup
=====

Coiled comes with a ``coiled login`` command line tool to configure
your account credentials. From the command line enter:

.. code-block:: bash

    $ coiled login


You'll then be asked to navigate to https://dev.coiledhq.com/profile to log in and
retreieve your Coiled token.

.. code-block:: bash

    Please login to https://dev.coiledhq.com/profile to get your token
    Token:

Upong entering your token, your credentials will be saved to Coiled's local
configuration file. Coiled will then pull credentials from the configuration
file when needed.


.. _first-computation:

Running your first computation
==============================

When performing computations on remote Dask clusters, it's important to have the same libraries
installed both in your local Python environment (e.g. on your laptop), as well as on the remote
Dask workers in your cluster. Coiled helps you seamlessly synchronize these software environments.
While there's more detailed information on this topic is available in the User Guide,
for now we'll just use the ``coiled env create`` command line tool for creating a standard
conda environment locally. From the command line:

.. code-block:: bash

    # Create local version of the coiled/default software environment
    $ coiled env create coiled/default

    # Activate the conda environment
    $ conda activate coiled-default

Now that we have our software environment set up, we can walk through the following example:

.. code-block:: python

    # Connect to Coiled
    from coiled import Cloud

    cloud = Cloud()

    # Create a remote Dask cluster managed by Coiled
    from coiled import CoiledCluster

    cluster = CoiledCluster(configuration="coiled/default")

    # Connect a Dask Client to the cluster
    from dask.distributed import Client

    client = Client(cluster)

    # Start performing computations!
    import dask.datasets

    df = dask.datasets.timeseries()
    df[["x", "y"]].resample("1h").mean().compute()


.. note::

    Note that when creating a ``CoiledCluster``, resources for our Dask cluster are
    provisioned on AWS. This provisioning process takes about a minute to complete

The example above goes through the following steps:

- Connects to Coiled by creating a :class:`Cloud` instance
  (this will pull your Coiled credentials from the ``coiled login`` setup step).
  The ``Cloud`` object is how you connect to and interact with Coiled.
- Spins up a remote Dask cluster by creating a :class:`CoiledCluster` instance.
- Connects a Dask ``Client`` to the cluster.
- Submits a Dask DataFrame computation for execution on the cluster.

To view the Dask diagnostics dashboard for you cluster, see the output of:

.. code-block:: python

    client.dashboard_link

which will look something like ``"http://ec2-3-22-74-94.us-east-2.compute.amazonaws.com:8787/status"``.


Making your own software environment
====================================

In the previous :ref:`first-computation` section, we used the pre-built "coiled/default" software environment to get started.
However, often you'll want to create your own custom software environment with the libraries you need.
This can be done with the :meth:`Cloud.create_software_environment` method. For example:

.. code-block:: python

    cloud.create_software_environment(
        name="my-conda-env",
        conda={
            "channels": ["conda-forge"],
            "dependencies": ["dask", "xarray>=0.15", "numba"],
        },
    )

will create a new Coiled software environment named "<coiled-account>/my-conda-env", where "<coiled-account>"
is the name of your current Coiled account, and uses conda to install dask, version 0.15.1 of xarray, and numba
from the ``conda-forge`` conda channel.

Once you've created a new Coiled software environment, you can use the ``conda env create`` command line tool
to create the same software environment locally:

.. code-block:: bash

    $ coiled env create <coiled-account>/my-conda-env
    $ conda activate <coiled-account>-my-conda-env

where, again, "<coiled-account>" should be replaced with the name of *your* Coiled account.


Making your own cluster configuration
=====================================

In the :ref:`first-computation` section, we passed ``configuration="coiled/default"``
when creating a ``CoiledCluster`` instance. This resulted in our cluster being launched
with certain resources. Namely, the cluster consisted of:

- 4 workers, each with 1 CPU and 4 GiB of memory
- A scheduler with 1 CPU and 4 GiB of memory
- The scheduler and each worker use the "coiled/default" software environment,
  which has Dask and a few other packages installed (e.g. NumPy, Pandas, Bokeh)

Outlining what resources and software environment your cluster should use is a crucial part
of modern workflows. To facilitate this, Coiled uses the concept of a **cluster configuration**
as a template, or recipe, for the resources you cluster should have. Use the
:meth:`Cloud.create_cluster_configuration` method to create a new cluster configuration.
For example:

.. code-block:: python

    # Create "my-cluster-config" cluster configuration
    cloud.create_cluster_configuration(
        name="my-cluster-config",
        worker_memory="16 GiB",
        worker_cpu=4,
        scheduler_memory="4 GiB",
        scheduler_cpu=1,
        software="coiled/default",
    )

creates a cluster configuration named "my-cluster-config" where the scheduler
has 1 CPU / 4 GiB of memory, workers each have 4 CPUs / 16 GiB of memory, and
the "coiled/default" software environment is used for the scheduler and all workers.
Each input can be modified as needed, including using custom software environments
you've created.

To create a cluster which uses the "my-cluster-config" cluster configuration,
pass the configuration name to ``CoiledCluster``:

.. code-block:: python

    from coiled import Cloud, CoiledCluster

    # Connect to Coiled
    cloud = Cloud()

    # Create a Dask cluster based on the "my-cluster-config" configuration
    cluster = CoiledCluster(configuration="my-cluster-config")


Next steps
==========

This page has illustrates some the core concepts of Coiled. For more in-depth
discussion of these features, additional examples, and more, please see the
:ref:`User Guide <user-guide>`.

.. link-button:: user_guide/index
    :type: ref
    :text: Go To User Guide
    :classes: btn-outline-primary btn-block

Happy computing!
