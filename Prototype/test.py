import requests
import json


base = 'http://127.0.0.1:5000/api/v1.0/'


if __name__ == '__main__':

    url = 'get_property_id'
    params = {'label': 'research problem',
              'size': '10'}
    response = requests.get(base+url, params = params)
    print(response.text)

    url = 'get_resource_id'
    params = {'label': 'article classification task',
              'size': '10'}
    response = requests.get(base+url, params = params)
    print(response.text)

    url = 'get_property_id'
    params = {'label': 'dataset',
              'size': '10'}
    response = requests.get(base+url, params = params)
    print(response.text)

    url = 'get_resource_id'
    params = {'label': 'DemL dataset',
              'size': '10'}
    response = requests.get(base+url, params = params)
    print(response.text)

    url = 'get_contribution_id'
    params = {'P32': 'R162375',
              'P2005': 'R644349'}
    response = requests.get(base+url, json = params)
    print(response.text)

    url = 'get_paper_id'
    params = {'contribution_id': 'R644335'}
    response = requests.get(base+url, params = params)
    print(response.text)

    url = 'get_paper_data'
    params = {'paper_id': 'R644333'}
    response = requests.get(base+url, params = params)
    print(response.text)
