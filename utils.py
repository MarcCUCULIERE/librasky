from flask import jsonify

def send_response(message, status_code=200):
    """Fonction pour envoyer des réponses JSON standardisées."""
    return jsonify({"message": message}), status_code