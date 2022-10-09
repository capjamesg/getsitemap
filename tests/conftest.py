import pytest


@pytest.fixture
def sitemap_1() -> str:
    with open("tests/fixtures/test_sitemap.xml", "r") as file:
        return file.read()
