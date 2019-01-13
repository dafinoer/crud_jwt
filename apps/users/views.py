from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required, current_identity
import sqlite3

users = []


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class Register(Resource):
    
    def post(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, requirment=True)
        parser.add_argument('username', type=str, requirment=True)
        parser.add_argument('password', type=str, requirment=True)

        data = parser.parse_args()

        query_select = 'select id from users where id= ?'
        select_query = cursor.execute(query_select, (data['id'],))
        query_result = select_query.fetchone()

        if query_result[0] == data['id']:
            return {'message': 'data {} exist'.format(data['id'])}

        select_query = 'insert into users values (?, ?, ?)'
        
        cursor.execute(select_query, (
                data['id'],
                data['username'],
                data['password'])
            )
        
        connection.commit()
        connection.close()


class Items(Resource):

    @jwt_required()
    def get(self):

        if len(users) != 0:
            return {'items': users}
        else:
            return {'items': None}


class Users(Resource):

    def get(self, name):
        text = next(filter(lambda x: x['name'] == name, users), None)
        return {'users': text}, 200 if text is not None else 404
    
    def post(self, name):

        items = next(filter(lambda x: x['name'] == name, users), None)
        if items is not None:
            return {'message': 'data sudah ada'}
        
        parser = reqparse.RequestParser()
        # validation
        parser.add_argument('power', type=int, required=True) 
        data = parser.parse_args()
        item = {'name': name, 'power': data['power']}
        users.append(item)

        return item
    
    def delete(self, name):

        global users
        item = list(filter(lambda x: x['name'] != name, users))
        users = item
        return {'message': 'data berhasil dihapus'}
    
    def put(self, name):

        parser = reqparse.RequestParser()

        parser.add_argument('power', type=int, required=True)
        data = parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, users), None)

        if item is None:
            k = {'name': name, 'power': data['power']}
            users.append(k)
            return k
        
        else:
            item.update(data)
            return item
