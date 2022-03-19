'''
    @author Zhenke Chen
    @date 28/09/2021

    Collect data from Google Search with two steps:
    1. Use the Google Programmable Search Engine to fetch all the websites from the Google Search results
    2. Apply BeautifulSoup as the web clawer to collect the text from the websites
'''

import urllib.request as urlrequest
import urllib.parse
import requests
import ssl
import json
from bs4 import BeautifulSoup, SoupStrainer
from bs4.element import NavigableString

# pip3 install google
from googlesearch import search
import string
import unidecode


STRING_LENGTH = 5

TIME_OUT = 60
FAIL = -1


########### this user agent should be modified to your own user agent ###########
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"


# define the mark to separate text from different sources while storing in the file
DELIMETER = "######"


# define the overload number of webistes got from googlesearch
OVERLOAD_NUM = 30


def condense_spaces(text):
    return ' '.join(text.split())



def extract_text(soup, text_filter):
    passages = soup.find_all(string=text_filter)

    passages = [unidecode.unidecode(str(p)) for p in passages if type(p) == NavigableString]
    passages = [condense_spaces(p) for p in passages]

    return passages
    


SUB_TITLE_LIST = ["h", "h1", "h2", "h3"]

def extract_chunks(soup):
    """
        Similar to above, except considers groups chunks of text under the same heading. This was the original method written by Zhenke
    """
    sub_mark = 0

    for i in SUB_TITLE_LIST:
        if len(soup.find_all(i)) == 0:
            continue
        elif len(soup.find_all(i)) > 4:
            SUB = i
            sub_mark = 1
            break
    

    if sub_mark == 1:
    
        curr_heading = soup.find(SUB)
        sub_len = len(soup.find_all(SUB))
        while idx < sub_len:
        
            res_txt = ""
            if idx > 0:
                curr_heading = curr_heading.find_next_sibling(SUB)
            
            next_heading = curr_heading.find_next_sibling(SUB)
            if next_heading == None:
                break
            else:
                next_heading = next_heading.get_text()
            paras = curr_heading
            while paras.find_next().get_text() != next_heading:
                paras = paras.find_next()
                if paras.name == "p" or paras.name == "p1" or paras.name == "p2" or paras.name == "p3":
                    tmp_para_text = paras.get_text()
                    if len(tmp_para_text) > STRING_LENGTH:
                        res_txt += tmp_para_text

            top_sen = curr_heading.get_text().strip(string.digits).strip(". ") + ". "
            tmp_text = top_sen + res_txt
            
            original_text.append(tmp_text)
            idx += 1      
        
    elif sub_mark == 0:
        tmp_list = []
        tmp_list.append(url)
        original_text.append(CollectData.web_clawer( tmp_list, 1)[0][0])

    return original_text


def filter_url(url):
    """
        Returns true if valid url
    """
    is_pdf = ".pdf" in url 
    is_wiki = "wikipedia" in url

    return not is_pdf and not is_wiki


def get_gsearch_urls(question, result_num = 2 ):
    '''
        Apply the third-party package googlesearch to get the websites list from Google Search

        Keyword arguments:
        question -- the question posted by the user
        result_num -- the intended result number (default 2)
    '''

    raw_websites_list = []

    # apply the googlesearch package to get the raw websites list,
    # which has the overload number of websites to avoid the irrelevant websites
    for i in search(
        query = question,           # define the question to search
        tld = "com",                # define the top level domain
        lang = "en",                # define the searching language
        num = 10,                   # define the number of results per page
        start = 0,                  # define the first result to retrieve
        stop = OVERLOAD_NUM,          # define the last result to retrieve
        pause = 2.0                 # define the lapse to wait between HTTP requests
    ):
        raw_websites_list.append(i)
        
    websites_list = []

    # Extract unique urls (duplicate if from same root)
    seen_websites = set()
    num_unique = 0
    
    for web in raw_websites_list:
        main_part = web.split("//")[1]
        main_part_1 = main_part.split("/")[0]

        if main_part_1 not in seen_websites:
            seen_websites.add(main_part_1)
            websites_list.append(web)
            num_unique += 1

    websites_list = [w for w in websites_list if filter_url(w)]
    websites_list = websites_list[:result_num]

    return websites_list



def fetch_candidate_texts(question, num_websites = 5, text_filter=lambda t: True):
    websites = get_gsearch_urls(question, num_websites)

    # Contains tuples of the form (url, [p1, p2, ...])
    url_data = []

    for url in websites:

        # Fetch url page
        header = {"User-Agent": USER_AGENT}
        request = urllib.request.Request(url, headers = header)

        try:
            response = urllib.request.urlopen(request)
        except:
            continue

        # print(response.get_content_type())

        # Parse using beautiful soup
        soup = BeautifulSoup(response.read().decode('utf-8', 'ignore'), features = "lxml")
        # soup = BeautifulSoup(response.read().decode('utf-8', 'ignore'), "html.parser")

        text_passages = extract_text(soup, text_filter=text_filter)
        if len(text_passages) == 0:
            continue

        content_type = response.info().get_content_type()
        cur_url_data = {
            "url": url,
            "type": content_type,
            "passages": text_passages
        }
        url_data.append(cur_url_data)

    return url_data



if __name__ == "__main__":
    question = "Data structure history"
    res_num = 10

    # Fetch text from websites
    text_list = fetch_candidate_texts(website_list, res_num)
    print(json.dumps(text_list, indent=4))