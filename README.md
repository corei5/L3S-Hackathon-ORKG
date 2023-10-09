# L3S-Hackathon-ORKG

## ChatGPT.csv

 - This file must be utilized and submitted when extracting knowledge using ChatGPT. Your kind support will help us to extract scholarly knowledge properly using LLMs in the future.

## Notebook

- The notebook contains the installation process and example codes related to this hackathon.

Example: 

```
def get_paper_via_doi(doi: str):
  dois = connector.literals.get_all(q=doi, exact=True).content
  if len(dois) > 0:
    # Found the id of DOI predicate from here https://orkg.org/resource/R36109?noRedirect
    statements = connector.statements.get_by_object_and_predicate(predicate_id="P26", object_id=dois[0]["id"]).content
    return statements[0]["subject"]
  else:
    return None

get_paper_via_doi("10.1101/2020.03.03.20029983")
```
```
from orkg import ORKG, Hosts
from collections import Counter

filters = []
print('Starting to add filters')
while True:

  # Inputing a property
  prop_label = input('Enter a property label or "ok" if you have enough filters: ')
  if prop_label == 'ok':
    break
  response = orkg.predicates.get(q = prop_label, exact = False, size = 10)
  if response.succeeded and response.content:
    [print(prop) for prop in response.content]
  else:
    print('No properties found, enter a filter again')
    continue
  prop_id = input('Enter ID of a selected property: ')
  response = orkg.predicates.by_id(id = prop_id)
  if not response.succeeded or not response.content:
    print('Wrong ID, enter a filter again')
    continue

  # Inputing a property value
  obj_label = input('Enter a resource label: ')
  response = orkg.resources.get(q = obj_label, exact = False, size = 10)
  if response.succeeded and response.content:
    [print(obj) for obj in response.content]
  else:
    print('No resources found, enter a filter again')
    continue
  obj_id = input('Enter ID of a selected resource: ')
  if not orkg.resources.exists(obj_id):
    print('Wrong ID, enter a filter again')
    continue

  filters.append((prop_id, obj_id))

print('Your filters:')
for filter in filters:
  print(f'property: {filter[0]}, resource: {filter[1]}')

# Quering contributions
contrs = []
for filter in filters:
  prop = filter[0]
  obj = filter[1]
  response = orkg.statements.get_by_object_and_predicate(object_id = obj, predicate_id = prop)
  if response.succeeded:
    for contr in response.content:
      contrs.append(contr['subject']['id'])

print('Found related contributions:')
for contr_id, count in Counter(contrs).items():
  print(f'contribution id: {contr_id}, number of mathes: {count}')

# Quering papers
print('Getting papers by related contributions')
while True:
  contr_id = input('Enter ID of a selected contribution, or "q" to quit: ')
  if contr_id == 'q':
    break
  response = connector.statements.get_by_object_and_predicate(object_id = contr_id, predicate_id = 'P31', size = 10)
  if response.succeeded:
    paper = response.content[0]
    paper_id = paper['subject']['id']
    print(f'ID of a paper with the selected contribution: {paper_id}')
    response = connector.statements.get_by_subject_and_predicate(subject_id = paper_id, predicate_id = 'P26')
    if response.succeeded and response.content:
      doi = response.content[0]['object']['label']
      print(f'DOI of the paper: {doi}')
  else:
    print('Wrong ID, enter ID again')
    continue
```

## Playground (Demo Prototype: Document Question Answering with ORKG using LLMs)

This project builds a scholarly document question-answering app powered by the Open Research Knowledge Graph (ORKG) and Large Language Models (LLMs) like Falcon-7B and Dolly-v2-3B using LangChain, the ChromaDB vector database.

**Note:** Due to memory issues with Streamlit, the app may not work sometimes and gives an error. This is due to the 1GB memory limit by Streamlit.

![demo](https://github.com/corei5/L3S-Hackathon-ORKG/assets/11629650/c10348ba-4d41-4dbc-91f5-5c9c4e5fec28)

This project aims to develop a Scholarly Document Question Answering app powered by Large Language Models (LLMs), such as Falcon-7B and Dolly-v2-3B, utilizing the LangChain platform and the ChromaDB vector database. By leveraging the capabilities of LLMs, this app aims to provide users with accurate and comprehensive answers to their questions within a given document corpus.

### Methodology

- **Extract scholarly document from ORKG (using DOI)**: The app supports scholarly knowledge extraction for a scholarly document (using DOI) using ORKG.
- **Extract scholarly document abstract from external DB**: The app supports abstract extraction for a scholarly document (using DOI).
- **Document Loading**: The app supports uploading of `.txt` files and `.docx` files. Once uploaded, the `.docx` file is converted to a `.txt` file. Using LangChain, the document is loaded using TextLoader.
- **Text Splitting**: Next, we split the text recursively by character. For this, we use the RecursiveCharacterTextSplitter. This text splitter is the recommended one for generic text. A chunk size is specified, as well as a list of separators.
- **Generating Embeddings**: The HuggingFaceEmbeddings() class in LangChain uses the sentence_transformers embedding models, more specifically the mpnet-base-v2 model.
- **Vector Database**: A vector store using ChromaDB stores embedded data and performs vector search operations.
- **Context Search**: Depending on the researcher's question, a similarity search is carried out on the vector database to get the most appropriate context to answer the question.
- **Prompt Engineering**: The above context, appropriate prompt, and the research question are created.
- **Inference using LLMs**: Depending on the researcher choice, we either use Falcon-7B or Dolly-v2-3B for our inference. We pass the engineered prompt to the model and display the model's response.

### Reference

- [1] Open Research Knowledge Graph (ORKG) - https://orkg.org/ 
- [2] This prototype was utilized and modified from this repository  - https://github.com/kedarghule/Document-Question-Answering 

## Contribution
 - Gollam Rabby
 - Yaser Jaradeh
 - Allard Oelen
 - Ildar Baimuratov
 - Tim Wittenborg
