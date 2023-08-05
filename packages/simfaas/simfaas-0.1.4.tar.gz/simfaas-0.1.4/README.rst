SimFaaS: A Serverless Performance Simulator
===========================================

|Binder| |PyPI| |PyPI - Status| |Upload Python Package| |Docker Image
CI| |Documentation Status| |Libraries.io dependency status for latest
release| |GitHub|

This is a project done in `PACS Lab <https://pacs.eecs.yorku.ca/>`__
aiming to develop a performance simulator for serverless computing
platforms. Using this simulator, we can calculate Quality of Service
(QoS) metrics like average response time, the average probability of
cold start, average running servers (directly reflecting average cost),
a histogram of different events, distribution of the number of servers
throughout time, and many other characteristics.

The developed performance model can be used to debug/improve analytical
performance models, try new and improved management schema, or dig up a
whole lot of properties of a common modern scale-per-request serverless
platform.

Artifacts
---------

-  `PyPi Package <https://pypi.org/project/simfaas/>`__
-  `Github Repo <https://github.com/pacslab/simfaas>`__
-  `ReadTheDocs
   Documentation <https://simfaas.readthedocs.io/en/latest/>`__
   (`PDF <https://simfaas.readthedocs.io/_/downloads/en/latest/pdf/>`__)
-  `Examples <./examples>`__ (`MyBinder Jupyter
   Lab <https://mybinder.org/v2/gh/pacslab/simfaas/production?urlpath=lab%2Ftree%2Fexamples%2F>`__)

Requirements
------------

-  Python 3.6 or above
-  PIP

Installation
------------

Install using pip:

.. code:: sh

   pip install simfaas

Upgrading using pip:

.. code:: sh

   pip install simfaas --upgrade

For installation in development mode:

.. code:: sh

   git clone https://github.com/pacslab/simfaas
   cd simfaas
   pip install -e .

And in case you want to be able to execute the examples:

.. code:: sh

   pip install -r examples/requirements.txt

Usage
-----

A simple usage of the serverless simulator is shown in the following:

.. code:: py

   from simfaas.ServerlessSimulator import ServerlessSimulator as Sim

   sim = Sim(arrival_rate=0.9, warm_service_rate=1/1.991, cold_service_rate=1/2.244,
               expiration_threshold=600, max_time=1e6)
   sim.generate_trace(debug_print=False, progress=True)
   sim.print_trace_results()

Which prints an output similar to the following:

::

   100%|██████████| 1000000/1000000 [00:42<00:00, 23410.45it/s]
   Cold Starts / total requests:    1213 / 898469
   Cold Start Probability:          0.0014
   Rejection / total requests:      0 / 898469
   Rejection Probability:           0.0000
   Average Instance Life Span:      6335.1337
   Average Server Count:            7.6612
   Average Running Count:           1.7879
   Average Idle Count:              5.8733

Using this information, you can predict the behaviour of your system in
production.

Development
-----------

In case you are interested in improving this work, you are always
welcome to open up a pull request. In case you need more details or
explanation, contact me.

To get up and running with the environment, run the following after
installing ``Anaconda``:

.. code:: sh

   conda env create -f environment.yml
   conda activate simenv
   pip install -r requirements.txt
   pip install -e .

After updating the README.md, use the following to update the README.rst
accordingly:

.. code:: sh

   bash .travis/readme_prep.sh

Examples
--------

Some of the possible use cases of the serverless performance simulator
are shown in the ``examples`` folder in our Github repository.

License
-------

Unless otherwise specified:

MIT (c) 2020 Nima Mahmoudi & Hamzeh Khazaei

Citation
--------

You can find the paper with details of the simultor in `PACS lab
website <https://pacs.eecs.yorku.ca/publications/>`__. You can use the
following bibtex entry for citing our work:

.. code:: bib

   Coming Soon...

.. |Binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/pacslab/simfaas/production?urlpath=lab%2Ftree%2Fexamples%2F
.. |PyPI| image:: https://img.shields.io/pypi/v/simfaas.svg
   :target: https://pypi.org/project/simfaas/
.. |PyPI - Status| image:: https://img.shields.io/pypi/status/simfaas.svg
.. |Upload Python Package| image:: https://github.com/pacslab/simfaas/workflows/Upload%20Python%20Package/badge.svg
.. |Docker Image CI| image:: https://github.com/pacslab/simfaas/workflows/Docker%20Image%20CI/badge.svg
.. |Documentation Status| image:: https://readthedocs.org/projects/simfaas/badge/?version=latest
   :target: https://simfaas.readthedocs.io/en/latest/?badge=latest
.. |Libraries.io dependency status for latest release| image:: https://img.shields.io/librariesio/release/pypi/simfaas.svg
.. |GitHub| image:: https://img.shields.io/github/license/pacslab/simfaas.svg

