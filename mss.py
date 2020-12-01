import csv
import requests
from bs4 import BeautifulSoup


class Scraper:
    def from_url(self, url):
        response = requests.get(url)
        self.url = url
        if response.ok:
            self.html = BeautifulSoup(response.content, "lxml")
        else:
            print("Bad response")

    def from_file(self, file_name, url):
        with open(file_name, "r", encoding="utf-8") as file:
            self.url = url
            self.html = BeautifulSoup(file.read(), "lxml")

    def to_file(self, content, file_name):
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)

    def to_csv(self, content, file_name, fieldnames):
        with open(file_name, "w", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            [writer.writerow(row) for row in content]
