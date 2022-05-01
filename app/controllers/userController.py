from bcrypt import hashpw
from flask import request, jsonify, current_app, url_for
from ..utils.helperFuncs import hashUrlSafe
from ..utils.email import sendEmailToken
from .errorController import AppError
from ..models.userModel import User
from app import bcrypt
from datetime import datetime
import json

###route controllers
def createOne():
    data = User.filterData(request.form.to_dict())
    data['confirmEmailToken'] = hashUrlSafe(current_app.config['SECRET_KEY'])

    user = User(data)
    user.save(pre_hooks=[user.hashpw])

    url = url_for('userRoutes.confirmEmail', confirm_token=data['confirmEmailToken'])
    sendEmailToken(data['email'],
                    'Confirm email address',
                    f'Please follow this link to activate your account: {url}')
    
    return jsonify({
        'status': 'success',
        'data': [vars(user)],
        'message': 'User signed up successfully. Please activate your account by following the instructions in the email we sent you.'
    }), 200


def updateOne(userId):
    data = User.filterData(request.form.to_dict())
    if(('password' in data.keys()) or ('passwordConfirm' in data.keys())):
        return AppError('Please use /changePassword for changing password', 400)
    
    user = User.findOne({'_id': userId})
    user.update({'$set': data})
    return jsonify({
        'status': 'success',
        'data': [vars(user)],
        'message': 'Update successfull'
    }), 200

def updatePassword(userId):
    data = request.get_json()
    if ('currentPassword' or 'newPassword' or 'confirmNewPassword') not in data.keys():
        return AppError('Input field missing', 400)

    user = User.findOne({'_id': userId})
    if not bcrypt.check_password_hash(user.password, data['currentPassword']):
        return AppError('Current password does not match the database', 401)

    user.update({'$set': {'password': data['newPassword'],
                'passwordConfirm': data['confirmNewPassword'],
                'passwordChangedAt': datetime.utcnow().strftime('%Y-%m-%d %H:%M')}},
                pre_hooks=[user.hashpw])

    return jsonify({
        'status': 'success',
        'data': [vars(user)],
        'message': 'Password updated successfully'
    }), 200


def confirmEmail(confirm_token):
    user = User.findOne({'confirmEmailToken': confirm_token})
    if not user:
        return AppError('Invalid token. User not found.', 404)
    
    if bcrypt.check_password_hash(confirm_token, current_app.config['SECRET_KEY'])==False:
        return AppError('Invalid activation token.', 400)
    
    user.update({'$set': {'active': True},
                '$unset': {'confirmEmailToken': ''}})

    return jsonify({
        'status': 'success',
        'data': [vars(user)],
        'message': 'Email confirmed successfully'
    })


def resetPasswordToken():
    data = User.filterData(request.get_json())
    if 'email' not in data.keys(): return AppError('Email is required', 400)

    user = User.findOne({'email': data['email']})
    if not user: return AppError('User with this email does not exist', 404)

    exp_time = int(datetime.utcnow().timestamp()) + int(current_app.config['PASS_RESET_TOKEN_DURATION'])
    
    reset_token = hashUrlSafe(current_app.config['SECRET_KEY'])
    user.update({'$set': {'passwordResetToken': reset_token,
                        'tokenExpires': exp_time}})

    url = url_for('userRoutes.resetPassword', reset_token=reset_token)
    ####Change the URL string to a valid string once in production (add base url + protocol)
    sendEmailToken(request.get_json()['email'],
                        'Password reset token',
                        f"Please follow this link to reset your password: {url}")

    return jsonify({
        'status': 'success',
        'data': None,
        'message': f'Password reset token sent to {user.email}'
    }), 200


def resetPassword(reset_token):
    user = User.findOne({'passwordResetToken': reset_token})
    if not user:
        return AppError('Invalid reset token. User does not exist.', 404)

    if int(user.tokenExpires) < int(datetime.utcnow().timestamp()):
        return AppError('This password reset token expired. Please get a new one!'), 400

    if bcrypt.check_password_hash(reset_token, current_app.config['SECRET_KEY'])==False:
        return AppError('Corrupt password reset URL.', 401)
    
    data = User.filterData(request.get_json())
    password, passwordConfirm = data['password'], data['passwordConfirm']

    user.update({'$set': {'password': password, 'passwordConfirm': passwordConfirm},
                '$unset': {'passwordResetToken': '',
                            'tokenExpires': ''}}, pre_hooks=[hashpw]
                )

    return jsonify({
        'status': 'success',
        'message': 'Password was reset successfully'
    }), 200




####after request controllers
def removeResponseFields(response, remove_fields):
    try: #tries to filter out unwanted data fields in the response
        data = response.get_json()
        for r in data['data']:
            for key in remove_fields:
                if key in r.keys():
                    del r[key]
        response.data = json.dumps(data)
        return response
    except:
        return response