from Util.BodyParser import BodyParser
from flask_restful import Resource
from Models.Store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.findByName(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.findByName(name):
            return {'message', "The store already exists with the name: '{}'".format(name)}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': 'An error ocurred while creating the store'}, 500

        return store.json()

    def delete(self, name):
        store = StoreModel.findByName(name)

        if store:
            store.delete_from_db()
        
        return {'message': 'Store deleted'}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}