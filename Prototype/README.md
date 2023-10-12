# Prototype with LLMs and ORKG

Welcome to the L3S-Hackathon-ORKG repository! This repository is dedicated to our collaborative efforts during the L3S Hackathon (for ORKG), where we will explore and leverage the Open Research Knowledge Graph (ORKG) to address pressing challenges in scholarly knowledge extraction and natural language processing.

In this repository, you'll find various resources, links, and code snippets to help you get started. The repo is structured as follows : 

### Prototype 

 - Need to Login in the ORKG
 - Need Huggingface access tokens for LLMs
 - Install requirement.txt
 - If you get root_validator error please use this: pip install pydantic==1.10.9 (https://stackoverflow.com/questions/76934579/pydanticusererror-if-you-use-root-validator-with-pre-false-the-default-you)

#### How to run this 

streamlit run app.py


### API 

- for requirements see _requirements.txt_
- run _l3s_retreat_orkg_app_example_api.py_

Methods:
- get_proptery_id(label, size)
- get_resource_id(label, size)
- get_contribution_id([[property_id, resource_id], ...])
- get_paper_id(contribution_id)
- get_paper_data(paper_id)

### Reference

- [1] Open Research Knowledge Graph (ORKG) - https://orkg.org/ 
- [2] This prototype was utilized and modified from this repository  - https://github.com/kedarghule/Document-Question-Answering 

## Contributors
 - Gollam Rabby
 - Yaser Jaradeh
 - Ildar Baimuratov
 - Allard Oelen
 - Tim Wittenborg
