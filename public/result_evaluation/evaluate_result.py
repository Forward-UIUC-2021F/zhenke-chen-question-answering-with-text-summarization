'''
    @author Zhenke Chen
    @date 2/11/2021

    Apply Rouge-L to evaluate the Text Summarization result
'''


# import the required packages
import rouge
from rouge import Rouge


# define the parameters for Rouge evaluation
GET_SCORE_AVG = True
ROUGE_SCORE_TYPE = "rouge-l"


class ResultEvaluation():

    def __init__( self ):
        pass


    def get_rouge_scores( self, test_text, reference_text ):

        '''
            Get the Rouge scores based on the comparison
            between the text to be evaluatd and the reference text

            Keyword arguments:
            test_text -- the text to be evaluated
            reference_text -- the reference text
        '''

        # constuct the rouge score system
        rouge = Rouge()
        rouge_score = rouge.get_scores(test_text, reference_text, avg = GET_SCORE_AVG)

        # return the Rouge scores according to the type of scores
        return rouge_score[ROUGE_SCORE_TYPE]
    
    
    def get_retrieval_scores( self, question, test_text ):
        
        '''
            Get the DPR Retrieval socres for relevance based on the comparison
            between the question and summarized text
            
            Keyword arguments:
            question -- the question asked by the user
            test_text -- the summarized text 
        '''
        
        return


def main():

    '''
        With the input of two types of text,
        one of which is the text to be evaluated and another is the reference one,
        the Rouge will calculate the socres to evaluate the result

        Keyword Arguments:
        test_text -- the text to be evaluated
        reference_text -- the reference text
    '''

    result_evaluation = ResultEvaluation()

    # input the test text and reference text
    # for comparison, there are two groups of test text

    test_text_1 = ["Natual language processing is a science to help computer interact with, process and analyze human language. The computer is expected to understand the data from the language."]

    test_text_2 = ["Natural language processing has its roots in the 1950s. Already in 1950, Alan Turing published an article titled Computing Machinery and Intelligence which proposed what is now called the Turing test as a criterion of intelligence, a task that involves the automated interpretation and generation of natural language, but at the time not articulated as a problem separate from artificial intelligence."]

    reference_text = ["Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data. The goal is a computer capable of understanding the contents of documents, including the contextual nuances of the language within them."]

    # output the Rouge result for each group

    print("+++++++++ Rouge Result for Group 1 +++++++++")
    print(result_evaluation.get_rouge_scores(test_text_1, reference_text))

    print("+++++++++ Rouge Result for Group 2 +++++++++")
    print(result_evaluation.get_rouge_scores(test_text_2, reference_text))


if __name__ == "__main__":
    main()
