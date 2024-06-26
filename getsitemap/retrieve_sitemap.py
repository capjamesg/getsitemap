import concurrent.futures
import urllib.robotparser as rp
from typing import Dict, Union

import requests
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"


def _concurrent_thread_starter(
    urls: list, thread_max: int, allow_xml_inference: bool, dedupe_results: bool
):
    """
    Create a pool of threads to retrieve sitemap files.

    :param urls: A list of URLs to retrieve.
    :type urls: list
    :param thread_max: The maximum number of threads to use in sitemap retrieval requests.
    :type thread_max: int
    :param allow_xml_inference: Whether or not to infer that a URL ending in .xml is a sitemap.
    :type allow_xml_inference: bool
    :param dedupe_results: Whether or not to deduplicate the results.
    :type dedupe_results: bool
    :return: A dictionary of URLs found in each discovered sitemap.
    :rtype: dict
    """
    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_max) as executor:
        processes = [
            executor.submit(
                get_individual_sitemap, url, dedupe_results, allow_xml_inference
            )
            for url in urls
        ]

        for process in concurrent.futures.as_completed(processes):
            results.update(process.result())

    return results


def _parse_list_of_urls(
    parsed_file: BeautifulSoup,
    root_url: str,
    allow_xml_inference: bool = True,
    recurse: bool = True,
    dedupe_results: bool = True,
) -> dict:
    """
    Get all the URLs in a non-sitemapindex sitemap.

    :param parsed_file: The parsed sitemap file.
    :type parsed_file: BeautifulSoup
    :param root_url: The URL of the sitemap.
    :type root_url: str
    :param allow_xml_inference: Whether or not to infer that a URL ending in .xml is a sitemap.
    :type allow_xml_inference: bool
    :return: A dictionary of URLs found in each discovered sitemap.
    :rtype: dict
    """
    all_urls = {}

    for url in parsed_file.find_all("url"):
        if not url.find("loc") or not url.find("loc").text:
            continue
        if (
            url.find("loc")
            and url.find("loc").text.endswith(".xml")
            and allow_xml_inference
        ):
            if recurse is False:
                all_urls.update(
                    get_individual_sitemap(
                        url.find("loc").text.strip(),
                        allow_xml_inference,
                        dedupe_results,
                    )
                )
        elif url.find("loc"):
            if all_urls.get(root_url):
                all_urls[root_url].append(url.find("loc").text.strip())
            else:
                all_urls[root_url] = [url.find("loc").text.strip()]

    return all_urls


def get_individual_sitemap(
    root_url: str,
    thread_max: int = 20,
    dedupe_results: bool = True,
    allow_xml_inference: bool = True,
    recurse: bool = True,
    user_agent: str = USER_AGENT,
) -> dict:
    """
    Get all of the URLs associated with a single sitemap.

    :param root_url: The URL of the sitemap.
    :type root_url: str
    :param thread_max: The maximum number of threads to use in sitemap retrieval requests.
    :type thread_max: int
    :param allow_xml_inference: Whether or not to infer that a URL ending in .xml is a sitemap.
    :type allow_xml_inference: bool
    :param recurse: Whether or not to recurse into other sitemaps.
    :type recurse: bool
    :param user_agent: The user agent to use in requests.
    :type user_agent: str
    :return: A dictionary of URLs found in each discovered sitemap.
    :rtype: dict

    Example:

    .. code-block:: python

        import getsitemap

        urls = getsitemap.get_individual_sitemap("https://jamesg.blog/sitemap.xml")

        print(urls) # ["https://jamesg.blog/2020/09/01/my-experience-with-jekyll/", ...]
    """

    all_urls = {}

    try:
        sitemap_file = requests.get(
            root_url, timeout=10, headers={"User-Agent": user_agent}
        )
    except requests.exceptions.RequestException:
        print(f"Could not retrieve sitemap at {root_url} (network error).")
        return {}

    if not sitemap_file.ok:
        print(
            f"Could not retrieve sitemap at {root_url} (site returned non-200 status code)."
        )
        return {}

    parsed_file = BeautifulSoup(sitemap_file.text, "lxml")

    if parsed_file.find("sitemapindex"):
        # find all the urls in the sitemap index
        all_sitemaps = parsed_file.find_all("sitemap")

        sitemap_urls = list(
            set(
                [
                    sitemap.find("loc").text
                    for sitemap in all_sitemaps
                    if sitemap.find("loc")
                ]
            )
        )

        if recurse:
            all_urls.update(
                _concurrent_thread_starter(
                    sitemap_urls, thread_max, allow_xml_inference, dedupe_results
                )
            )
        else:
            return {root_url: sitemap_urls}
    else:
        all_urls.update(_parse_list_of_urls(parsed_file, root_url, allow_xml_inference))

    if dedupe_results:
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


def retrieve_sitemap_urls(
    root_page: str,
    as_flat_list: bool = True,
    allow_xml_inference: bool = True,
    thread_max: int = 20,
    dedupe_results: bool = True,
) -> Union[list, dict]:
    """
    Find all of the URLs in every sitemap associated with a provided domain.

    This function will take a bit of time to run depending on how many URLs are discovered.

    :param root_page: The root page of the domain to search for sitemaps.
    :type root_page: str
    :param as_flat_list: Whether or not to return the URLs as a flat list.
    :type as_flat_list: bool
    :param allow_xml_inference: Whether or not to infer that a URL ending in .xml is a sitemap.
    :type allow_xml_inference: bool
    :param thread_max: The maximum number of threads to use in sitemap retrieval requests.
    :type thread_max: int
    :param dedupe_results: Whether or not to remove duplicate URLs.
    :type dedupe_results: bool
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

        new_urls = _concurrent_thread_starter(
            unique_sitemaps, thread_max, allow_xml_inference, dedupe_results
        )

        all_discovered_urls.update(new_urls)

    if as_flat_list:
        return [url for url_list in all_discovered_urls.values() for url in url_list]
    else:
        return _flatten_sitemap_dictionaries(all_discovered_urls)
