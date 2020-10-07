import requests
import pandas as pd
import time


class Scrape():
    def __init__(self, request_mode, api_key):

        self.request_mode = request_mode

        self.api_key = api_key

        self.df = pd.read_csv("./hashes.csv", names=["hashes"])

        self.hashes = list(self.df["hashes"])

        self.len_hashes = len(self.hashes)

        self.api_key = api_key

        self.parameters = {
            "apikey": self.api_key
        }

    def scraper(self, hash):
        url = "https://virusshare.com/apiv2/{}?apikey={}&hash={}".format(
            self.request_mode, self.api_key, hash)
        print(url)
        headers = {"Accept": "text/html, application/xhtml+xml, application/xml",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Accept-Language": "en-US, en",
                   "User-Agent": "Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}

        try:
            response = requests.request(
                "GET", url, headers=headers)
        except Exception:
            print("******Error getting response with the hash******")

        file_name = response.headers["Content-Disposition"].split("filename=")[
            1]
        print("Downloading {}".format(file_name))
        open(file_name, 'wb').write(response.content)


sc = Scrape("download", "API_KEY_HERE")


for each in sc.hashes:
    try:
        sc.scraper(each)
    except Exception:
        print("Holding to follow 4 requests per minute!")
        time.sleep(60)
        sc.scraper(each)
