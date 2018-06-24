import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
            type=str,
            required=True,
            help="This field cannot be left blank")
    parser.add_argument('password',
            type=str,
            required=True,
            help="This field cannot be left blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        #print ("**********am here", data['username'], data['password'])

        if UserModel.find_by_username(data['username']) is not None:
            return{'message': 'User already exists'},400
        
        user = UserModel(1, data['username'], data['password'])
        #print (data['username'], data['password'])
        #also can -- user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created'},201

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "INSERT INTO users VALUES(NULL, ?, ?)"
        # cursor.execute(query,(data['username'], data['password']))

        # connection.commit()
        # connection.close()

