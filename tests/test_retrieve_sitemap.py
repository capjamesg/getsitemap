import responses

from getsitemap.retrieve_sitemap import retrieve_sitemap_urls


class TestReplyContext:
    @responses.activate
    def test_reply_context_1(self, sitemap_1):
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
