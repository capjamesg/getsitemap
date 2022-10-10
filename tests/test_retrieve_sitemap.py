import responses

from getsitemap.retrieve_sitemap import get_individual_sitemap, retrieve_sitemap_urls


class TestRetrieveSitemap:
    @responses.activate
    def test_retrieve_sitemap(self, sitemap_1):
        url = "https://jamesg.blog"

        responses.add(
            responses.GET,
            "https://jamesg.blog/sitemap.xml",
            body=sitemap_1,
            status=200,
            content_type="application/xml",
        )

        all_urls = retrieve_sitemap_urls(url)

        assert len(all_urls) == 1719

    @responses.activate
    def test_retrieve_single_sitemap(self, sitemap_1):
        url = "https://jamesg.blog/sitemap.xml"

        responses.add(
            responses.GET,
            "https://jamesg.blog/sitemap.xml",
            body=sitemap_1,
            status=200,
            content_type="application/xml",
        )

        all_urls = get_individual_sitemap(url)

        assert list(all_urls.keys()) == ["https://jamesg.blog/sitemap.xml"]
        assert len(all_urls["https://jamesg.blog/sitemap.xml"]) == 1719
