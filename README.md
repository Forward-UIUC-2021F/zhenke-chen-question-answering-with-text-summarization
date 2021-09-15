# Question-answering-with-extracted-text-summarization
This project is to answer questions related to keywords using google with extracted text summarization.

# Functional Design
## Funtion 1 inputQuestionTemplate
* ***Functionality***: Implement the question template
* ***Input***:
    * templateId: the id of the template
    * template: template represented by a list
    <br>e.g. "What is xxx" is represented by ["What is ", 0]
    <br>e.g. "xxx's history" is represented by [0, "'s history"]
* ***Output***: 0 for success and -1 for failed
```python
def inputQuestionTemplate( templateId, template):
    xxxxx
    return 0
```
