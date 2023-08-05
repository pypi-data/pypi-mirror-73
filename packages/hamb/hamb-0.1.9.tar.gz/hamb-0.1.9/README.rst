********************************
Health and Monitoring Bot (HAMB)
********************************

Getting started with HAMB

.. image:: https://img.shields.io/pypi/v/hamb.svg
   :target: https://pypi.python.org/pypi/hamb
   :alt: Pypi Version
.. image:: https://travis-ci.org/readthedocs/hamb.svg?branch=master
   :target: https://travis-ci.org/readthedocs/hamb
   :alt: Build Status
.. image:: https://readthedocs.org/projects/sphinx-rtd-theme/badge/?version=latest
  :target: http://sphinx-rtd-theme.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status


Local setup
============

It is recommended to use the steps below to set up a virtual environment for development:

.. code-block:: console

  python3 -m venv <virtual env name>
  source <virtual env name>/bin/activate
  pip install -r requirements.txt

  or

  pip install hamb

Save credentials to ``etl.cfg`` file locally in project directory. See ``sample.etl.cfg`` file provided in root directory.


Directory Structure
===================

By default, it will look for manifests folder, etl.cfg and services.yaml in your current working directory.

.. code-block:: console

  hamb/
  manifests/
  etl.cfg
  services.yaml


Manifests
=========

This is about metadata about your test sets, including the sql and diagnostic queries to be run. Manifests files are stored in
``/manifests``


Services
============

``services.yaml`` This is a global config which stores outbound communication details.
Basically it says for a given scenerio, what handlers will be used, and with what targets.


Handlers
========

Test results are printed, but handlers are available for other means of notification.
See ``/hamb/handlers/``.

.. code-block:: console

  email_handler
  sftp_handler
  slack_handler
  sql_compo_list
  sql_comp
  watch_file_handler
  jenkins_handler
  sns_handler

Execution walkthru
===================

* HAMB will be executed from command line for a given manifest (test set): ``hamb -m sample_compare``
* It will read the tests from the corresponding manifest file into a Python object
* It will then loop through each test
* For each test it will execute the appropriate plugin
* The results from each test will be collected, then as configured in services.yaml the appropriate handler will be evoked
* Based on the services metadata, the appropriate handler will be evoked with parameters for that service (email list, sns topic, etc)

Go ahead, compose your own and try it out..


Examples
========

Compare two lists wherein it succeeds when the lists are the same and fails when different.

Try running ``hamb -m sample_compare`` or ``python -m hamb.module -m sample_compare``

.. code-block:: console

  Examples:

  a. when lists are the same
  'script_a_result': [a, b, c]
  'script_b_result': [a, b, c]
  'status': 'success'
  'diff': None

  b. when only a few elements are similar
  'script_a_result': [a, b, c]
  'script_b_result': [a, b]
  'status': 'failure'
  'diff': [c]

  c. when one list is empty
  'script_a_result': [a, b, c]
  'script_b_result': []
  'status': 'failure'
  'diff': [a, b, c]

  d. when lists have completely different elements
  'script_a_result': [a, b, c]
  'script_b_result': [d, e, f]
  'status': 'failure'
  'diff': [a, b, c, d, e, f]


If the manifest is in another folder, you can provide the absolute path

.. code-block:: console

  hamb -m /path/to/sample_compare

If you want to use AWS secrets, just include --config secret_manager param.

.. code-block:: console

  hamb -m sample_compare --config secret_manager

Hamb also supports logging the results to the database. To use this feature, include -t <your_database_table>.
See: ``/hamb/ham_run_utility.py``:``save_db_log()`` method for sample table schema.

.. code-block:: console

  hamb -m sample_compare --t public.hambot_history


Tests
============

To run the testing suite, the following commands are required:

.. code-block:: console

  pip install -r requirements-dev.txt

  tox

  or

  python -m unittest discover tests


Documentation
=============

HAMB documentation is powered by `Sphinx <https://www.sphinx-doc.org/en/master/>`_, a tool that makes documentation easy.

To build docs locally

.. code-block:: console

  cd docs
  make html

To see HAMB documentation, open ``/docs/_build/html/index.html``.

If you want to make changes, edit ``README.rst`` and build docs again.
