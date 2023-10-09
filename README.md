# L3S-Hackathon-ORKG

## ChatGPT.csv

 - This file must be utilized and submitted when extracting knowledge using ChatGPT. Your kind support will help us to extract scholarly knowledge properly using LLMs in the future.

## Notebook

- The notebook contains the installation process and example codes related to this hackathon.  

## Playground (Demo Prototype: Document Question Answering with ORKG using LLMs)

This project builds a scholarly document question-answering app powered by the Open Research Knowledge Graph (ORKG) and Large Language Models (LLMs) like Falcon-7B and Dolly-v2-3B using LangChain, the ChromaDB vector database.

**Note:** Due to memory issues with Streamlit, the app may not work sometimes and gives an error. This is due to the 1GB memory limit by Streamlit.


![demo](https://github.com/corei5/L3S-Hackathon-ORKG/assets/11629650/54001adf-813a-4b59-9efc-0fd85819b3d6)

### Problem Statement

In today's era of information overload, individuals and organizations are faced with the challenge of efficiently extracting relevant information from vast amounts of scholarly data. Traditional search engines often need to provide precise and context-aware answers to specific questions posed by research. As a result, there is a growing need for advanced natural language processing (NLP) techniques to enable scholarly document question-answering (QA) systems.

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
