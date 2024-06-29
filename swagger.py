import swagger
from flask_restx import Api, Resource, fields

app = swagger.Flask(__name__)
api = Api(app, version='1.0', title='API de Ma Collection',
          description='Une API simple pour gérer une collection')

ns = api.namespace('collection', description='Opérations de collection')

item = api.model('Collection Item', {
    'id': fields.Integer(readonly=True, description='Identifiant unique de l\'élément'),
    'nom': fields.String(required=True, description='Nom de l\'élément')
})

class CollectionDAO(object):
    def __init__(self):
        self.counter = 0
        self.items = []

    def get(self, id):
        for item in self.items:
            if item['id'] == id:
                return item
        api.abort(404, "Item {} n'existe pas".format(id))

    def create(self, data):
        item = data
        item['id'] = self.counter = self.counter + 1
        self.items.append(item)
        return item

DAO = CollectionDAO()
DAO.create({'nom': 'Premier élément'})

@ns.route('/')
class CollectionList(Resource):
    '''Montre une liste des éléments, et permet d'en ajouter de nouveaux'''
    @ns.doc('list_collection')
    @ns.marshal_list_with(item)
    def get(self):
        '''Liste tous les éléments'''
        return DAO.items

    @ns.doc('create_item')
    @ns.expect(item)
    @ns.marshal_with(item, code=201)
    def post(self):
        '''Crée un nouvel élément'''
        return DAO.create(api.payload), 201

if __name__ == '__main__':
    app.run(debug=True)