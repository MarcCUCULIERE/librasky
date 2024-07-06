import pyodbc
import youtils
import json
import time
from datetime import datetime, date
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Librasky', description='Une API simple pour gerer les collections.')
ns = api.namespace('/', description='Opérations principales')

data_model = api.model('Create',{
    'Quantite': fields.Integer(required=True, description='Quantité de bouteille détenue(s)'),
    'Nom': fields.String(required=True, description='Nom de l\'Edition'),
    'Distillerie': fields.String(required=True, description='Distillerie'),
    'Année': fields.Integer(required=True, description='Année d\'achat de la bouteille'),
    'Age': fields.Integer(required=True, description='Age de la bouteille en année(s)'),
    'Degrés': fields.Float(required=True, description='Degrés d\'alcool de la bouteille'),
    'Date_achat': fields.Date(required=True, description='Date d\'achat'),
    'Prix': fields.Float(required=True, description='Prix')
})

def fetch_data():
    conn = None
    try:
        conn = youtils.connect_to_sql_server()
        if conn is None:
            raise ConnectionError("Failed to connect to the database.")
        cursor = conn.cursor()
        cursor.execute("SELECT Quantite, Nom, Distillerie, Année, Age, Degrés, Date_achat, Prix FROM Collection")
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return data
    except pyodbc.Error as err:
        app.logger.error(f"Database error: {err}")
        return {"error": "Database operation failed"}, 500
    except ConnectionError as e:
        app.logger.error(f"Connection error: {e}")
        return {"error": "Failed to connect to the database"}, 500
    finally:
        if conn:
            conn.close()

# Example of a simple health check endpoint
@api.route('/health/ping')
class HealthCheck(Resource):
    def get(self):
        try:
            conn = youtils.connect_to_sql_server()
            if conn is None:
                raise ConnectionError("Database connection failed")
            return "pong", 200
        except ConnectionError as e:
            app.logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy"}, 503

@api.route('/create')
class InsertData(Resource):
    @api.expect(data_model)
    def post(self):
        data = request.json
        quantite = data.get("Quantite")
        nom = data.get("Nom")
        distillerie = data.get("Distillerie")
        annee = data.get("Année")
        age = data.get("Age")
        degres = data.get("Degrés")
        date_achat = data.get("Date_achat")
        prix = data.get("Prix")
        try:
            conn = youtils.connect_to_sql_server()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Collection (Quantite, Nom, Distillerie, Année, Age, Degrés, Date_achat, Prix) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                       (quantite, nom, distillerie, annee, age, degres, date_achat, prix))
            conn.commit()
            print(f"Données insérées avec succès : {quantite}, {nom}, {distillerie}, {annee}, {age}, {degres}, {date_achat}, {prix}")
        except pyodbc.Error as e:
            print("Erreur lors de l'insertion des données:", str(e))
        finally:
            if conn:
                conn.close()
        return jsonify({"message": "Data inserted successfully", "data": data})

@api.route('/list')
class ListData(Resource):
    def get(self):
        data = fetch_data()
        return jsonify(data)
    
@api.route('/update')
class UpdateData(Resource):
    @api.expect(data_model)
    def put(self):
        data = request.json
        quantite = data.get("Quantite")
        nom = data.get("Nom")
        distillerie = data.get("Distillerie")
        annee = data.get("Année")
        age = data.get("Age")
        degres = data.get("Degrés")
        date_achat = data.get("Date_achat")
        prix = data.get("Prix")
        try:
            conn = youtils.connect_to_sql_server()
            cursor = conn.cursor()
            cursor.execute("UPDATE Collection SET Quantite=?, Nom=?, Distillerie=?, Année=?, Age=?, Degrés=?, Date_achat=?, Prix=? WHERE Nom=?", 
                       (quantite, nom, distillerie, annee, age, degres, date_achat, prix, nom))
            conn.commit()
            print(f"Données mises à jour avec succès : {quantite}, {nom}, {distillerie}, {annee}, {age}, {degres}, {date_achat}, {prix}")
        except pyodbc.Error as e:
            print("Erreur lors de la mise à jour des données:", str(e))
        finally:
            if conn:
                conn.close()
        return jsonify({"message": "Data updated successfully", "data": data})

@api.route('/delete')
class DeleteData(Resource):
    @api.expect(data_model)
    def delete(self):
        data = request.json
        nom = data.get("Nom", "Distillerie", "Année", "Age", "Degrés", "Date_achat", "Prix")
        try:
            conn = youtils.connect_to_sql_server()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Collection WHERE Nom=?, Distillerie=?, Quantite=?, ", (quantite, nom,))
            conn.commit()
            print(f"Données supprimées avec succès : {nom}")
        except pyodbc.Error as e:
            print("Erreur lors de la suppression des données:", str(e))
        finally:
            if conn:
                conn.close()
        return jsonify({"message": "Data deleted successfully", "data": data})

@api.route('/search')
class SearchData(Resource):
    @api.doc(params={'query': 'The search query'})
    def get(self):
        data = fetch_data()
        query = request.args.get("query")
        result = [item for item in data if query.lower() in item["Distillerie"].lower() or query.lower() in item["Nom"].lower()]
        return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)