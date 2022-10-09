.. getsitemap documentation master file, created by
   sphinx-quickstart on Sun Oct  9 17:01:22 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to getsitemap's documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Get all URLs in a website's sitemaps
------------------------------------

The `retrieve_sitemap_urls()` function returns all URLs found in a website's sitemaps.

This function:

1. Checks for `Sitemap`` directives in a website's robots.txt file. All sitemap found are crawled recursively.
2. Checks for the presence of a sitemap.xml file. If one is found, it is crawled recursively.
3. Merges the results of all checks to return either a list of all URLs or a dictionary that maps each URL to the sitemap in which it was found.

.. autofunction:: getsitemap.retrieve_sitemap_urls

To get a list of all sitemaps in a website, you can append `.keys()` to the result of this function, as long as you specify `as_flat_list=False` in the command arguments.

Please note this function may take time to run if there are a lot of sitemaps to crawl. This is because a network request has to be made for each URL.