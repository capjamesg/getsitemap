getsitemap
==========

.. image:: https://readthedocs.org/projects/getsitemap/badge/?version=latest
   :target: https://getsitemap.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://badge.fury.io/py/getsitemap.svg
   :target: https://badge.fury.io/py/getsitemap
   
.. image:: https://img.shields.io/pypi/dm/getsitemap
   :target: https://pypistats.org/packages/getsitemap

.. image:: https://img.shields.io/pypi/l/getsitemap
   :target: https://github.com/capjamesg/getsitemap/blob/main/LICENSE

.. image:: https://img.shields.io/pypi/pyversions/getsitemap
   :target: https://badge.fury.io/py/getsitemap
|

getsitemap is a Python library that retrieves all of the URLs that are found in all of the sitemaps on a website.

This project may be useful if you are building a search crawler or sitemap URL status code validators.

You can read the documentation for this project on `Read the Docs <https://getsitemap.readthedocs.io/en/latest/>`_.

Installation 💻
---------------

To get started, pip install `getsitemap`:

::

   pip install getsitemap
   
Quickstart ⚡
--------------

get all URLs recursively in all sitemaps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import getsitemap

   urls = getsitemap.get_individual_sitemap("https://jamesg.blog/sitemap.xml")

   print(urls)

get all URLs in a single sitemap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import getsitemap

   all_urls = getsitemap.retrieve_sitemap_urls("https://sitemap")

   print(all_urls)

Code Quality
-------------

This library uses `tox`, `pytest`, and `flake8` to assure code quality.

To run code quality checks, run the following command:

.. code-block:: bash

    tox

License 👩‍⚖️
----------

This project is licensed under an `MIT License <LICENSE>`_.

Contributing 🛠️
---------------

We would love to have your help in improving `getsitemap`. Have an idea for a new feature or a bug to fix? Leave information in a GitHub Issue to start a discussion!

If you have 

Contributors 💻
---------------

-  capjamesg
