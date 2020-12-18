from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()

###########################################User Model######################################################
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    is_registered = db.Column(db.Integer,nullable=False)
    payment_method = db.Column(db.Integer,nullable=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, id,is_registered=0,name='',phone=''):
        self.id = id
        self.name = name
        self.phone = phone
        self.is_registered = is_registered
        self.payment_method=0
        # Wallet will be generated regardless of user registration
        wallet = Wallet()
        db.session.add(wallet)
        db.session.commit()
        self.wallet_id = wallet.id

class UserSchema(ma.Schema):
    id = fields.String()
    name = fields.String()
    phone = fields.String()
    is_registered = fields.Integer()
    payment_method = fields.Integer()
    wallet_id = fields.Integer()

#########################################Wallet Model##############################################################

class Wallet(db.Model):
    __tablename__ = "wallet"
    id = db.Column(db.Integer,primary_key=True)
    wallet_balance = db.Column(db.Integer)

    def __init__(self):
        self.wallet_balance=0

