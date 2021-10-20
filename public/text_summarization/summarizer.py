'''
    @author Zhenke Chen
    @date 19/10/2021

    Apply GPT-3 to summarize the text abstractively
'''


# import the required packages
import numpy as np
import os
import openai


# OpenAI API parameters setting
openai.api_key = "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"


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
                get_result = 1

        # print(response)
        # print(response["choices"][0]["text"])

        summarized_text = response["choices"][0]["text"]

        return summarized_text

    
def main():

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



if __name__ == "__main__":
    main()
