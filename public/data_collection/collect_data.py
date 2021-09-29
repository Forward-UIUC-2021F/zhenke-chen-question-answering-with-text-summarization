'''
    @author Zhenke Chen
    @date 28/09/2021

    Collect data from Google Search with two steps:
    1. Use the Google Programmable Search Engine to fetch all the websites from the Google Search results
    2. Apply BeautifulSoup as the web clawer to collect the text from the websites
'''

# import the required packages
import urllib.request as urlrequest
import urllib.parse
import requests
import ssl
import json
from bs4 import BeautifulStoneSoup
from bs4 import SoupStrainer

# define the module level constants
STRING_LENGTH = 5
DOC = "tmp_website.html"
TIME_OUT = 60

# parameters setting for the Google Programmable Search Engine, which can be modified based on different users
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
GOOGLE_CLOUD_KEY = "AIzaSyA-Wb9q_61coW7iPJtGlJJOrB9oTRAdcVg"
SEARCH_ENGINE_CX = "64828619eec714ab8"


def google_search( question, result_num = 2):
    
    '''
        Apply the google search and get all the results based on the API of Google Programmable Search Engine

        Keyword arguments:
        question -- the question posted by the user
        result_num -- the intended result number (default 1)
    '''

    # create the API based on the question and settings
    url = "https://www.googleapis.com/customsearch/v1?key="+ GOOGLE_CLOUD_KEY + "&q=" + question + "&cx=" + SEARCH_ENGINE_CX + "&start=1&num=" + str(result_num)
    headers = {"User-Agent": USER_AGENT}

    # fetch the results from API and store it as JSON
    content = urlrequest.urlopen(url, TIME_OUT).read()
    json_content = json.loads(content.decode("utf8"))

    return json_content