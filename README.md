# Question-answering-with-extracted-text-summarization
This project is to answer questions related to keywords using google with extracted text summarization.

# Functional Design

<!-- ## Funtion 1 inputQuestionTemplate
* ***Functionality***: Implement the question template
* ***Input***:
    * templateId: the id of the template
    * template: template represented by a list
    <br>e.g. "What is xxx" is represented by ["What is ", 0]
    <br>e.g. "xxx's history" is represented by [0, "'s history"]
* ***Output***: 0 for success and -1 for failed
```python
def inputQuestionTemplate( templateId, template ):
   xxxxxx
   return 0
``` -->

<!-- ## Function 2 getGoogleResults
* ***Functionality***: Get searching results from Google Search with question
* ***Input***:
   * question: the question to be searched on Google
   * resNum: the number of results as original text for summarization
   * conditionId: potential condition for Google Search result filter
   <br>e.g. if the conditions are pre-defined with specific id for each one, such as only with “.edu“ websites, then the source of original text will only be ".edu" websites
* ***Output***: Original text stored in a list of length resNum, with each element from one piece of Google Search result
```python
def getGoogleResults( question, resNum, conditionId ):
   xxxxxx
   return originalText
``` -->

## Module 1: Data Collection
### Function 1 getGoogleResults
* ***Functionality***: Get searching results from Google Search with question
* ***Input***:
   * keywords: the keywords for the question
   * resNum: the number of results as original text for summarization
   <br>e.g. if the conditions are pre-defined with specific id for each one, such as only with “.edu“ websites, then the source of original text will only be ".edu" websites
* ***Output***: Original text stored in a list of length resNum, with each element from one piece of Google Search result
```python
def getGoogleResults( keywords, resNum ):
   xxxxxx
   return originalText
```

<!-- ### Function 2 optimizeResultsWithConcept
* ***Functionality***: Select the best results from Google based on the key concept
* * ***Input***:
   * keywords: the keywords for key concepts for the question
   * resNum: the number of optimized results
   * originalText: the original text to be optimized, stored as a list
* ***Output***: Optimized text stored in a list of length resNum
```python
def optimizeResultsWithConcept( keywords, resNum, originalText ):
   xxxxxx
   return optimizedText
``` -->

## Module 2: Model Training (if necessary for the user)
### Function 2 trainModel
* ***Functionality***: Train the model if it is necessary for the user
* ***Input***:
   * referenceText: standard reference text is needed for calculation of saliency scores
   * data: data with sentences from original text
   * word2vecWordNum: number of words used in word embedding with word2vec
   * wordNum: maximum number of words to keep (with relatively large frequency)
* ***Output***: trained model
```python
def trainModel( referenceText, data, word2vecWordNum, wordNum ):
   xxxxxx
   return trainedModel
```

<!-- ### Function 3 preprocess
* ***Functionality***: Preprocess the sentences from original text by Rouge method compared with reference data to get each sentence's saliency scores
* ***Input***:
   * rougeMethodId: id selection of Rouge method
   * referenceText: standard reference text is needed for calculation of saliency scores
   * data: data with sentences from original text
* ***Output***: data with sentences and saliency scores for each sentence
```python
def preprocess( rougeMethodId, referenceText, data ):
   xxxxxx
   return dataWithScores
```

### Function 4 embedSentences
* ***Functionality***: Embed the sentences with word2vec
* ***Input***:
   * data: data with sentences and their corresponding saliency scores
   * word2vecWordNum: number of words used in word embedding with word2vec
   * wordNum: maximum number of words to keep (with relatively large frequency)
* ***Output***: embedded data with saliency scores
```python
def embedSentences( data, word2vecWordNum, wordNum ):
   xxxxxx
   return embeddedData
```
### Function 5 trainModel
* ***Functionality***: Train the CNN model based on embedded data from standard reference text
* ***Input***:
   * embeddedData: embedded data with saliency scores
   * dataWithScores: data with sentences and saliency scores for each sentence
* ***Output***: trained model
```python
def trainModel( embeddedData, dataWithScores ):
   xxxxxx
   return trainedModel
``` -->

## Module 3: Results Selection and Evaluation
### Function 3 getResult
* ***Functionality***: Get the saliency scores from the trained model and select the sentences with highest scores
   * data: raw data to summarize
   * model: trained model
   * sentenceNum: number of sentences from the summarization
   * threshold: limit the similarity if the sentences with all the sentences already in the summary
* ***Output***: summarized text
```python
def getResult ( data, model, sentenceNum, threshold ):
   xxxxxx
   return summarizedText
```

<!-- ### Function 6 getModelOutput
* ***Functionality***: Get the saliency scores output by the trained model
* ***Input***:
   * data: raw data to summarize
   * model: trained model
* ***Output***: Data with sentences with saliency scores
```python
def getModelOutput ( data, model ):
   xxxxxx
   return rawResults
```

### Function 7 selectSentences
* ***Functionality***: Select sentence from sentences with highest saliency scores calculated by the trained model
* ***Input***:
   * data: data from the output of trained model, with saliency scores
   * sentenceNum: number of sentences from the summarization
   * threshold: limit the similarity if the sentences with all the sentences already in the summary
* ***Output***: summarized text
```python
def selectSentences ( data, sentenceNum, threshold ):
   xxxxxx
   return summarizedText
``` -->

<!-- ## Function 7 evaluateWithRouge
* ***Functionality***: Evaluate the text summarization result with Rouge
* ***Input***:
   * rougeMethodId: since there are many different Rouge evaluation methods, such Rouge-1, Rouge-2 and Rouge-L, this is for selection of Rouge method
   * referenceText: for some Rouge methods, the evaluation needs the standard reference text
   * summarizedText: summarized text to be evaluated
* ***Output***: evaluation result represented by a dictionary with form {Precision: xxx, Recall: xxx, Fmeasure: xxx}
```python
def evaluateWithRouge( rougeMethodId, referenceText, summarizedText ):
   xxxxxx
   return evaluationResult
``` -->

<!-- ### Function 8 evaluateWithRouge
* ***Functionality***: Evaluate the text summarization result with Rouge
* ***Input***:
   * referenceText: for some Rouge methods, the evaluation needs the standard reference text
   * summarizedText: summarized text to be evaluated
* ***Output***: evaluation result represented by a dictionary with form {Precision: xxx, Recall: xxx, Fmeasure: xxx}
```python
def evaluateWithRouge( referenceText, summarizedText ):
   xxxxxx
   return evaluationResult
``` -->

<!-- ## Function 8 getAnswer
* ***Functionality***: Overall text summarization function, for convenience of implementation
* ***Input***:
   * templateId: the id of the template
   * conditionId: potential condition for Google Search result filter
   * searchResNum: the number of google search results as original text for summarization
   * keyword: keyword of the question
   * sentenceNum: the sentence number of summarized text
* ***Output***: summarized text
```python
def getAnswer( templateId, conditionId, searchResNum, keyword, sentenceNum ):
   xxxxxx
   return summarizedText
``` -->

<!-- ## Function 7 getAnswer
* ***Functionality***: Overall text summarization function, for convenience of implementation
* ***Input***:
   * searchResNum: the number of google search results as original text for summarization
   * keywords: keywords of the question
   * sentenceNum: the sentence number of summarized text
* ***Output***: summarized text
```python
def getAnswer( searchResNum, keywords, sentenceNum ):
   xxxxxx
   return summarizedText
``` -->

# Algorithmic Design

There are three parts of algorithmic designs for this project, which are corresponding the three parts from the functional design, which are **Data Collection**, **Model Training** as well as **Results Selection and Evaluation**.

## Module 1: Data Collection
* For data collection, since the data are collected from the Google Search, the websites of raw text result corresponding to the questions will be listed by the **APIs** offered by Google.
* Then, with the **BeautifulSoup** web clawer, the raw text will be extracted from the raw website data and compose the original text for the text summarization.<br>
<!-- * Then, since some of the searching results may not be relevant enough with the keywords presented by the user, there will be a filter algorithm to opimize the searching results. In details, the ones most related to the concept will be chosed to form the text to be summarized. For this part, I will temporarily apply the algorithms from Zicheng to pursue the best performance.<br> -->


  ![Routine for Module 1](https://github.com/Forward-UIUC-2021F/Question-answering-with-extracted-text-summarization/blob/main/Images%20for%20md/Module_1.png)

## Module 2: Model Training
* For data training, in order to provide comparison for supervised learning, the train data will be preprocessed. The widely-accepted automatic summarization evaluation metric, ROUGE, is applied to get the salience score for each sentence. Those scores will be used in a further training process.
* To promote the performance of training, the raw training data, also known as sentences, are not used as inputs directly. Instead, the word embedding technique, **word2vec** will be applied to make better use of the semantic and grammatical association of words. So, the human feature enginnering is not needed.
* For the training, the Convolutional Neural Networds (**CNN**) is applied with Convolution (Sigmoid as Activation Function), Max-pooling and Regularization. And the goal is to minimized the cross-entropy (CE) compared with the salience scores from train data.<br>

   ![CNN Training Model](https://github.com/Forward-UIUC-2021F/Question-answering-with-extracted-text-summarization/blob/main/Images%20for%20md/Module_2.png)

## Module 3: Results Selection and Evaluation
* To get all the salience scores for the input test results, also known as the text from Google Search, the text needs to be input into the trained model, and the results are salience scores for each sentence.
* In order to select the most appropriate sentences to form a summary, the salience socres of sentences are compared, and the highest ones will be chosen. In order not collect too many sentences with similar meanings, there is a threahold measuring the similarity of the collected sentences, and if the similarity reaches the threshold, no more similar sentences will be chosen. The routine will start from the beginning until required number of sentences are collected.
* For performance evaluation after the sentence selection, the **ROUGE-L** method with measurement of **F-Measure** value will be applied. This evaluation perspective considers both the Precision and Recall values. With larger the value, the performance is better.

# References
## Datasets:
* Google's Word2vec. Link: https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz.
* DUC Dataset. Link: https://duc.nist.gov/data.html.
## Papers:
* Extractive Document Summarization Based on Convolutional Neural Networks. Link: https://ieeexplore.ieee.org/document/7793761.
* Extractive Document Summarization Using Convolutional Neural Networks - Reimplementation. Link: https://leolaugier.github.io/doc/summarization.pdf.
