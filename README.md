# L3S-Hackathon-ORKG

Welcome to the L3S-Hackathon-ORKG repository! This repository is dedicated to our collaborative efforts during the L3S Hackathon (for ORKG), where we will explore and leverage the Open Research Knowledge Graph (ORKG) to address pressing challenges in scholarly knowledge extraction and natural language processing.

In this repository, you'll find various resources, links, and code snippets to help you get started. The repo is structured as follows : 

## ChatGPT.csv

 - This file must be utilized and submitted when extracting knowledge using ChatGPT. Your kind support will help us to extract scholarly knowledge properly using LLMs in the future.

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

## Notebook

- Notebooks contain the installation process and example codes related to this hackathon.

## Demo code

```
from orkg import ORKG, Hosts # import base class from package
connector = ORKG(host=Hosts.SANDBOX) # create the connector to the ORKG

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
from orkg import ORKG, Hosts # import base class from package
connector = ORKG(host=Hosts.SANDBOX) # create the connector to the ORKG

def get_contributions_of_paper(paper_id: str):
  if connector.resources.exists(paper_id):
    # P31 is the predicate that connects papers to contributions
    # It can be found when exploring any paper resource in the ORKG
    statements = connector.statements.get_by_subject_and_predicate(subject_id=paper_id, predicate_id="P31").content
    return [st["object"] for st in statements]
  else:
    raise ValueError("Paper doesn't exist in the system!")

get_contributions_of_paper("R36109")

```

For more detail (example code): https://github.com/corei5/L3S-Hackathon-ORKG/blob/main/Notebook/L3S_Retreat_ORKG_app_example.ipynb 


### Reference

- [1] Open Research Knowledge Graph (ORKG) - https://orkg.org/ 
- [2] This prototype was utilized and modified from this repository  - https://github.com/kedarghule/Document-Question-Answering 

## Contributors
 - Gollam Rabby
 - Yaser Jaradeh
 - Ildar Baimuratov
 - Allard Oelen
 - Tim Wittenborg
 - Sagnik Basu
 - Enrique Iglesias
