import requests
from flask import Flask, jsonify, request
import os

API_DAO = os.getenv("API_DAO", "http://127.0.0.1:5600")
app = Flask(__name__)

def get_token():
    token = request.headers.get("Authorization")
    print("TOKEN ds service cp:", token)
    return token

@app.route('/v1/enseignants')
def tous_enseignants():
    token = get_token()
    if not token:
        return jsonify({"erreur": "Token manquant"}), 401
    url = f'{API_DAO}/v1/tibinc/professeurs-dao'
    reponse = requests.get(url,headers={"Authorization": token})
    print("STATUS:", reponse.status_code)
    print("TEXT:", reponse.text)
    return jsonify(reponse.json()), reponse.status_code

@app.route('/v1/conseillers', methods=['POST'])
def creer_conseiller( ):
    token = get_token()
    if not token:
        return jsonify({"erreur": "Token manquant"}), 401
    data = request.get_json()
    url = f'{API_DAO}/v1/tibinc/conseillers-dao'
    reponse = requests.post(url, json=data,headers={"Authorization": token})
    return jsonify(reponse.json()), reponse.status_code

@app.route('/v1/conseillers/<string:email>', methods=['PUT'])
def mise_a_jour_conseiller(email):
    token = get_token()
    if not token:
        return jsonify({"erreur": "Token manquant"}), 401
    data = request.get_json()
    url = f'{API_DAO}/v1/tibinc/conseillers-dao/{email}'
    reponse = requests.put(url, json=data,headers={"Authorization": token})
    return jsonify(reponse.json()), reponse.status_code

@app.route('/v1/conseillers/<string:email>', methods=['DELETE'])
def supprimer_conseiller(email):
    token = get_token()
    if not token:
        return jsonify({"erreur": "Token manquant"}), 401
    url = f'{API_DAO}/v1/tibinc/conseillers-dao/{email}'
    reponse = requests.delete(url,headers={"Authorization": token})
    return jsonify(reponse.json()), reponse.status_code


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5900)