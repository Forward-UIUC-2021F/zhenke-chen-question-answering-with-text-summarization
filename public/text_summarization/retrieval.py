'''
    @author Zhenke Chen
    @date 2/11/2021

    There are mainly two steps in Retrieval before the Text Summarization:
    1. Apply the Dense Passage Retrieval (DPR) to evaluate the relevance between the question and text from Google Search
    2. Select the most relevant text as the original text for Text Summarization
'''


# import the required packages
import pygaggle
from pygaggle.rerank.base import Query, Text
from pygaggle.rerank.transformer import MonoT5
from pygaggle.rerank.transformer import MonoBERT
from pyserini.search import SimpleSearcher


# apply the proper transformer for the DPR
reranker = MonoT5()


class Retrieval():

    def __init__( self ):
        pass

    def select_paragraphs( self ):
        