from flask import Blueprint
from flask_jwt_extended import jwt_required

from ...models.userModel import User
from ...models.postModel import Post
from ...controllers import postController
from ...controllers import handlerFactory

postRoutes = Blueprint('postRoutes', __name__)

@postRoutes.route('/api/v1/posts', methods=['GET'])
def getAll():
    return handlerFactory.getAll(Post)

@postRoutes.route('/api/v1/posts/getN', methods=['GET'])
def getN():
    return handlerFactory.getN(Post)

@postRoutes.route('/api/v1/posts/<string:postId>', methods=['GET'])
def getOne(postId):
    return handlerFactory.getOne(postId, Post,
                                populate=True,
                                populateData={
                                    'field': 'author',
                                    'model': User,
                                    'hideFields': ['password', 'passwordConfirm',
                                                    'passwordChangedAt', '_createdAt',
                                                    'active', 'confirmEmailToken']
                                })

@postRoutes.route('/api/v1/posts/search', methods=['GET'])
def searchPosts():
    return handlerFactory.searchByQueryString(Post)


@postRoutes.route('/api/v1/posts/<string:postId>', methods=['DELETE'])
@jwt_required()
def deleteOne(postId):
    return handlerFactory.deleteOne(postId, Post)


@postRoutes.route('/api/v1/posts', methods=['POST'])
@jwt_required()
def createOne():
    return postController.createOne()


@postRoutes.route('/api/v1/posts/<string:postId>', methods=['PATCH'])
@jwt_required()
def updateOne(postId):
    return postController.updateOne(postId)