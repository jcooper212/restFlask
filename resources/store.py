import sqlite3
from flask_restful import Resource, Api,request, reqparse
from flask_jwt import JWT, jwt_required
from models.store_model import StoreModel

#item resource
class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
            type=str,
            required=True,
            help="This field cannot be left blank")    

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):

        store = StoreModel.find_by_name(name)
        if store:
            return {'message': "An store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        
        try:
            store.save_to_db()
        except: 
            return {'message':'store could not be inserted into db'}, 500
        

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {'message': "An store with name '{}' does not exist.".format(name)}, 400
        else: store.delete_from_db()

        return {'message': 'Store deleted'}
    
    def put(self, name):
       
       store = StoreModel.find_by_name(name)
       data = Store.parser.parse_args()
       
       if store is None:
           store = StoreModel(name)

    #    else:
    #        s.price = data['price']
    #        item.store_id = data['store_id']

       store.save_to_db()
       
       return store.json(), 201


# ItemList
class StoreList(Resource):
    def get(self):

        #return {'stores': [store.json() for store in StoreModel.query.filter_by(name=name).all()]}
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # qry = "SELECT * FROM items"
        # result = cursor.execute(qry)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        # # connection.commit()
        # connection.close()
        # return{'items': items}

