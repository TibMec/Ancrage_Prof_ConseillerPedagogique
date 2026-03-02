import requests
from flask import Flask, jsonify, request
import os

API_DAO = os.getenv("API_DAO", "http://127.0.0.1:5600")
app = Flask(__name__)

def get_token():
    token = request.headers.get("Authorization")
    print("TOKEN ds service cp:", token)
    return token

@app.route("/v1/conseillers-affilies", methods=["GET"])
def conseillers_affilies():
    token = get_token()
    if not token:
        return jsonify({"erreur": "Token manquant"}), 401
    url = f'{API_DAO}/v1/tibinc/professeurs-dao/lierConseiller'
    reponse = requests.get(url, headers={"Authorization": token})
    return jsonify(reponse.json()), reponse.status_code

@app.route('/v1/enseignants', methods=['POST'])
def creer_prof( ):
    data = request.get_json()
    url = f'{API_DAO}/v1/tibinc/professeurs-dao'
    reponse = requests.post(url, json=data)
    return jsonify(reponse.json()), reponse.status_code

@app.route('/v1/enseignants/<string:email>', methods=['PUT'])
def mise_a_jour_prof(email ):
    token = get_token()
    if not token:
        return jsonify({"erreur": "Token manquant"}), 401
    data = request.get_json()
    url = f'{API_DAO}/v1/tibinc/professeurs-dao/{email}'
    reponse = requests.put(url, json=data, headers={"Authorization": token})
    return jsonify(reponse.json()), reponse.status_code

@app.route('/v1/enseignants/<string:email>', methods=['DELETE'])
def supprimer_prof(email):
    token = get_token()
    if not token:
        return jsonify({"erreur": "Token manquant"}), 401
    url = f'{API_DAO}/v1/tibinc/professeurs-dao/{email}'
    reponse = requests.delete(url,headers={"Authorization": token})
    return jsonify(reponse.json()), reponse.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5700)