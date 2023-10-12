from orkg import ORKG, Hosts
from flask import *
from collections import Counter


app = Flask(__name__)
connector = ORKG(host=Hosts.PRODUCTION)


@app.route('/api/v1.0/get_property_id', methods=['GET'])
def get_proptery_id():
  try:
    args = request.args
    label = args['label']
    size = args['size']
    response = connector.predicates.get(q = label, exact = False, size = size)
    if response.succeeded and response.content:
      return jsonify([[prop['id'], prop['label']] for prop in response.content]), 200
    else:
      return jsonify('No properties found'), 200
  except Exception as e:
    return jsonify({'exception': str(e)}), 400


@app.route('/api/v1.0/get_resource_id', methods=['GET'])
def get_resource_id():
  try:
    args = request.args
    label = args['label']
    size = args['size']
    response = connector.resources.get(q = label, exact = False, size = size)
    if response.succeeded and response.content:
      return jsonify([[obj['id'], obj['label'], obj['shared']] for obj in response.content]), 200
    else:
      return jsonigy('No resources found'), 200
  except Exception as e:
    return jsonify({'exception': str(e)}), 400


@app.route('/api/v1.0/get_contribution_id', methods=['GET'])
def get_contribution_id():
  try:
    
    args = request.get_json()
    contrs = []
    for prop_id, obj_id in args.items():

      response = connector.predicates.by_id(id = prop_id)
      if not response.succeeded or not response.content:
        return jsonify('Wrong property ID')

      if not connector.resources.exists(obj_id):
        return jsonify('Wrong object ID')

      response = connector.statements.get_by_object_and_predicate(object_id = obj_id,
                                                                  predicate_id = prop_id)
      if response.succeeded:
        for contr in response.content:
          contrs.append(contr['subject']['id'])
    
    return jsonify(Counter(contrs)), 200

  except Exception as e:
    return jsonify({'exception': str(e)}), 400


@app.route('/api/v1.0/get_paper_id', methods=['GET'])
def get_paper_id():
  try:
    args = request.args
    contr_id = args['contribution_id']
    response = connector.statements.get_by_object_and_predicate(object_id = contr_id,
                                                                predicate_id = 'P31',
                                                                size = 1)
    if response.succeeded:
      paper = response.content[0]
      return jsonify(paper['subject']['id']), 200
    else:
      return jsonify('Wrong contribution ID'), 200
  except Exception as e:
    return jsonify({'exception': str(e)}), 400


@app.route('/api/v1.0/get_paper_data', methods=['GET'])
def get_paper_data():
  try:
    args = request.args
    paper_id = args['paper_id']
    response = connector.statements.get_by_subject_and_predicate(subject_id = paper_id,
                                                                 predicate_id = 'P26')
    if response.succeeded and response.content:
      statement = response.content[0]
      doi = statement['object']['label']
      url = 'https://doi.org/' + doi
      title = statement['subject']['label']
      return jsonify([doi, url, title]), 200
    else:
      return jsonify('DOI not found'), 200
  except Exception as e:
    return jsonify({'exception': str(e)}), 400


if __name__ == "__main__":
    app.run()
