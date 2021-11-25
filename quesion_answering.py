'''
    @author Zhenke Chen
    @date 15/11/2021

    Overall question answering file, together with test cases
'''


# import the required packages
import urllib
from collections import OrderedDict
from itertools import repeat


# import the necessary functions from other files
from public.data_collection.collect_data import main as collect_data
from public.text_summarization.summarizer import main2 as text_summarization


# define the path to store the result
RESULT_PATH = "./result.txt"


# define the number of websites for each subquestion
WEB_NUM = 6


# define the number of candidate answers for each subquestion
CANDIDTE_NUM = 5


# define the list of subqeustion
# SUB_QUESTIONS = ["What is ", "History of ", "Method of "]
SUB_QUESTIONS = ["What is ", "Method of ", "Application of "]
# SUB_QUESTIONS = ["What is ", "History of ", "Applications of "]
# SUB_QUESTIONS = ["History of ", "Applications of "]
# SUB_QUESTIONS = ["What is "]
# SUB_QUESTIONS = ["History of "]
# SUB_QUESTIONS = ["Method of "]
# SUB_QUESTIONS = ["Applications of "]


def answer_question(keyword):

    '''
        There are mainly three steps in this function:
        1. Answer all the subquestions for the keyword
        2. Store the results as a page with reference in the certain file
        
        Keyword arguments:
        keyword -- the keyword to generate the subquestions
    '''
    
    # store the reuslt as a page into the file
    with open(RESULT_PATH, "w") as file_object:
        
        for sub_id in range(len(SUB_QUESTIONS)):
            
            retry_num = 0
            success_tag = 0
            
            # construct the question with subquestion and keyword
            tmpquestion = SUB_QUESTIONS[sub_id] + keyword
            
            # create the header into the file for each subquestions
            file_object.write(str(sub_id + 1) + ". " + tmpquestion + "\n\n")
            
            # deal with the url error with certain number of retries
            while(retry_num < 5):
                try:
                    # obtain the websites list of original text as references
                    # also, collect the data with Data Collection module
                    data_collected = collect_data(tmpquestion, WEB_NUM)
                    if data_collected[0] == -1:
                        print("++++++++++ DATA COLLECTION FAIL ++++++++++\n")
                        file_object.close()
                        return
                    reference_list = data_collected[1]
                except urllib.error.URLError or urllib.error.HTTPError:
                    print("The internet is not stable, retrying...")
                    retry_num += 1
                else:
                    retry_num = 5
                    success_tag = 1
            retry_num = 0
            
            if success_tag == 0:
                print("The question cannot be answered because of the poor Internet connection.")
                file_object.close()
                return
            
            # summarize the original text with Text Summarization module
            answer = text_summarization(tmpquestion)
            
            # input the answer into the file
            file_object.write(answer + "\n\n")
            
            # input the reference list into the file
            file_object.write("References:\n")
            for web in reference_list:
                file_object.write(web + "\n")
            file_object.write("\n")
    
    file_object.close()     
        
    return

def result_selection(text_list):
    
    '''
        This function is to select the best result from several answers generated,
        the goal is to select the one with least repeatability
        
        Keyword arguments:
        text_list: the list of all candidate answers
    '''
    
    alternatives = {}
    optimized_ans_list = []
    
    # simplify every candidate answers by removing the repetitive parts
    for text_idx in range(len(text_list)):
        optimized_answer = ""
        tmp_txt = text_list[text_idx]
        
        # deal with some cases that the answer starts with one or two spaces
        if tmp_txt[:2] == "  ":
            tmp_txt = tmp_txt[2:]
        elif tmp_txt[:1] == " ":
            tmp_txt = tmp_txt[1:]
            
        # deal with some cases that the answer has blank lines
        tmp_txt = tmp_txt.replace("\n\n", "")
        
        # deal with some cases that there is no space after the period for each sentence
        tmp_txt = tmp_txt.replace(". ", ".")
            
        # split the answer sentence by sentence
        splitted = tmp_txt.split(".")
        splitted_len = len(splitted)
        # last_sentence = splitted[splitted_len - 1]
        # last_sentence_len = len(last_sentence)
        # if last_sentence[last_sentence_len - 1] == ".":
        #     splitted[splitted_len - 1] = last_sentence[: last_sentence_len - 1]
            
        res = list(OrderedDict(zip(splitted, repeat(None))))
        res_len = len(res)
        alternatives[text_idx] = res_len
        for i in range(res_len):
            if i != res_len - 2 and i != res_len - 1:
                optimized_answer += res[i] + ". "
            elif i == res_len - 2:
                optimized_answer += res[i] + "."
        # print(optimized_answer)
        optimized_ans_list.append(optimized_answer)
        
    # print(optimized_ans_list)
    max_id = max(alternatives, key = lambda k: alternatives[k])
    ans = optimized_ans_list[max_id]
    # print(ans)
    return ans


def optimized_answer_question(keyword):
    
    '''
        There are mainly three steps in this function:
        1. Answer all the subquestions for the keyword with several answers
        2. Store the results as a page with reference in the certain file
        
        Keyword arguments:
        keyword -- the keyword to generate the subquestions
    '''
    
    # store the reuslt as a page into the file
    with open(RESULT_PATH, "w") as file_object:
        
        for sub_id in range(len(SUB_QUESTIONS)):
            
            retry_num = 0
            success_tag = 0
            candidate_ans_list = []
            
            # construct the question with subquestion and keyword
            tmpquestion = SUB_QUESTIONS[sub_id] + keyword
            
            # create the header into the file for each subquestions
            file_object.write(str(sub_id + 1) + ". " + tmpquestion + "\n\n")
            
            # deal with the url error with certain number of retries
            while(retry_num < 5):
                try:
                    # obtain the websites list of original text as references
                    # also, collect the data with Data Collection module
                    data_collected = collect_data(tmpquestion, WEB_NUM)
                    if data_collected[0] == -1:
                        print("++++++++++ DATA COLLECTION FAIL ++++++++++\n")
                        file_object.close()
                        return
                    reference_list = data_collected[1]
                except urllib.error.URLError or urllib.error.HTTPError:
                    print("The internet is not stable, retrying...")
                    retry_num += 1
                else:
                    retry_num = 5
                    success_tag = 1
            retry_num = 0
            
            if success_tag == 0:
                print("The question cannot be answered because of the poor Internet connection.")
                file_object.close()
                return
            
            # summarize the original text with Text Summarization module for several times
            for i in range(CANDIDTE_NUM):
                candidate_answer = text_summarization(tmpquestion)
                candidate_ans_list.append(candidate_answer)
                
            # select the best answer with result_selection function
            answer = result_selection(candidate_ans_list)
            
            # input the answer into the file
            file_object.write(answer + "\n\n")
            
            # input the reference list into the file
            file_object.write("References:\n")
            for web in reference_list:
                file_object.write(web + "\n")
            file_object.write("\n")
    
    file_object.close()     
        
    return
    
if __name__ == "__main__":
    
    keyword = "federated learning"
    # answer_question(keyword)
    optimized_answer_question("machine learning")
    