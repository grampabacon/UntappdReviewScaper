import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv

# Set the URL to scrape from
# url = "https://untappd.com/b/accidental-brewery-basking-sharks/3649109"


def get_untappd_data(url):
    # Setting up and Making the Web Call
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        headers = {'User-Agent': user_agent}
        # Make web request for that URL and don't verify SSL/TLS certs
        response = requests.get(url, headers=headers, verify=False)
        return response.text

    except Exception as e:
        print('ERROR - Untappd issue: {}'.format(str(e)))
        exit(1)


def get_beer_data(beer_id):
    # Parsing user information
    url = 'https://untappd.com/beer/{}'.format(beer_id)
    print("\n[ ] BEER DATA: Requesting {}".format(url))
    resp = get_untappd_data(url)

    html_doc = BeautifulSoup(resp, 'html.parser')
    review_bulk = html_doc.find_all("div", class_="checkin")  # soup.find_all("a", class_="sister")
    return review_bulk


def scrape_reviews(beer_id):
    data = get_beer_data(beer_id)

get_beer_data(3649109)
