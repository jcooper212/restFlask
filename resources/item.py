import sqlite3
from flask_restful import Resource, Api,request, reqparse
from flask_jwt import JWT, jwt_required
from models.item_model import ItemModel

#item resource
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left blank")
    
    parser.add_argument('store_id',
            type=int,
            required=True,
            help="Every item needs a store id")      

    @jwt_required()
    def get(self, name):
        # for it in items:
        #     if (it['name'] == name):
        #         return it
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

        # item = next(filter(lambda x: x['name'] == name, items), None) #if not found return None
        # return {"Item": item}, 200 if item is not None else 404



    def post(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        # if (next(filter(lambda x: x['name'] == name, items), None)) is not None:
        #     return {'message': "An item with name '{}' already exists.".format(name)}, 400
        # print("reached pos2")

        data = Item.parser.parse_args()

        #data = request.get_json(force = True) #Force = True means returns ok for difft datatypes
        item = ItemModel(name,data['price'], data['store_id'])
        
        try:
            item.save_to_db()
        except: 
            return {'message':'item could not be inserted into db'}, 500
        

        return item.json(), 201

    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))

        item = ItemModel.find_by_name(name)
        if item is None:
            return {'message': "An item with name '{}' does not exist.".format(name)}, 400
        else: item.delete_from_db()

        return {'message': 'Item deleted'}

        # if (next(filter(lambda x: x['name'] == name, items), None)) is not None:
        #     return {'message': "An item with name '{}' already exists.".format(name)}, 400
        # print("reached pos2")
        # #data = Item.parser.parse_args()

        #data = request.get_json(force = True) #Force = True means returns ok for difft datatypes
        #item = {'name': name, 'price': data['price']}
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # qry = "DELETE FROM items WHERE name=?"
        # cursor.execute(qry, (name,))
        # connection.commit()
        # connection.close()
        
    
    def put(self, name):
       
       item = ItemModel.find_by_name(name)
       data = Item.parser.parse_args()
       
       if item is None:
           #same as below// item = ItemModel(name, data['price'], data['store_id'])
           item = ItemModel(name, **data)

       else:
           item.price = data['price']
           item.store_id = data['store_id']

       item.save_to_db()
       
       return item.json(), 201

        # item = next(filter(lambda x: x['name'] == name, items), None)
        # if item is None:
        #     item = {'name':name, 'price': data['price']}
        #     items.append(item)
        # else:
        #     item.update(data)

# ItemList
class ItemList(Resource):
    def get(self):

        #return {'items': [item.json() for item in ItemModel.query.filter_by(name=name).all()]}
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

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

