from flask import request, jsonify

def configure_routes(app):

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