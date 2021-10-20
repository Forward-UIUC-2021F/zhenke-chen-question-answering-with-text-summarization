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
FILE_PATH = "xxx"


# define the parameters for OpenAI API
ENGINE = "davinci"
TEMPERATURE = 0.3
MAX_TOKENS = 100
TOP_P = 1.0
FREQ_P = 0.0
PRE_P = 0.0


class TextSummarizer():
    
    def __init__( self ):
        pass


    def convert_file( self, file_path ):

        '''
            Convert the original text file to the one recognized by the openai API, specifically TL;DR mark in the end

            Keyword arguments:
            file_path -- the file path for the original text file
        '''


    def text_summarization( self, original_text ):

        '''
            Summarize the original text with OpenAI API TL;DR summarization

            Keyword arguments:
            original_text -- the original text to be summarized
        '''

        response = openai.Completion.create(

            # define the NLP engine
            # davinci proper for Text Summarization
            engine = ENGINE,

            # define the text to be summarize
            prompt = original_text,

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

        # print(response)
        print(response["choices"][0]["text"])

        return

    
def main():

    '''
        There are mainly two steps to summarize the text 
        1. Convert the original text extracted from Google Search results to the form recognized by the OpenAI API
        2. Abstractively summarize the text with the OpenAI API

        Keyword Arguments:
        file_path -- the file path for the original text file
    '''

    text_summarizing = TextSummarizer()

    text = "A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei. tl;dr"

    text_summarizing.text_summarization(text)




if __name__ == "__main__":
    main()
