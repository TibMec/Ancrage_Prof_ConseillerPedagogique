from flask import Flask, jsonify, request, session
from html import escape
from datetime import datetime

from pymongo import MongoClient
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager, create_access_token
from flasgger import Swagger, swag_from
from mod_modele_pydantic import Prof, CP

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "Sésame ouvre-toi"

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API Tibinc",
        "description": "Service d'ancrage enseignant-conseiller pédagogique",
        "version": "1.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Coller la chaine obtenue dans la route http://127.0.0.1:5600/login-test-apidocs",
        }
    }
}

jwt = JWTManager(app)

# Création du client Mongo
client = MongoClient("mongodb+srv://admin:1234@test.a2y5cje.mongodb.net/")

# Base de données
db = client["test"]

# Collection
profs_col = db["profs"]
conseillers_col = db["conseillers"]

# Index unique pour le courriel
profs_col.create_index("courriel", unique=True)
conseillers_col.create_index("courriel", unique=True)

def api_headers():
    token = session.get("token")
    return {
        "Authorization": f"Bearer {token}"
    }

@app.before_request
def debug_token():
    print("HEADER AUTH:", request.headers.get("Authorization"))

@app.before_request
def bypass_jwt_for_swagger():
    swagger_paths = [
        "/apidocs",
        "/apidocs/",
        "/apispec.json",
        "/flasgger_static"
    ]

    for path in swagger_paths:
        if request.path.startswith(path):
            return

#Routes ===============================================================================
#DAO PROFS =================================================
#GET (READ)
@app.route('/v1/tibinc/professeurs-dao')
@jwt_required()
@swag_from("doc/tous_les_profs.yml")
def get_teachers():
    current_user = get_jwt_identity()
    print("Utilisateur connecté:", current_user)
    profs = []
    for p in profs_col.find():
        prof = Prof.model_validate(p)
        profs.append(prof.model_dump(exclude={"password"}))
    return jsonify({'professeurs': profs})

#GET
@app.route('/v1/tibinc/professeurs-dao/<string:email>')
@jwt_required()
def get_teacher_by_email(email):
    trouve = profs_col.find_one({"courriel": email})
    if not trouve:
        return jsonify({'error': escape('Aucun prof trouvé')}), 404
    prof = Prof.model_validate(trouve)
    return jsonify({'prof': prof.model_dump(exclude={"password"})}), 200


#POST (CREATE)
@app.route('/v1/tibinc/professeurs-dao/', methods=['POST'])
@swag_from('doc/creer_prof.yml')
def create_teacher():
    data = request.get_json()

    # Vérifier unicité courriel
    if profs_col.find_one({'courriel': data['courriel']}):
        return jsonify({'Erreur': 'courriel déjà utilisé'}), 409

    #validation du data
    try:
        nouveau_prof = Prof(**data)
        profs_col.insert_one(nouveau_prof.model_dump())
    except Exception as e:
        return jsonify({'Erreur de creation': str(e)}), 400

    return jsonify({
        "message": "prof créé avec succès",
        "prof": nouveau_prof.model_dump(exclude={"password"})
    }), 201

#PUT (UPDATE)
@app.route('/v1/tibinc/professeurs-dao/<string:email>', methods=['PUT'])
@jwt_required()
def update_teacher(email):
    data = request.get_json()

    # validation pydantic
    try:
        prof = Prof(**data)
    except Exception as e:
        return jsonify({'Erreur de mise à jour': str(e)}), 400

    result = profs_col.update_one({'courriel': email}, {'$set': prof.model_dump()})

    if result.matched_count == 0:
        return jsonify({'message': "prof non trouvé"}), 404

    return jsonify({'message': "prof mis à jour"}), 200


#DELETE (DELETE)
@app.route('/v1/tibinc/professeurs-dao/<string:email>', methods=['DELETE'])
@jwt_required()
def delete_teacher_by_email(email):
    trouve = profs_col.find_one({"courriel": email})
    if not trouve:
        return jsonify({'error': escape('Aucun prof avec ce courriel')}), 404
    profs_col.delete_one({"courriel": email})
    return jsonify({'message': "prof supprimé"}), 200

#TROUVER SON CONSEILLER PEDAGOGIQUE
@app.route('/v1/tibinc/professeurs-dao/lierConseiller', methods=['GET'])
@jwt_required()
@swag_from('doc/mes_conseillers.yml')
def link_teacher_to_advisor():
    try:
        courriel = get_jwt_identity()
        if not courriel:
            return jsonify({'message': "Utilisateur non authentifié"}), 400

        # Récupération du prof
        prof = profs_col.find_one({'courriel': courriel})
        if not prof:
            return jsonify({'message': "Prof non trouvé"}), 404

        # Récupération des conseillers qui ont au moins une matière en commun
        conseillers = list(conseillers_col.find({
            'codesMatieres': {'$in': prof.get('codesMatieres', [])}
        }))

        # Conversion des ObjectId en string pour JSON si besoin
        for c in conseillers:
            c['_id'] = str(c['_id'])

        return jsonify({
            'prof': prof['courriel'],
            'codesMatieres': prof.get('codesMatieres', []),
            'conseillers': conseillers
        })

    except Exception as e:
        return jsonify({'message': str(e)}), 500

#DAO CONSEILLERS =================================================
#POST (CREATE)
@app.route('/v1/tibinc/conseillers-dao/', methods=['POST'])
@jwt_required()
def create_advisor():
    data = request.get_json()

    # Vérifier unicité courriel
    if conseillers_col.find_one({'courriel': data['courriel']}):
        return jsonify({'Erreur': 'courriel déjà utilisé'}), 409

    #validation pydantic
    try:
        nouveau_cp = CP(**data)
        conseillers_col.insert_one(nouveau_cp.model_dump())
    except Exception as e:
        return jsonify({'Erreur de creation': str(e)}), 400

    return jsonify({
        "message": "conseiller créé avec succès",
        "conseiller": nouveau_cp.model_dump(exclude={"password"})
    }), 201

#PUT (UPDATE)
@app.route('/v1/tibinc/conseillers-dao/<string:email>', methods=['PUT'])
@jwt_required()
def update_advisor(email):
    data = request.get_json()

    # validation pydantic
    try:
        cp = CP(**data)
    except Exception as e:
        return jsonify({'Erreur de mise à jour': str(e)}), 400

    result = conseillers_col.update_one({'courriel': email}, {'$set': cp.model_dump()})

    if result.matched_count == 0:
        return jsonify({'message': "conseiller non trouvé"}), 404

    return jsonify({'message': "conseiller mis à jour"}), 200

#DELETE (DELETE)
@app.route('/v1/tibinc/conseillers-dao/<string:email>', methods=['DELETE'])
@jwt_required()
def delete_advisor_by_email(email):
    trouve = conseillers_col.find_one({"courriel": email})
    if not trouve:
        return jsonify({'error': escape('Aucun conseiller avec ce courriel')}), 404
    conseillers_col.delete_one({"courriel": email})
    return jsonify({'message': "conseiller supprimé"}), 200

@app.route('/login-test-apidocs')
def login_test_apidocs():
    return "Bearer " + create_access_token(identity='jcho@csdm.com'), 200

if __name__ == '__main__':
    swagger = Swagger(app,template=swagger_template)
    app.run(debug=True, port=5600)