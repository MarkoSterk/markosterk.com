from flask import Blueprint
from flask_jwt_extended import jwt_required
from ...models.userModel import User
from ...controllers import userController
from ...controllers import handlerFactory
from ...controllers import authController

userRoutes = Blueprint('userRoutes', __name__)


####endpoint functions/routes
@userRoutes.route('/api/v1/users', methods=['GET'])
@jwt_required()
def getAll():
    return handlerFactory.getAll(User)

@userRoutes.route('/api/v1/users/getN', methods=['GET'])
@jwt_required()
def getN():
    return handlerFactory.getN(User)

@userRoutes.route('/api/v1/users/<string:userId>', methods=['GET'])
@jwt_required()
def getOne(userId):
    return handlerFactory.getOne(userId, User)


@userRoutes.route('/api/v1/users/<string:userId>', methods=['DELETE'])
@jwt_required()
def deleteOne(userId):
    return handlerFactory.deleteOne(userId, User)


@userRoutes.route('/api/v1/users/update/<string:userId>', methods=['PATCH'])
@jwt_required()
def updateOne(userId):
    return userController.updateOne(userId)


@userRoutes.route('/api/v1/users/updatePassword/<string:userId>', methods=['PATCH'])
@jwt_required()
def updatePassword(userId):
    return userController.updatePassword(userId)


@userRoutes.route('/api/v1/users/signup', methods=['POST'])
def createOne():
    return userController.createOne()


@userRoutes.route('/api/v1/users/confirmEmail/<string:confirm_token>', methods=['GET'])
def confirmEmail(confirm_token):
    return userController.confirmEmail(confirm_token)


@userRoutes.route('/api/v1/users/resetPasswordToken', methods=['POST'])
def resetPasswordToken():
    return userController.resetPasswordToken()


@userRoutes.route('/api/v1/users/resetPassword/<string:reset_token>', methods=['POST'])
def resetPassword(reset_token):
    return userController.resetPassword(reset_token)


@userRoutes.route('/api/v1/users/login', methods=['POST'])
def login():
    return authController.login()


@userRoutes.route('/api/v1/users/logout', methods=['GET'])
@jwt_required()
def logout():
    return authController.logout()

@userRoutes.after_request
def refresh_expiring_jwts(response):
    return authController.refreshExpiringJWTS(response)


###after request functions
@userRoutes.after_request
def removeResponseFields(response):
    return userController.removeResponseFields(response, 
                            remove_fields=['password',
                                            'passwordConfirm',
                                            'active',
                                            'passwordChangedAt',
                                            'confirmEmailToken',
                                            'passwordResetToken',
                                            'tokenExpires'])





