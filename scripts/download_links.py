import os, sys, glob, re
import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import uuid

from config import LINK_LIST_PATH

# Encoding for writing the URLs to the .txt file
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"


def save_link(url, page):
    """
    Save collected link/url and page to the .txt file in LINK_LIST_PATH
    """
    id_str = uuid.uuid3(uuid.NAMESPACE_URL, url).hex
    with open(LINK_LIST_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([id_str, url, str(page)]) + "\n")


def download_links_from_index():
    """
    This function should go to the defined "url" and download the news page links from all
    pages and save them into a .txt file.
    """

    # Checking if the link_list.txt file exists
    if not os.path.exists(LINK_LIST_PATH):
        with open(LINK_LIST_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "url", "page"]) + "\n")
        start_page = 0
        downloaded_url_list = []

    # If some links have already been downloaded,
    # get the downloaded links and start page
    else:
        # Get the page to start from
        data = pd.read_csv(LINK_LIST_PATH, sep="\t")
        if data.shape[0] == 0:
            start_page = 0
            downloaded_url_list = []
        else:
            start_page = data["page"].astype("int").max()
            downloaded_url_list = data["url"].to_list()

    # WRITE YOUR CODE HERE
    #########################################
    # Start downloading from the page "start_page"
    # which is the page you ended at the last
    # time you ran the code (if you had an error and the code stopped)

    rootURL = "http://foreign.gov.vc/foreign/index.php/news"
    contURL = "http://foreign.gov.vc/foreign/index.php/news?start="

    for pid in range((start_page*30)-30,300,30):

        if pid == 0:
            pageURL = rootURL
        else:
            pageURL = "{}{}".format(contURL, pid)

        resp = requests.get(pageURL)
        soup = bs(resp.text, features="lxml")

        for item in soup.find_all("td", {"class": "list-title"}):

            hreflink = item.find("a", href=True)
            collected_url = "http://foreign.gov.vc" + hreflink["href"]
            pageid = int((pid/30) + 1)

            # Save the collected url in the variable "collected_url"
            # Save the page that the url is taken from in the variable "pageid"

            if collected_url not in downloaded_url_list:
                print("\t", collected_url, flush=True)
                save_link(collected_url, pageid)

    # The following code block saves the collected url and page
    # Save the collected urls one by one so that if an error occurs
    # you do not have to start all over again

    #########################################


if __name__ == "__main__":
    download_links_from_index()
