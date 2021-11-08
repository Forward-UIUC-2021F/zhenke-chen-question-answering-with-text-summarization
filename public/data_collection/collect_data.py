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
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from googlesearch import search


# define the module level constants
STRING_LENGTH = 5
DOC = "./public/data_collection/tmp_website.html"
DOC_2 = "./public/data_collection/original_text.txt"
DOC_3 = "./public/data_collection/original_text_with_paragraphs.txt"
TIME_OUT = 60
FAIL = -1

# parameters setting for the Google Programmable Search Engine, which can be modified based on different users
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"


# These parameters for Google API are not used now, so they are deleted for protection of provacu
GOOGLE_CLOUD_KEY = None
SEARCH_ENGINE_CX = None


# define the mark to separate text from different sources while storing in the file
DELIMETER = "######"


class CollectData():

    def __init__( self ):
        pass


    # This Google API is not used now 
    def google_search( question, result_num = 2 ):
        
        '''
            Apply the google search and get all the results based on the API of Google Programmable Search Engine

            Keyword arguments:
            question -- the question posted by the user
            result_num -- the intended result number (default 2)
        '''

        # create the API based on the question and settings
        url = "https://www.googleapis.com/customsearch/v1?key="+ GOOGLE_CLOUD_KEY + "&q=" + question + "&cx=" + SEARCH_ENGINE_CX + "&start=1&num=" + str(result_num)
        headers = {"User-Agent": USER_AGENT}

        # fetch the results from API and store it as JSON
        content = urlrequest.urlopen(url, TIME_OUT).read()
        json_content = json.loads(content.decode("utf8"))

        return json_content


    def googlesearch_search( self, question, result_num = 2 ):

        '''
            Apply the third-party package googlesearch to get the websites list from Google Search

            Keyword arguments:
            question -- the question posted by the user
            result_num -- the intended result number (default 2)
        '''

        websites_list = []

        # apply the googlesearch package to get the websites list
        for i in search(
            query = question,           # define the question to search
            tld = "com",                # define the top level domain
            lang = "en",                # define the searching language
            num = 10,                   # define the number of results per page
            start = 0,                  # define the first result to retrieve
            stop = result_num,          # define the last result to retrieve
            pause = 2.0                 # define the lapse to wait between HTTP requests
        ):
            websites_list.append(i)

            # test the websites list
            # print(i)

        # check if the websites number fits the requirement
        if len(websites_list) != result_num:
            print("The number of websites does not match the requirement.")
            return FAIL

        return websites_list
    

    # This transformation from json to python data is currently not used
    def fetch_json( self, json_content ):

        '''
            Fetch the list of websites from the json content

            Keyword arguments:
            json_content -- json content from API
        '''

        # convert the json content into python data and then extract the websites
        python_data = json.loads(json_content)
        websites_list = [i.link for i in range(len(python_data.items))]

        return websites_list


    def web_clawer( self, websites, result_num = 2 ):

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
            response = urllib.request.urlopen(request).read()
            file = open(DOC, "wb")
            file.write(response)
            file.close()

            # fetch the appropriate text from the website
            soup = BeautifulSoup(open(DOC), features = "lxml")
            for p_idx in soup.select("p"):
                if len(p_idx.get_text().split()) > STRING_LENGTH:
                    tmp_text += p_idx.get_text()
                    # tmp_text_2 += p_idx.get_text() + "\n"
                    original_text_2.append(p_idx.get_text())

            
            original_text.append(tmp_text)
            # original_text_2.append(tmp_text)
            
            # The loop is too long for the one-line coding style
            # original_text = [p_idx.get_text() for p_idx in soup.select("p") if len(p_idx.get_text().split()) > STRING_LENGTH]

        # test
        # print(original_text)
        # print(len(original_text))

        # test if the number of original text satisfies the requirement
        if len(original_text) != result_num:
            original_text = FAIL

        return [original_text, original_text_2]

        
def main( question, res_num ):

    '''
        Get searching results from Google Search with question and output as a list

        Keyword arguments:
        question -- the question post by the user
        res_num -- the result number determined by the user
    '''

    collect_data = CollectData()

    # apply Google Search to get the list of websites
    website_list = collect_data.googlesearch_search(question, res_num)

    # appply the web clawer to fetch the text
    # test if the Google Search results are valid
    if website_list == FAIL:
        print("The Google Search is invalid.")
        text_list = FAIL
    else:
        text_list = collect_data.web_clawer(website_list, res_num)[0]
        text_list_2 = collect_data.web_clawer(website_list, res_num)[1]

        # test if the Web Clawer results are valid
        if text_list == FAIL:
            print("The Web Clawer is invalid.")
            text_list = FAIL
        else:
            # print out the original text for demonstration
            # for i in text_list:
            #     print(i)
            # print(i for i in text_list)
            pass
        
    # store the orginal text into orginal_text.txt
    file = open(DOC_2, "w", encoding = "UTF-8")
    for text_id in range(len(text_list)):
        file.write(text_list[text_id])
        # to make the demonstration more clear, split each result with three blank lines
        if text_id != len(text_list) - 1:
            file.write(DELIMETER + "\n")
    file.close()

    file_2 = open(DOC_3, "w", encoding = "UTF-8")
    for text_id in range(len(text_list_2)):
        file_2.write(text_list_2[text_id])
        if text_id != len(text_list) - 1:
            file_2.write(DELIMETER + "\n")
    file_2.close()

    return text_list


if __name__ == "__main__":
    question = "What is TensorFlow?"
    number = 6
    if main(question, number) == FAIL:
        print("++++++++++ DATA COLLECTION FAIL ++++++++++")
    else:
        print("++++++++++ DATA COLLECTION SUCCESS ++++++++++")