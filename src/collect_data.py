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
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

# pip3 install google
from googlesearch import search
import string


STRING_LENGTH = 5

TIME_OUT = 60
FAIL = -1


########### this user agent should be modified to your own user agent ###########
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"


# define the mark to separate text from different sources while storing in the file
DELIMETER = "######"


# define the potential tags the websites may have for subtitles
SUB_TITLE_LIST = ["h", "h1", "h2", "h3"]


# define the overload number of webistes got from googlesearch
OVERLOAD_NUM = 30


def condense_spaces(text):
    return re.sub("\s\s+", " ", text)

filter_re = re.compile("(\b\w+\b){100}", flags=re.IGNORECASE)


def extract_text(soup):
    result = soup.findAll(text=filter_re)

    for r in result:
        r_text = condense_spaces(r.parent.text)
        print("\t(*) " + r_text)
        print('\n')


def googlesearch_search(question, result_num = 2 ):
    '''
        Apply the third-party package googlesearch to get the websites list from Google Search

        Keyword arguments:
        question -- the question posted by the user
        result_num -- the intended result number (default 2)
    '''

    raw_websites_list = []
    websites_list = []
    existed_websites_list = []
    tmp_num = 0

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
        
    
    for web in raw_websites_list:
        if tmp_num >= result_num:
            break
        main_part = web.split("//")[1]
        main_part_1 = main_part.split("/")[0]

        if main_part_1 not in existed_websites_list:
            existed_websites_list.append(main_part_1)
            websites_list.append(web)
            tmp_num += 1

    # print out the source of the original text
    print("\nThe results are from:")
    for i in websites_list:
        print (i)
    print("")
    
    # check if the websites number fits the requirement
    if len(websites_list) != result_num:
        print("The number of websites does not match the requirement.")
        return FAIL

    return websites_list


def web_clawer(websites, result_num = 2 ):
    '''
        Store the HTML content of websites into a temporary file and then claw the appropriate text from it using the BeautifulSoup
    
        Keyword arguments:
        websites -- the list storing the websites from Google Search results
        result_num -- the intended result number, same as the number of pieces of text from different websites
    '''

    original_text = []
    original_text_2 = []

    for website_idx in range(result_num):
        tmp_text = ""
        tmp_text_2 = ""

        # store the website into the temporary file
        url = websites[website_idx]
        header = {"User-Agent": USER_AGENT}
        request = urllib.request.Request(url, headers = header)
        response = urllib.request.urlopen(request)

        soup = BeautifulSoup(response.read().decode('utf-8', 'ignore'), features = "lxml")
        
        for p_idx in soup.select("p"):
            if len(p_idx.get_text().split()) > STRING_LENGTH:
                tmp_text += p_idx.get_text()
                # tmp_text_2 += p_idx.get_text() + "\n"
                original_text_2.append(p_idx.get_text())

        
        original_text.append(tmp_text)

    if len(original_text) != result_num:
        original_text = FAIL

    return [original_text, original_text_2]


def optimized_web_clawer(websites, result_num = 2 ):

    original_text = []
    sub_mark = 0

    for website_idx in range(result_num):

        tmp_text = ""
        header_list = []
        idx = 0

        # store the website into the temporary file
        url = websites[website_idx]
        header = {"User-Agent": USER_AGENT}
        request = urllib.request.Request(url, headers = header)
        response = urllib.request.urlopen(request)
        soup = BeautifulSoup(response.read().decode('utf-8', 'ignore'), features = "lxml")
        
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


if __name__ == "__main__":
    question = "Data structure history"
    res_num = 10

    # Get google search results urls
    website_list = googlesearch_search(question, res_num)

    if website_list == FAIL:
        print("The Google Search is invalid.")
        exit()

    # Fetch text from websites
    text_list = optimized_web_clawer(website_list, res_num)

    if text_list == FAIL:
        print("The Web Clawer is invalid.")
        exit()

    # Print out retrieved texts
    print("Retrieved texts: ")
    for text_id in range(len(text_list)):
        print("\t(*) " + text_list[text_id])
        print('\n')