from flask import Blueprint, redirect, render_template, url_for, request
from flask_jwt_extended import get_jwt_identity
from ...models.postModel import Post

mainRoutes = Blueprint('mainRoutes', __name__)

@mainRoutes.route('/', methods=['GET'])
def index():
    posts = [vars(p) for p in Post.findMany({'active': True})]
    return render_template('main/index.html', posts = posts)

@mainRoutes.route('/post/<string:postSlug>', methods=['GET'])
def post(postSlug):
    post = Post.findOne({'slug': postSlug})
    return render_template('main/post.html', post=post, title=post.title)

@mainRoutes.route('/about', methods=['GET'])
def about():
    return render_template('main/about.html', title='About Me')


@mainRoutes.route('/resume', methods=['GET'])
def resume():
    return render_template('main/detail.html', title='My Resume')


@mainRoutes.route('/contact', methods=['GET'])
def contact():
    return render_template('main/contact.html', title='Get in touch')


@mainRoutes.route('/login', methods=['GET'])
def login():
    return render_template('main/login.html', title='Login')

@mainRoutes.route('/search', methods=['GET'])
def search():
    return render_template('main/search.html')