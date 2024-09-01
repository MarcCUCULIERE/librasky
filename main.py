import logging
import youtils
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app, version='1.0', title='Librasky', description='Une API simple pour gérer les collections.')
ns = api.namespace('/', description='Opérations principales')

data_model = api.model('Create', {
    'Quantite': fields.Integer(required=True, description='Quantité de bouteille détenue(s)'),
    'Nom': fields.String(required=True, description='Nom de l\'Edition'),
    'Distillerie': fields.String(required=True, description='Distillerie'),
    'Année': fields.Integer(required=True, description='Année d\'achat de la bouteille'),
    'Age': fields.Integer(required=True, description='Age de la bouteille en année(s)'),
    'Degrés': fields.Float(required=True, description='Degrés d\'alcool de la bouteille'),
    'Date_achat': fields.Date(required=True, description='Date d\'achat'),
    'Prix': fields.Float(required=True, description='Prix')
})

@api.route('/health/ping')
class HealthCheck(Resource):
    def get(self):
        conn = youtils.connect_to_sql_server()
        if conn:
            conn.close()
            return "pong", 200
        return {"status": "unhealthy"}, 503

@api.route('/create')
class InsertData(Resource):
    @api.expect(data_model)
    def post(self):
        data = request.json
        query = "INSERT INTO Collection (Quantite, Nom, Distillerie, Année, Age, Degrés, Date_achat, Prix) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        params = (data['Quantite'], data['Nom'], data['Distillerie'], data['Année'], data['Age'], data['Degrés'], data['Date_achat'], data['Prix'])
        conn, cursor = youtils.execute_query(query, params)
        if cursor:
            conn.close()
            return jsonify({"message": "Data inserted successfully", "data": data})
        return {"error": "Failed to insert data"}, 500

@api.route('/list')
class ListData(Resource):
    def get(self):
        data = youtils.fetch_data()
        if data:
            return jsonify(data)
        return {"error": "Failed to fetch data"}, 500

@api.route('/update')
class UpdateData(Resource):
    @api.expect(data_model)
    def put(self):
        data = request.json
        query = "UPDATE Collection SET Quantite=?, Nom=?, Distillerie=?, Année=?, Age=?, Degrés=?, Date_achat=?, Prix=? WHERE Nom=?"
        params = (data['Quantite'], data['Nom'], data['Distillerie'], data['Année'], data['Age'], data['Degrés'], data['Date_achat'], data['Prix'], data['Nom'])
        conn, cursor = youtils.execute_query(query, params)
        if cursor:
            conn.close()
            return jsonify({"message": "Data updated successfully", "data": data})
        return {"error": "Failed to update data"}, 500

@api.route('/delete')
class DeleteData(Resource):
    @api.expect(data_model)
    def delete(self):
        data = request.json
        query = "DELETE FROM Collection WHERE Nom=?"
        params = (data['Nom'],)
        conn, cursor = youtils.execute_query(query, params)
        if cursor:
            conn.close()
            return jsonify({"message": "Data deleted successfully", "data": data})
        return {"error": "Failed to delete data"}, 500

@api.route('/search')
class SearchData(Resource):
    @api.doc(params={'query': 'The search query'})
    def get(self):
        data = fetch_data()
        query = request.args.get("query")
        result = [item for item in data if query.lower() in item["Distillerie"].lower() or query.lower() in item["Nom"].lower()]
        return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)