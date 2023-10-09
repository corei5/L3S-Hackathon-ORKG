import os
import streamlit as st 
from docx import Document
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from orkg import ORKG, Hosts # import base class from package
from semanticscholar import SemanticScholar
sch = SemanticScholar()


huggingfacehub_api_token = " " # Add the huggingfacehub API token
orkg = ORKG(host=Hosts.PRODUCTION) # create the connector to the ORKG

# Customize the layout
st.set_page_config(page_title="ORKGQA", page_icon="🤖", layout="wide", )
st.markdown(f"""
            <style>
            .stApp {{background-image: url("https://blogs.tib.eu/wp/tib/wp-content/uploads/sites/3/2020/01/ORKG_Gesamt_Facebook.jpg .."); 
                     background-attachment: fixed;
                     background-size: cover}}
         </style>
         """, unsafe_allow_html=True)

#Use ORKG

def get_paper_via_doi(doi: str):
  dois = orkg.literals.get_all(q=doi, exact=True).content
  try:
      if len(dois) > 0:
        # Found the id of DOI predicate from here https://orkg.org/resource/R36109?noRedirect
        statements = orkg.statements.get_by_object_and_predicate(predicate_id="P26", object_id=dois[0]["id"]).content
        return statements[0]["subject"]["id"], statements[0]["subject"]["label"]
      else:
        return "Please provide DOI"
  except:
      return "  "

def abstract_summary(doi: str):
    try:
        paper_semanticscholar = sch.get_paper(doi_search)
        return paper_semanticscholar.abstract
    except:
        return "  "


#get_paper_via_doi("10.1101/2020.03.03.20029983")

doi_search = st.text_input("Give your DOI", placeholder="DOI will be")

paper_id = get_paper_via_doi(doi_search)[0]
paper_label = get_paper_via_doi(doi_search)[1]
st.write(paper_id)
st.write(paper_label)


st.write(abstract_summary(doi_search))
# function for writing uploaded file in temp
def write_text_file(content, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error occurred while writing the file: {e}")
        return False

def is_docx_file(file):
    # Check if the file extension is .docx
    if file.name.split(".")[-1].lower() == "docx":
        return True
    else:
        return False

# set prompt template
prompt_template = """
You are an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. Below is some information. 
{context}

Based on the above information only, answer the below question. 

{question}
"""

prompt = PromptTemplate.from_template(prompt_template)

#for summary
# st.title("📄 Scholarly Document summarizer")
# st.text("𓅃 Powered by Falcon-7B")
#
# option = st.selectbox(
#     'Which LLM would you like to use?',
#     ('Falcon-7B', 'Dolly-v2-3B'))
#
#
# model_dict = {'Falcon-7B': "tiiuae/falcon-7b-instruct", 'Dolly-v2-3B': "databricks/dolly-v2-3b"}
#
# repo_id = model_dict[option] if option else "tiiuae/falcon-7b-instruct"
#
# llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token,
#                      repo_id=repo_id,
#                      model_kwargs={"temperature":0.6, "max_new_tokens":250 if option=='Dolly-v2-3B' else 500 }) # "max_new_tokens":500})
# embeddings = HuggingFaceEmbeddings()
# llm_chain = LLMChain(prompt=prompt, llm=llm)
#
# from langchain.chains.summarize import load_summarize_chain
#
#
# chain = load_summarize_chain(
#     llm=llm,
#     chain_type="refine",
#     question_prompt=prompt,
#     refine_prompt="Write 2 line summary for this text",
#     return_intermediate_steps=True,
#     input_key="input_documents",
#     output_key="output_text",
# )
# result = chain({"input_documents": abstract_summary(doi_search)}, return_only_outputs=True)

#stuff_chain.run({"context": abstract_summary(doi_search), "question": "Write 2 line summary for this text"})

#...............

st.title("📄 Scholarly Document Question Answering with ORKG and LLMs")
st.text("𓅃 Powered by Falcon-7B")

option = st.selectbox(
    'Which LLM would you like to use?',
    ('Falcon-7B', 'Dolly-v2-3B'))


model_dict = {'Falcon-7B': "tiiuae/falcon-7b-instruct", 'Dolly-v2-3B': "databricks/dolly-v2-3b"}

repo_id = model_dict[option] if option else "tiiuae/falcon-7b-instruct"

llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token, 
                     repo_id=repo_id, 
                     model_kwargs={"temperature":0.6, "max_new_tokens":250 if option=='Dolly-v2-3B' else 500 }) # "max_new_tokens":500})
embeddings = HuggingFaceEmbeddings()
llm_chain = LLMChain(prompt=prompt, llm=llm)

uploaded_file = st.file_uploader("Upload an article", type=["docx", "txt"])
flag = 0

if uploaded_file is not None:
    if is_docx_file(uploaded_file):
        document = Document(uploaded_file)
        paragraphs = [p.text for p in document.paragraphs]
        
        content = "\n".join(paragraphs)
        file_path = "temp/file.txt"
        write_text_file(content, file_path)   
        # st.write(content)
    else:
        content = uploaded_file.read().decode('utf-8')
        file_path = "temp/file.txt"
        write_text_file(content, file_path)   
    loader = TextLoader(file_path)
    docs = loader.load()    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=256, chunk_overlap=0, separators=[" ", ",", "\n", "."]
    )
    texts = text_splitter.split_documents(docs)
    db = Chroma.from_documents(texts, embeddings)    
    st.success("File Loaded Successfully!!")
    flag = 1



# Query through LLM    
if flag == 1:
    question = st.text_input("Ask something from the file", placeholder="Find something similar to: ....this.... in the text?", disabled=not uploaded_file)    
    if question:
        similar_doc = db.similarity_search(question, k=1)
        context = similar_doc[0].page_content
        query_llm = LLMChain(llm=llm, prompt=prompt)
        response = query_llm.run({"context": context, "question": question})        
        st.write(response)
