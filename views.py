from main import insert_data, list_data as ld, update_data, delete_data
from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Librasky', description='Une API simple pour gerer les collections.')
ns = api.namespace('/', description='Opérations principales')

create_model = api.model('Create', {
    'Quantite': fields.Integer(required=True, description='Quantité'),
    'Nom': fields.String(required=True, description='Nom'),
    'Distillerie': fields.String(required=True, description='Distillerie'),
    'Année': fields.Integer(required=True, description='Année'),
    'Age': fields.Integer(required=True, description='Age'),
    'Degrés': fields.Float(required=True, description='Degrés'),
    'Date_achat': fields.Date(required=True, description='Date d\'achat'),
    'Prix': fields.Float(required=True, description='Prix')
})

def configure_routes(app):

#    @app.route('/create', methods=['POST'])
#    def create_data():
#        # Ici, vous récupérerez les données envoyées par l'utilisateur
#        # et appellerez la fonction de création (similaire à votre extrait de code)
#        return jsonify({"message": "Donnée créée avec succès"}), 200

    @app.route('/read', methods=['GET'])
    def read_data():
        # Ici, vous appellerez la fonction de lecture (similaire à votre extrait de code)
        return jsonify({"message": "Donnée lue avec succès"}), 200
    

    @app.route('/update', methods=['POST'])
    def update_data():
        # Ici, vous récupérerez les données envoyées par l'utilisateur
        # et appellerez la fonction de mise à jour (similaire à votre extrait de code)
        return jsonify({"message": "Donnée mise à jour avec succès"}), 200

    @app.route('/delete', methods=['POST'])
    def delete_data():
        # Ici, vous récupérerez les données envoyées par l'utilisateur
        # et appellerez la fonction de suppression (similaire à votre extrait de code)
        return jsonify({"message": "Donnée supprimée avec succès"}), 200

@api.route('/list')
class ListData(Resource):
    def get(self):
        return ld()

@api.route('/create')
class CreateData(Resource):
    @api.expect(create_model)
    def post(self):
        # Récupération des données envoyées par l'utilisateur
        data = request.get_json()
        print(data)

        quantite = data.get('quantite')
        nom = data.get('nom')
        distillerie = data.get('distillerie')
        annee = data.get('annee')
        age = data.get('age')
        degres = data.get('degres')
        date_achat = data.get('date_achat')
        prix = data.get('prix')
        
        # Appel de la fonction de création avec tous les arguments nécessaires
        response = insert_data(quantite, nom, distillerie, annee, age, degres, date_achat, prix)
        return response

if __name__ == '__main__':
    app.run(debug=True)