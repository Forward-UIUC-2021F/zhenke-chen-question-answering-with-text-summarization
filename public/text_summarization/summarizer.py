'''
    @author Zhenke Chen
    @date 19/10/2021

    Apply GPT-3 to summarize the text abstractively
'''


# import the required packages
import numpy as np
import os
import openai
import sys
import os


# import the retrieval from another file
# from retrieval import Retrieval
from public.text_summarization.retrieval import Retrieval


# OpenAI API parameters setting
########### this key should be changed to your own OpenAI API key ###########
openai.api_key = ""


# define the file path which stores the original file
FILE_PATH = "./public/data_collection/original_text.txt"


# define the mark for the OpenAI API to recognize
MARK = "tl;dr:"


# define the parameters for OpenAI API
ENGINE = "davinci"
TEMPERATURE = 0.3
MAX_TOKENS = 300
TOP_P = 1.0
FREQ_P = 0.0
PRE_P = 0.0


# define the mark to separate text from different sources while storing in the file
DELIMETER = "######"


# define the number of paragraphs to construct the original text
PARA_NUM = 5


class TextSummarizer():
    
    def __init__( self ):
        pass


    def convert_file( self, file_path ):

        '''
            Convert the original text file to the one recognized by the openai API, specifically TL;DR mark in the end

            Keyword arguments:
            file_path -- the file path for the original text file
        '''

        original_text = []
        tmp_text = ""
        space_mark = 0

        # read the original text file and fetch the text
        with open(file_path, "r") as f:
            data = f.readlines()
            for i in range(len(data)):
                line = data[i].strip("\n")
                if line == DELIMETER:
                    original_text.append(tmp_text)
                    tmp_text = ""
                    space_mark = 0
                elif line != DELIMETER:
                    if i != len(data) - 1 and space_mark == 1:
                        tmp_text += " " + line
                    elif i != len(data) - 1 and space_mark == 0:
                        tmp_text += line
                        space_mark = 1
                    else:
                        original_text.append(tmp_text)
        f.close()

        # print(len(original_text))
        # print(original_text)

        # add the "tl;dr" to the end of text from every source
        for i in range(len(original_text)):
            original_text[i] += "\n" + MARK

        # print(original_text)

        return original_text
                    

    def text_summarization( self, original_text ):
    
        '''
            Summarize the original text with OpenAI API TL;DR summarization
            Keyword arguments:
            original_text -- the original text to be summarized
        '''

        get_result = 0
        cut = 1
        length = len(original_text)
        # print(length)
        tmp_text = original_text

        while(get_result == 0):
            try:
                response = openai.Completion.create(

                    # define the NLP engine
                    # davinci proper for Text Summarization
                    engine = ENGINE,

                    # define the text to be summarize
                    prompt = tmp_text,

                    # define the randomness for completion
                    # lower for less random
                    temperature = TEMPERATURE,

                    # define the maximum output tokens
                    # approximately four characters for one token
                    max_tokens = MAX_TOKENS,

                    # define diversity via nucleus sampling
                    top_p = TOP_P,

                    # define how much to penalize the new tokens based on their existing frequency
                    # increase the value will decrease the likelihood to repeat the same line verbatim
                    frequency_penalty = FREQ_P,

                    # define how much to penalize the new tokens based on whether they appear in the text so far
                    # increase the value will increase the likelihood to discuss about new topics
                    presence_penalty = PRE_P
                )
            
            # deal with the case when the original text is too long
            except openai.error.InvalidRequestError:
                tmp_text = tmp_text[:int((10-cut)/10*length)]
                tmp_text += "\n" + MARK
                # print(tmp_text)
                cut += 1

            else:
                print(tmp_text)
                get_result = 1

        # print(response)
        # print(response["choices"][0]["text"])

        summarized_text = response["choices"][0]["text"]

        return summarized_text


    # def text_summarization( self, original_text ):

    #     '''
    #         Summarize the original text with OpenAI API TL;DR summarization

    #         Keyword arguments:
    #         original_text -- the original text to be summarized
    #     '''

    #     get_result = 0
    #     cut = 1
    #     length = len(original_text)
    #     # print(length)
    #     tmp_text = original_text

    #     while(get_result == 0):
    #         try:
    #             response = openai.Completion.create(

    #                 # define the NLP engine
    #                 # davinci proper for Text Summarization
    #                 engine = ENGINE,

    #                 # define the text to be summarize
    #                 prompt = tmp_text,

    #                 # define the randomness for completion
    #                 # lower for less random
    #                 temperature = TEMPERATURE,

    #                 # define the maximum output tokens
    #                 # approximately four characters for one token
    #                 max_tokens = MAX_TOKENS,

    #                 # define diversity via nucleus sampling
    #                 top_p = TOP_P,

    #                 # define how much to penalize the new tokens based on their existing frequency
    #                 # increase the value will decrease the likelihood to repeat the same line verbatim
    #                 frequency_penalty = FREQ_P,

    #                 # define how much to penalize the new tokens based on whether they appear in the text so far
    #                 # increase the value will increase the likelihood to discuss about new topics
    #                 presence_penalty = PRE_P
    #             )
            
    #         # deal with the case when the original text is too long
    #         except openai.error.InvalidRequestError:
    #             if cut < 10:
    #                 tmp_text = tmp_text[:int((10-cut)/10*length)]
    #             else:
    #                 tmp_text = tmp_text[:int((19-cut)/100*length)]
                
    #             # make sure the last piece of the result is a complete sentence
    #             print(len(tmp_text))
    #             if tmp_text[len(tmp_text) - 1] != ".":
    #                 tmp_text = tmp_text.split(".")[:len(tmp_text.split(".")) - 1]
    #             tmp_answer = ""
    #             for i in range(len(tmp_text)):
    #                 if i == len(tmp_text) - 1:
    #                     tmp_answer += tmp_text[i] + ". "
    #                 else:
    #                     tmp_answer += tmp_text[i]
    #             tmp_answer += "."
    #             tmp_answer += "\n" + MARK
    #             tmp_text = tmp_answer
    #             # print(tmp_text)
    #             cut += 1

    #         else:
    #             print(tmp_text)
    #             get_result = 1

    #     # print(response)
    #     # print(response["choices"][0]["text"])

    #     summarized_text = response["choices"][0]["text"]

    #     return summarized_text

    
def main1():

    '''
        There are mainly two steps to summarize the text
        1. Convert the original text extracted from Google Search results to the form recognized by the OpenAI API
        2. Abstractively summarize the text with the OpenAI API

        Keyword Arguments:
        file_path -- the file path for the original text file
    '''

    text_summarizing = TextSummarizer()

    # get the converted text usable for Text Summarizer
    original_text = text_summarizing.convert_file(FILE_PATH)

    # apply the first piece of text for testing
    text = original_text[0]
    # print(text)
    
    # summarize the text with OpenAPI
    answer = text_summarizing.text_summarization(text)
    print("++++++++++ SUMMARIZED ANSWER ++++++++++")
    print(answer)

    return


def main2(question):

    '''
        There are mainly three steps to summarize the text
        1. Apply the DPR retrieval to evaluate the relevance between the question and text from Google Search
        2. Select the ones most relevant as the input for OpenAI API to do the Text Summarization
        3. Abstractively summarize the text with the OpenAI API
    '''

    text_summarizing = TextSummarizer()
    text_retrieval = Retrieval()
    
    # define the question and passge before retrieval
    # question = "What is data structure?"
    passage = text_retrieval.process_text(FILE_PATH)
    
    # apply the DPR Retrieval to get the orginal text
    original_text = text_retrieval.select_paragraphs(question, passage, PARA_NUM)
    # original_text += "\n" + MARK
    # print("++++++++++ ORIGINAL TEXT ++++++++++")
    # print(original_text)
    # print("")
    
    # summarize the text and get the result
    answer = text_summarizing.text_summarization(original_text)
    
    # make sure the last piece of the result is a complete sentence
    
    # if answer[len(answer) - 1] != ".":
    #     answer = answer.split(".")[:len(answer.split(".")) - 1]
    # tmp_answer = ""
    # for i in range(len(answer)):
    #     if i != len(answer) - 1:
    #         tmp_answer += answer[i] + ". "
    #     else:
    #         tmp_answer += answer[i]
    # tmp_answer += "."
    
    answer = str(answer)
    # print(len(answer))
    for i in range(len(answer)):
        # print(answer[len(answer)-i-1])
        if answer[len(answer)-i-1] == ".":
            answer = answer[:len(answer)-i]
            break
    # print(answer)
    tmp_answer = answer
        
    print("++++++++++ SUMMARIZED ANSWER ++++++++++")
    print(tmp_answer)

    return tmp_answer



if __name__ == "__main__":
    # main1()
    question = "What is machine learning"
    main2(question)