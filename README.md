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

## Function 1 getOptimizedGoogleResults
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

## Function 3 preprocess
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

## Function 4 embedSentences
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

## Function 5 trainModel
* ***Functionality***: Train the CNN model based on embedded data from standard reference text
* ***Input***:
   * embeddedData: embedded data with saliency scores
   * dataWithScores: data with sentences and saliency scores for each sentence
* ***Output***: trained model
```python
def trainModel( embeddedData, dataWithScores ):
   xxxxxx
   return trainedModel
```

## Function 6 selectSentences
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
```

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

## Function 7 evaluateWithRouge
* ***Functionality***: Evaluate the text summarization result with Rouge
* ***Input***:
   * referenceText: for some Rouge methods, the evaluation needs the standard reference text
   * summarizedText: summarized text to be evaluated
* ***Output***: evaluation result represented by a dictionary with form {Precision: xxx, Recall: xxx, Fmeasure: xxx}
```python
def evaluateWithRouge( referenceText, summarizedText ):
   xxxxxx
   return evaluationResult
```

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

## Function 8 getAnswer
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
```

# Algorithmic Design


# References
Dataset: 
