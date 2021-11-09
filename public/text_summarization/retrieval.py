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
from pygaggle.rerank.base import hits_to_texts


# apply the proper transformer for the DPR
reranker = MonoT5()


# define the file path which stores the original file
FILE_PATH_1 = "./public/data_collection/original_text.txt"
FILE_PATH_2 = "./public/data_collection/original_text_with_paragraphs.txt"


# define the mark to separate text from different sources while storing in the file
DELIMETER = "######"


# define the number of paragraphs to construct the original text
PARA_NUM = 5


class Retrieval():

    def __init__( self ):
        pass


    def process_text( self, file_path ):

        '''
            Locate the text, which is stored in the specific txt file as a result of Google Search and Data Clawer
            Then, process the text into the form proper for DPR to run

            Keyword Arguments:
            file_path -- the path of file string the text from Google Search and Data Clawer
        '''

        text_list = []
        idx = 0

        # read the original text file and fetch the text as certain format with ID
        with open(file_path, "r") as f:
            data = f.readlines()
            for i in range(len(data)):
                if len(data[i]) > 50:
                    idx += 1
                    text_list.append([str(idx), data[i]])
        
        # print out the text list for testing
        # for i in text_list:
        #     print(i)
        # print(len(text_list))
        
        f.close()

        return text_list


    def select_paragraphs( self, question, passages, paragraph_num ):

        '''
            Apply the DPR to rank the relevance between the question and text
            Then select the certain number of paragraphs as the original text with DPR

            Keyword Arguments:
            question -- the question asked by the user
            passges -- all passages fetched from Google Search with specific format
            paragraph_num -- number of paragraphs of original text for text summarization
        '''

        ranking_result = {}
        original_text = ""

        # define the query
        query = Query(question)

        # define the dense decoder 
        searcher = SimpleSearcher.from_prebuilt_index('msmarco-passage')
        hits = searcher.search(query.text)
        texts = hits_to_texts(hits)

        # extract the text with certain format
        texts = [ Text(p[1], {'docid': p[0]}, 0) for p in passages]

        # print out the ranking before the reranking
        # for i in range(0, len(passages)):
        #     print(f'{i+1:2} {texts[i].metadata["docid"]:15} {texts[i].score:.5f} {texts[i].text}')

        # re-rank
        reranked = reranker.rerank(query, texts)

        # print out and store the re-ranked results
        for i in range(0, len(passages)):
            print(f'{i+1:2} {reranked[i].metadata["docid"]:15} {reranked[i].score:.5f} {reranked[i].text}')
            tmp_score = reranked[i].score
            ranking_result[tmp_score] = reranked[i].text
        print("")

        # sort out the ranking result with scores from high to low
        # then output the ones with the highest socres
        sorted_reranked = sorted(ranking_result, reverse = True)
        # print(sorted_reranked)
        for i in range(paragraph_num):
            original_text += ranking_result[sorted_reranked[i]].strip('\n')
            if i != paragraph_num - 1:
                original_text += " "
        # print(original_text)
        # print(len(original_text))

        return original_text



def main():

    '''
        There are mainly three steps to finish the retrieval
        1. Convert the text store in the file with the format accpetable for DPR
        2. Calculate the socres of relevance bwtween the question and text
        3. Ouput the most relavant paragraphs with certain number
    '''

    retrieval = Retrieval()

    # define the question and possible answers for testing
    test_question = "What is Natural Language Processing?"
    test_passages = [["1", "The Python programing language provides a wide range of tools and libraries for attacking specific NLP tasks. Many of these are found in the Natural Language Toolkit, or NLTK, an open source collection of libraries, programs, and education resources for building NLP programs."], ["2", "Natural language processing (NLP) refers to the branch of computer science—and more specifically, the branch of artificial intelligence or AI—concerned with giving computers the ability to understand text and spoken words in much the same way human beings can."], ["3", "I wish I have a cat."], ["4","IBM has innovated in the artificial intelligence space by pioneering NLP-driven tools and services that enable organizations to automate their complex business processes while gaining essential business insights."]]

    # extract the passage from the stored file and convert to the certain format with ID
    passages = retrieval.process_text(FILE_PATH_1)
    question = "What is data structure?"

    # apply the retrieval to get the top related pieces of text and combine them as the original text
    # retrieval.select_paragraphs(question, test_passages, 3)
    result = retrieval.select_paragraphs(question, passages, PARA_NUM)
    print("+++++++++ Original Text +++++++++")
    print(result)

    return


if __name__ == "__main__":
    main()
