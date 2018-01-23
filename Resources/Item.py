from Util.BodyParser import BodyParser
from flask_restful import Resource
from flask_jwt import jwt_required
from Models.Item import ItemModel


class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = ItemModel.findByName(name)
        if item:
            return item.json()

        return {'Message': 'Item not found!'}, 404

    def post(self, name):

        if ItemModel.findByName(name):
            return {'Message': "Item '{}' already exist".format(name)}, 400

        data = BodyParser.bodyParser(
            [{'key': 'price', '_type': float, '_required': True, '_help': 'This field is necessary to create an Item!'},
             {'key': 'store_id', '_type': int, '_required': True, '_help': 'Every item needs a store id.'}])

        item = ItemModel(None, name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            # internal server error
            return {'Message': 'An error ocurred inserting the item'}, 500

        return item.json(), 201

    def put(self, name):
        data = BodyParser.bodyParser(
            [{'key': 'price', '_type': float, '_required': True, '_help': 'This field is necessary to create an Item!'},
            {'key': 'store_id', '_type': int, '_required': True, '_help': 'Every item needs a store id.'}])

        item = ItemModel.findByName(name)

        if item is None:
            item = ItemModel(None, name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()

    def delete(self, name):
        item = ItemModel.findByName(name)
        if item:
            item.delete_from_db()
        return {'success': True, 'Message': 'Item deleted'}


class ItemList(Resource):
    def get(self):
        print(ItemModel.query.all())
        
        return {'Items':[item.json() for item in ItemModel.query.all()] }

