from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user
from ...controllers import cmsController
from ...models.postModel import Post

cmsRoutes = Blueprint('cmsRoutes', __name__)

@cmsRoutes.route('/cms/sendContactForm', methods=['POST'])
def sendContactForm():
    return cmsController.sendContactForm()


@cmsRoutes.route('/cms/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    posts = Post.findMany({'author': current_user._id})
    return render_template('cms/dashboard.html', 
                            title='Dashboard', 
                            posts = posts)


@cmsRoutes.route('/cms/addPost', methods=['GET'])
@jwt_required()
def addPost():
    categories = Post.Schema['category']['validators'][1][1]
    return render_template('cms/post.html', 
                            title='Add Post', 
                            categories = categories)


@cmsRoutes.route('/cms/editPost/<string:postSlug>', methods=['GET'])
@jwt_required()
def editPost(postSlug):
    categories = Post.Schema['category']['validators'][1][1]
    post = Post.findOne({'slug': postSlug})
    return render_template('cms/post.html', 
                            title='Edit Post', 
                            categories = categories,
                            post = post)
