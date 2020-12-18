from functools import wraps

import firebase_admin
from firebase_admin import auth
from flask import request, json
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from model import db, User, UserSchema, Wallet

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        # data = json.loads(request.data)
        data = request.form
        token = data['idtoken']
        try:
            decoded_token = auth.verify_id_token(token)
            if(data['uid'] == decoded_token['uid']):
                pass
            else:
                return 'authfailed'
        except firebase_admin.auth.InvalidIdTokenError:
            return 'authfailed'
        return f(*args, **kwargs)
    return decorated

class CreateUser(Resource):
    method_decorators = [token_required]
    def post(self):
        # data = json.loads(request.data)
        data = request.form
        # user = User(id=request.data.decode("utf-8").replace('"',''))
        try:
            user = User(id=data['uid'])
            db.session.add(user)
            db.session.commit()
            return user.id
        except IntegrityError:
            return {'status':0,'message':'duplicate_entry'}
