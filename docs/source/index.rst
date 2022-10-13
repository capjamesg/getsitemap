.. getsitemap documentation master file, created by
   sphinx-quickstart on Sun Oct  9 17:01:22 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to getsitemap's documentation!
======================================

`getsitemap` is a simple Python library that retrieves all the URLs in the sitemaps associated with a website.

This library may be useful when building a web search crawler, an SEO validation tool, or a sitemap monitor.

You can download `getsitemap` using the following comamnd:

.. code-block:: bash

   pip install getsitemap

See the documentation for `getsitemap` below.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Get all URLs in a website's sitemaps
------------------------------------

The `retrieve_sitemap_urls()` function returns all URLs found in a website's sitemaps.

This function:

1. Checks for `Sitemap` directives in a website's robots.txt file. All sitemap found are crawled recursively.
2. Checks for the presence of a sitemap.xml file. If one is found, it is crawled recursively.
3. Merges the results of all checks to return either a list of all URLs or a dictionary that maps each URL to the sitemap in which it was found.

.. autofunction:: getsitemap.retrieve_sitemap_urls

To get a list of all sitemaps in a website, you can append `.keys()` to the result of this function, as long as you specify `as_flat_list=False` in the command arguments.

Please note this function may take time to run if there are a lot of sitemaps to crawl. This is because a network request has to be made for each URL.

Get all URLs in a single sitemap
--------------------------------

The `get_individual_sitemap()` function returns all URLs found in a single sitemap.

With the `recurse=True` argument, this function will also crawl all sitemaps found in the sitemap and do so recursively.

If `recurse=False`, this function will return only the list of URLs in the provided sitemap file. This will include sitemap files if you use this function on a sitemap index.

.. autofunction:: getsitemap.get_individual_sitemap

Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a
Changelog <https://keepachangelog.com/en/1.0.0/>`__, and this project
adheres to `Semantic
Versioning <https://semver.org/spec/v2.0.0.html>`__.

[0.1.1] - 2022-10-09
--------------------

Added
~~~~~

-  Refactored ``get_individual_sitemap`` to allow use as a public
   function.
-  Documentation for the ``get_individual_sitemap`` function.

.. _section-1:

[0.1.0] - 2022-10-09
--------------------

.. _added-1:

Added
~~~~~

-  Initial release of ``getsitemap``.
-  ``retrieve_sitemap_urls`` to retrieve all the URLs from a sitemap.
-  Documentation for the ``retrieve_sitemap_urls`` function.
