from app import mongo
from xmlrpc.client import Boolean
from .validator import Validator
from .model import Model
from app import bcrypt


class User(Model):
    session=mongo.db
    collection = 'user'
    __ModelName__ = 'User'

    Schema = {
        'name': {
            'type': str,
            'validators': [
                (Validator.minLength, 5),
                (Validator.maxLength, 25)
            ],
            'required': True
        },
        'email': {
            'type': str,
            'validators': [
                (Validator.isEmail, True)
            ],
            'required': True,
            'unique': True
        },
        'password': {
            'type': str,
            'validators': [
                (Validator.minLength, 8),
                (Validator.mustMatch, 'passwordConfirm')
            ],
            'required': True
        },
        'passwordConfirm': {
            'type': str,
            'required': True
        },
        'active': {
            'type': Boolean,
            'required': True,
            'default': False
        },
        'role': {
            'type': str,
            'required': True,
            'default': 'user',
            'protected': True
        },
        'passwordChangedAt': {
            'type': str,
            'required': False
        },
        'confirmEmailToken': {
            'type': str,
            'required': False
        },
        'passwordResetToken': {
            'type': str,
            'required': False
        },
        'tokenExpires': {
            'type': str,
            'required': False
        }
    }
    
    def __init__(self, data, validate=True, onLoad=False):
        #super().__init__(user)
        Model.__init__(self, data, validate=validate, onLoad=onLoad)
    
    def hashpw(self):
        self.password = bcrypt.generate_password_hash(self.password).decode('utf-8')
        self.passwordConfirm = self.password
        return self