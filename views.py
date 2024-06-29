from flask import request, jsonify
from main import insert_data, list_data as ld, update_data, delete_data

def configure_routes(app):

    @app.route('/create', methods=['POST'])
    def create_data():
        # Ici, vous récupérerez les données envoyées par l'utilisateur
        # et appellerez la fonction de création (similaire à votre extrait de code)
        return jsonify({"message": "Donnée créée avec succès"}), 200

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

    @app.route('/list', methods=['GET'])
    def list_data():
        # Ici, vous appellerez la fonction de liste (similaire à votre extrait de code)
        data = ld()
        return jsonify(data), 200
        #return jsonify({data}), 200