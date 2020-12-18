from flask import Blueprint
from flask_restful import Api
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

from resources.User import *

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
cred = credentials.Certificate("firebase-admin-sdk-service.json")
firebase_admin.initialize_app(cred)

# Route
#USER
api.add_resource(CreateUser, '/createuser')
