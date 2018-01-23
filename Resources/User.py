import sqlite3
from flask_restful import Resource, reqparse
from Util.BodyParser import BodyParser
from Models.User import UserModel

class UserResgister(Resource):

    def post(self):
        
        data = BodyParser.bodyParser([
            {
                'key': 'username',
                '_type': str,
                '_required': True,
                '_help': 'This field cannot be blank!'
            },
            {
                'key': 'password',
                '_type': str,
                '_required': True,
                '_help': 'This field cannot be blank!'
            }
        ])

        if UserModel.findByUserName(data['username']):
            return {'Message': 'User already exists', 'success': False}, 400

        user = UserModel(**data)

        user.save_to_db()

        return {'message': 'User created successfully'}, 201
