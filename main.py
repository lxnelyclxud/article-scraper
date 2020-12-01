import textwrap
import os
import sys
import json
from urllib.parse import urlsplit, urljoin
from mss import Scraper
from bs4 import NavigableString


class ArticleScraper(Scraper):
    def __init__(self, config):
        self.config = config

    def parse(self):
        def filter(tag):  # "filter" function for BeautifulSoup's find_all method
            return (
                tag.name in config["banned_tags"]
                or (
                    any(
                        tag_class.lower() in " ".join(tag["class"]).lower()
                        for tag_class in config["banned_classes"]
                        if tag.has_attr("class")
                    )
                    and tag.name != "body"
                )
                or (
                    any(
                        tag_id.lower() in tag["id"].lower()
                        for tag_id in config["banned_classes"]
                        if tag.has_attr("id")
                    )
                    and tag.name != "body"
                )
            )

        # clear out the response based on filter
        [tag.decompose() for tag in self.html.find_all(filter)]

        # finds lowest tag containing the most amount of paragraph tags
        content = max(
            self.html.body.find_all(),
            key=lambda child: len(child.find_all("p", recursive=False)),
        )

        # if href links to the same site append it to site's base url
        url_format = (
            lambda href: href
            if "http" in href
            else urljoin("://".join(urlsplit(self.url)[:2]), href)
        )

        # constructing final article text
        self.article = textwrap.fill(self.html.title.text, width=80) + "\n" * 3
        for tag in content:
            if not isinstance(tag, NavigableString):
                if tag.text.strip() != "":
                    for link in tag.find_all("a"):
                        link.append(f" [{url_format(link['href'])}]")
                        link.unwrap()
                    self.article += f"{textwrap.fill(tag.text, width=80)} \n\n"

    def to_file(self):
        url_scheme = urlsplit(self.url).scheme  # http(s)
        path_from_url = os.path.normpath(
            self.url.replace(f"{url_scheme}://", "").replace("www.", "")
        )
        file_path = os.path.join(
            "scraped_articles", f"{os.path.splitext(path_from_url)[0]}.txt"
        )

        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.article)
            print(f"File {file_path} saved")


if __name__ == "__main__":
    config = None
    url = None

    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
    except FileNotFoundError as ex:
        print("Config file not found near exe")

    if config:
        if len(sys.argv) > 1:
            url = sys.argv[1]
        else:
            print("No URL provided as an argument")

            url = input("You can paste it here instead: ")

        try:
            scraper = ArticleScraper(config)
            scraper.from_url(url)
            scraper.parse()
            scraper.to_file()
        except Exception as ex:
            print(ex)