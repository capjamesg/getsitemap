from collections import Counter

import src.getsitemap as getsitemap
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    url = request.args.get("url")
    export = request.args.get("export")

    if url:
        sitemap_urls = getsitemap.get_individual_sitemap(url, recurse=True)

        if len(sitemap_urls) == 0:
            return render_template("index.html", error="No sitemap found. Make sure you specify an XML file to parse.")

        for key, value in sitemap_urls.items():
            sitemap_urls[key] = sorted(value)

        all_urls = [url for urls in sitemap_urls.values() for url in urls]

        count = Counter(all_urls)

        total_urls = sum(count.values())

        duplicate_urls = [url for url, count in Counter(all_urls).items() if count > 1]

        # get all subpaths
        # like /
        # /x/
        # /x/y/
        # /x/y/z/

        subpaths = set()

        for url in all_urls:
            url = url.replace(url.strip("/").split("/")[-1], "").strip("/")
            subpaths.add(url)

        if export:
            # make into csv with format
            # url, sitemap
            csv_content = "url,sitemap\n"

            for key, value in sitemap_urls.items():
                for url in value:
                    csv_content += f"{url},{key}\n"

            # return as downloadable file
            response = app.response_class(
                csv_content,
                mimetype="text/csv",
                headers={"Content-disposition": f"attachment; filename=sitemap_urls.csv"},
            )

            return response

        return render_template(
            "index.html",
            sitemap_urls=sitemap_urls,
            duplicate_urls=duplicate_urls,
            count=total_urls,
            url=url,
            subpaths=subpaths,
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
