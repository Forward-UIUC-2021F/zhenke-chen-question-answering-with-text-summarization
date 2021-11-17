'''
    @author Zhenke Chen
    @date 15/11/2021

    Overall question answering file, together with test cases
'''


# import the required packages
import urllib


# import the necessary functions from other files
from public.data_collection.collect_data import main as collect_data
from public.text_summarization.summarizer import main2 as text_summarization


# define the path to store the result
RESULT_PATH = "./result.txt"


# define the number of websites for each subquestion
WEB_NUM = 6


# define the list of subqeustion
# SUB_QUESTIONS = ["What is ", "History of ", "Methods of "]
SUB_QUESTIONS = ["What is ", "History of ", "Applications of "]
# SUB_QUESTIONS = ["What is "]
# SUB_QUESTIONS = ["History of "]
# SUB_QUESTIONS = ["Methods of "]
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
    
if __name__ == "__main__":
    
    keyword = "federated learning"
    answer_question(keyword)
    