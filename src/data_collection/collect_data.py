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
import string


# define the module level constants
STRING_LENGTH = 5
DOC = "./src/data_collection/tmp_website.html"
DOC_2 = "./src/data_collection/original_text.txt"
# DOC_3 = "./src/data_collection/original_text_with_paragraphs.txt"
TIME_OUT = 60
FAIL = -1


########### this user agent should be modified to your own user agent ###########
# parameters setting for the Google Programmable Search Engine, which can be modified based on different users
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"


# These parameters for Google API are not used now, so they are deleted for protection of provacu
GOOGLE_CLOUD_KEY = None
SEARCH_ENGINE_CX = None


# define the mark to separate text from different sources while storing in the file
DELIMETER = "######"


# define the potential tags the websites may have for subtitles
SUB_TITLE_LIST = ["h", "h1", "h2", "h3"]


# define the overload number of webistes got from googlesearch
OVERLOAD_NUM = 30


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
        json_content = json.loads(content.decode("utf8", "ignore"))

        return json_content


    def googlesearch_search( self, question, result_num = 2 ):

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
            
        # for i in raw_websites_list:
        #     print(i)
        
        for web in raw_websites_list:
            if tmp_num >= result_num:
                break
            main_part = web.split("//")[1]
            main_part_1 = main_part.split("/")[0]
            # print(main_part)
            # print(main_part_1)
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
            response = urllib.request.urlopen(request)
            # file = open(DOC, "wb")
            # file.write(response)
            # file.close()

            # fetch the appropriate text from the website
            # try:
            #     soup = BeautifulSoup(open(DOC), features = "lxml")
            # except UnicodeDecodeError:
            #     return["", ""]
            # soup = BeautifulSoup(open(DOC), features = "lxml", from_encoding="utf-8")
            soup = BeautifulSoup(response.read().decode('utf-8', 'ignore'), features = "lxml")
            
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
    
    def optimized_web_clawer( self, websites, result_num = 2 ):
    
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
            
            # print(len(soup.find_all(SUB)))
            # print(sub_mark)
            # print(SUB)
            # print(soup.find_all(SUB))
            # print(len(soup.find_all(SUB)))
            if sub_mark == 1:
            
                curr_heading = soup.find(SUB)
                sub_len = len(soup.find_all(SUB))
                while idx < sub_len:
                
                    res_txt = ""
                    if idx > 0:
                        curr_heading = curr_heading.find_next_sibling(SUB)
                    # print(paras.find_next(SUB))
                    
                    # print(idx)
                    # print(curr_heading)
                    # print(curr_heading.find_next_sibling(SUB))
                    # print("\n")
                    
                    next_heading = curr_heading.find_next_sibling(SUB)
                    if next_heading == None:
                        break
                    else:
                        next_heading = next_heading.get_text()
                    paras = curr_heading
                    while paras.find_next().get_text() != next_heading:
                        paras = paras.find_next()
                        # print(paras)
                        # print(paras.name)
                        # if paras.name != "a" and paras.name != "style" and paras.name != "noscript" and paras.name != "aside":
                        #     print(paras.name)
                        #     res_txt += paras.get_text()
                        if paras.name == "p" or paras.name == "p1" or paras.name == "p2" or paras.name == "p3":
                            tmp_para_text = paras.get_text()
                            if len(tmp_para_text) > STRING_LENGTH:
                                res_txt += tmp_para_text
                    # top_sen = "One of the aspects is " + curr_heading.get_text().strip(string.digits).strip(". ") + ". "
                    top_sen = curr_heading.get_text().strip(string.digits).strip(". ") + ". "
                    tmp_text = top_sen + res_txt
                    
                    # print(tmp_text)
                    original_text.append(tmp_text)
                    idx += 1
                    
                
            elif sub_mark == 0:
                
                tmp_list = []
                tmp_list.append(url)
                original_text.append(CollectData.web_clawer( self, tmp_list, 1)[0][0])

        return original_text

        
def main2( question, res_num ):

    collect_data = CollectData()

    # apply Google Search to get the list of websites
    website_list = collect_data.googlesearch_search(question, res_num)

    # appply the web clawer to fetch the text
    # test if the Google Search results are valid
    if website_list == FAIL:
        print("The Google Search is invalid.")
        text_list = FAIL
    else:
        text_list = collect_data.optimized_web_clawer(website_list, res_num)

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
            # file.write(DELIMETER + "\n")
            file.write("\n")
    file.close()

    return text_list, website_list

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
            # file.write(DELIMETER + "\n")
            file.write("\n")
    file.close()

    # file_2 = open(DOC_3, "w", encoding = "UTF-8")
    # for text_id in range(len(text_list_2)):
    #     file_2.write(text_list_2[text_id])
    #     if text_id != len(text_list) - 1:
    #         file_2.write(DELIMETER + "\n")
    # file_2.close()

    return text_list, website_list


if __name__ == "__main__":
    question = "Methods of data mining"
    number = 1
    if main(question, number)[0] == FAIL:
        print("++++++++++ DATA COLLECTION FAIL ++++++++++\n")
    else:
        print("++++++++++ DATA COLLECTION SUCCESS ++++++++++\n")