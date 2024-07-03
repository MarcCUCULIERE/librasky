# test_main.py
import pytest
from main import UpdateData  # Ajustez le chemin d'importation selon votre structure de projet

def test_update_data_success(monkeypatch):
    # Mock de la requête et de la réponse
    class MockRequest:
        json = {
            "Nom": "Spectacular",
            "Quantite": 2,
            # Ajoutez les autres champs nécessaires
        }
    
    class MockResponse:
        def jsonify(self, *args, **kwargs):
            return args, kwargs
    
    # Mock des fonctions et méthodes externes
    monkeypatch.setattr("flask.request", MockRequest())
    monkeypatch.setattr("flask.jsonify", MockResponse.jsonify)
    
    # Exécution du test
    response = UpdateData().put()
    assert "Data updated successfully" in response[1]["message"]