# this file is to test the beautifulsoup

from bs4 import BeautifulSoup
import urllib.request as urlrequest
import urllib.parse
import string

FAIL = -1

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"

STRING_LENGTH = 5

SUB_TITLE_LIST = ["h", "h1", "h2", "h3"]

def optimized_web_clawer( websites, result_num = 2 ):

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
            
            print(len(soup.find_all(SUB)))
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
                    top_sen = "One of the aspects is " + curr_heading.get_text().strip(string.digits).strip(". ") + ". "
                    tmp_text = top_sen + res_txt
                    
                    # print(tmp_text)
                    original_text.append(tmp_text)
                    idx += 1
                    
                
            elif sub_mark == 0:
                # xxxxxx
                return "?"

        return original_text
    
def main():
    websites = ["https://www.talend.com/resources/data-mining-techniques/"]
    # websites = ["https://www.precisely.com/blog/datagovernance/top-5-data-mining-techniques?utm_medium=Redirect-Infogix&utm_source=Direct-Traffic"]
    data = optimized_web_clawer( websites, 1)
    data_collected = data
    file = open("./test_bf.txt", "w")
    for i in range(len(data_collected)):
        file.write(data_collected[i])
        file.write("\n")
    file.close()
    
if __name__ == "__main__":
    main()
