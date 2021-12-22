# zhenke-chen-question-answering-with-text-summarization
This project is to answer questions related to keywords using google with text summarization.

# Setup

## Dependencies
```
pip install -r requirements.txt
```

## File Structure
```
zhenke-chen-question-answering-with-text-summarization/
    - requirements.txt
    - README.md
    - data/images/
        -- Module_1.png
    - src/
        -- data_collection/
            --- collect_data.py
            --- original_text.txt
        -- result_evaluation/
            --- evaluate_result.py
        -- text_summarization/
            --- retrieval.py
            --- summarizer.py
            --- original_text.py
        -- question_answering.py
     - tests/
        -- results.txt
```

## File Descriptions

* ```data/images/Module_1.png```: store the image for readme file
* ```src/data_collection/```: Data Collection module
* ```src/result_evaluation/```: Result Evaluation module
* ```src/text_summarization/```: Text Summarization module
* ```src/question_answering.py```: answer questions based on the keyword

# Functional Design

## Module 1: Data Collection

### Function 1 get_google_results
* ***Functionality***: Get searching results from Google Search with question
* ***Input***:
   * keywords: the keywords for the question
   * res_num: the number of results as original text for summarization
   <br>e.g. if the conditions are pre-defined with specific id for each one, such as only with “.edu“ websites, then the source of original text will only be ".edu" websites
* ***Output***:
   * raw_text: the text stored in a list of length res_num, with each element from one piece of Google Search result
```python
def get_google_results( keywords, res_num ):
   xxxxxx
   return raw_text
```

## Module 2: Text Summarization
### Function 2 retrieval
* ***Functionality***: Apply the Dense Passage Retrieval (DPR) to evaluate and rank the relevance between the question and text, then select the most relevant ones as the original text
* ***Input***:
   * question: the question asked by the user
   * raw_text: the raw text fetched from the Data Collection module 
   * paragraph_num: the number of paragraphs user wants to apply for the original text
* ***Output***:
   * original_text: the text most relevant to the question, which is ranked by DPR
```python
def retrieval( question, raw_text, paragraph_num ):
   xxxxxx
   return original_text
```

### Function 3 summarizer
* ***Functionality***: Apply the OpenAI GPT-3 Abstractive Text Summarization model to summarize the original text
* ***Input***:
   * original_text: the original text to be summarized
* ***Output***:
   * summarized_text: the summarized text, which is also the answer to the question asked by the user
```python
def summarizer( original_text ):
   xxxxxx
   return summarized_text
```

## Module 3: Result Evaluation
### Function 4 rouge_evaluation
* ***Functionality***: Apply the Rouge scores to evaluate the summarized text compared with the reference text
* ***Input***:
   * summarized_text: the text from the result of Text Summarization module
   * reference_text: the reference text to test if the summarization is good enough
* ***Output***:
   * rouge_scores: the Rouge-L scores, with Pricision (higher the better), Recall (higher the better) and F-Measure (higher the better)
```python
def rouge_evaluation( summarized_text, reference_text ):
   xxxxxx
   return rouge_scores
```

### Function 5 DPR_evaluation
* ***Functionality***: Apply the DPR scores to evaluate the relevance between the question and summarized text
* ***Input***:
   * summarized_text: the text from the result of Text Summarization module
   * question: the question asked by the user
* ***Output***:
   * DPR_scores: the DPR retrieval scores, when it is closer to 0, the relevance between the question and summarizer is larger
```python
def DPR_evaluation( summarized_text, question ):
   xxxxxx
   return DPR_scores
```

# Demo Video
## Link: https://drive.google.com/file/d/1Q6xhHJjivIeuBHzjfAgNNmuIqSTg0_vW/view?usp=sharing

# Algorithmic Design

There are three parts of algorithmic designs for this project, which are corresponding the three parts from the functional design, which are **Data Collection**, **Text Summarization** as well as **Results Selection and Evaluation**.

## Module 1: Data Collection
* For data collection, since the data are collected from the Google Search, the websites of raw text result corresponding to the questions will be listed by the google search **APIs**
* Then, with the **BeautifulSoup** web clawer, the raw text will be extracted from the raw website data based on the subtitles and compose the raw text.
* However, because of the design of googlesearch API, some of the subpages in the Google Search result page will also be caught into the websites list, which have the less relevant content with the question. To solve this problem, I will checkout the websites, if they have the same prefix, then the second one will not be accepted.<br>


  ![Routine for Module 1](https://github.com/Forward-UIUC-2021F/Question-answering-with-extracted-text-summarization/blob/milestone_1/Images_for_md/Module_1.png)

   
## Module 2: Text Summarization
* In this module, it mainly completes the task of Text Summarization. There are two steps. The first one is to choose the most relevant paragraphs from the raw text fetch from the websites compared with the question to compose the original text for Text Summarization. And the second step is to apply models to summarize the original text.
* For the first step, it uses the **Dense Passage Retrieval (DPR)** to evaluate the relevance between the question and paragraphs from the Data Collection model. Then, the DPR will rank the paragraphs based on the relevance, and the most relevant ones will compose the original text.
* For the second step, it mainly uses the **OpenAI tl;dr** Text Summarization model (with Davinci Model) to summarize the text. Before the summarization, the original text will be preprocessed to the format accepted by the model. Then, the summarizer will summarize the original text.
* To optimize the result, it will run several times for the summarizer and select the bese result as the answer to the question.

## Module 3: Results Evaluation
* The result evaluation includes the comparision between summarized text and reference text, as well as the comparision between question and answer. 
* For performance evaluation after the Text Summarization, the **ROUGE-L** method with measurement of Precision, Recall and F-Measure value will be applied. With larger the value, the performance is better.
* Then, the DPR scores evaluation will be applied to evaluate the relevance between the question and answer (which is also the summarized text). With the scores closest to 0, the answer is most relevant to the question.

# Issues and Future Work
* The project needs to run for relatively long time for question answering
* The OpenAI API sometimes has poor results in some cases
* Sometimes the project does not have stable results

# References
## Papers:
* Summarizing Papers With Python and GPT-3. Link: https://medium.com/geekculture/a-paper-summarizer-with-python-and-gpt-3-2c718bc3bc88
* Dense Passage Retrieval for Open-Domain Question Answering. Link: https://arxiv.org/abs/2004.04906
* ROUGE - A Package for Automatic Evaluation of Summaries. Link: https://www.aclweb.org/anthology/W04-1013.pdf
## APIs:
* googlesearch API. Link: https://python-googlesearch.readthedocs.io/en/latest/ 
* OpenAI API. Link: https://beta.openai.com/docs/introduction

