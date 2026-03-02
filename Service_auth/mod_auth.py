from datetime import timedelta

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from flask_jwt_extended import create_access_token
from mod_modele_pydantic import Prof, CP

app = Flask(__name__)

# Création du client Mongo
client = MongoClient("mongodb+srv://admin:1234@test.a2y5cje.mongodb.net/")

# Base de données
db = client["test"]

# Collection
profs_col = db["profs"]
conseillers_col = db["conseillers"]

app.config["JWT_SECRET_KEY"] = "Sésame ouvre-toi"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
jwt = JWTManager(app)

@app.route('/login-test-apidocs')
def login_test_apidocs():
    return jsonify({"access_token": create_access_token(identity='test')}), 200

@app.route('/v1/tibinc/login-prof', methods=['POST'])
def login_prof():
    data = request.get_json()

    courriel = data.get("courriel")
    password = data.get("password")

    prof = profs_col.find_one({"courriel": courriel})

    if not prof:
        return jsonify({"message": "Utilisateur introuvable"}), 404

    if prof["password"] != password:
        return jsonify({"message": "Mot de passe invalide"}), 401

    access_token = create_access_token(identity=courriel)
    print("TOKEN SESSION ds service auth:", access_token)

    return jsonify({
        "token": access_token,
        "courriel": courriel
    }), 200

@app.route('/v1/tibinc/login-cp', methods=['POST'])
def login_cp():
    data = request.get_json()

    courriel = data.get("courriel")
    password = data.get("password")

    conseiller = conseillers_col.find_one({"courriel": courriel})

    if not conseiller:
        return jsonify({"message": "Utilisateur introuvable"}), 404

    if conseiller["password"] != password:
        return jsonify({"message": "Mot de passe invalide"}), 401

    access_token = create_access_token(identity=courriel)
    print("TOKEN SESSION ds service auth:", access_token)

    return jsonify({
        "token": access_token,
        "courriel": courriel
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5100)