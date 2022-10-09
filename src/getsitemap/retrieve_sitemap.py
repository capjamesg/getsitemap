import concurrent.futures
import urllib.robotparser as rp
from typing import Dict, Union

import requests
from bs4 import BeautifulSoup


def concurrent_thread_starter(urls: list):
    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        processes = [executor.submit(_get_individual_sitemap, url) for url in urls]

        for process in concurrent.futures.as_completed(processes):
            results.update(process.result())

    return results


def _parse_list_of_urls(parsed_file: BeautifulSoup, root_url: str) -> dict:
    """
    Get all the URLs in a non-sitemapindex sitemap.
    """
    all_urls = {}

    for url in parsed_file.find_all("url"):
        if not url.find("loc") or not url.find("loc").text:
            continue
        if url.find("loc") and url.find("loc").text.endswith(".xml"):
            all_urls.update(_get_individual_sitemap(url.find("loc").text.strip()))
        elif url.find("loc"):
            if all_urls.get(root_url):
                all_urls[root_url].append(url.find("loc").text.strip())
            else:
                all_urls[root_url] = [url.find("loc").text.strip()]

    return all_urls


def _get_individual_sitemap(root_url: str) -> dict:
    """
    Get all of the URLs associated with a single sitemap.

    :param root_url: The URL of the sitemap.
    :type root_url: str
    :return: A dictionary of URLs found in each discovered sitemap.
    :rtype: dict
    """

    all_urls = {}

    try:
        sitemap_file = requests.get(root_url, timeout=10)
    except requests.exceptions.RequestException:
        return {}

    if sitemap_file.status_code != 200:
        return {}

    parsed_file = BeautifulSoup(sitemap_file.text, "xml")

    if parsed_file.find("sitemapindex"):
        # find all the urls in the sitemap index
        all_sitemaps = parsed_file.find_all("sitemap")

        sitemap_urls = list(set([sitemap.find("loc").text for sitemap in all_sitemaps if sitemap.find("loc")]))

        all_urls.update(concurrent_thread_starter(sitemap_urls))
    else:
        all_urls.update(_parse_list_of_urls(parsed_file, root_url))

    for key, value in all_urls.items():
        # remove duplicates
        all_urls[key] = list(set(value))

    return all_urls


def _flatten_sitemap_dictionaries(all_discovered_sitemaps: dict) -> dict:
    """
    Flatten a dictionary of sitemaps into a flat list.

    :param all_discovered_sitemaps: A dictionary of sitemaps.
    :type all_discovered_sitemaps: dict
    :return: A flat list of URLs.
    :rtype: list
    """
    flat_sitemaps: Dict[str, list] = {}
    for key, url in all_discovered_sitemaps.items():
        if isinstance(url, dict):
            for key, value in url.items():
                if flat_sitemaps.get(key):
                    flat_sitemaps[key].extend(value)
                else:
                    flat_sitemaps[key] = value
        else:
            flat_sitemaps[key] = url

    return flat_sitemaps


def retrieve_sitemap_urls(root_page: str, as_flat_list: bool = True) -> Union[list, dict]:
    """
    Find all of the URLs in every sitemap associated with a provided domain.

    This function will take a bit of time to run depending on how many URLs are discovered.

    :param root_page: The root page of the domain to search for sitemaps.
    :type root_page: str
    :param as_flat_list: Whether or not to return the URLs as a flat list.
    :type as_flat_list: bool
    :return: A list of URLs.
    :rtype: Union[list, dict]

    Example:

    .. code-block:: python

        import getsitemap

        all_urls = getsitemap.retrieve_sitemap_urls("https://www.example.com")

        print(all_urls) # ["https://www.example.com", "https://www.example.com/about", ...]
    """
    all_discovered_urls = {}

    parser = rp.RobotFileParser()
    parser.set_url(root_page.rstrip("/") + "/robots.txt")
    parser.read()

    sitemap_urls = parser.site_maps()

    if sitemap_urls:
        if root_page + "/sitemap.xml" not in sitemap_urls:
            sitemap_urls.append(root_page + "/sitemap.xml")

        unique_sitemaps = list(set(sitemap_urls))

        new_urls = concurrent_thread_starter(unique_sitemaps)

        all_discovered_urls.update(new_urls)

    if as_flat_list:
        return [url for url_list in all_discovered_urls.values() for url in url_list]
    else:
        return _flatten_sitemap_dictionaries(all_discovered_urls)
