from flask import request, jsonify, current_app, url_for
from .errorController import AppError
from ..models.postModel import Post
from flask_jwt_extended import current_user
from datetime import datetime
from ..utils.helperFuncs import saveImageFiles, setPostOperation
from ..utils.imageScraping import textToHtmlParser


def createOne():
    data = request.form.to_dict()

    if 'category' in data.keys():
        data['category'] = data['category'].split(',') if ',' in data['category'] else [data['category']]
    
    data = Post.filterData(data)
    if request.files:
        data['coverImage']=saveImageFiles(request.files.getlist('coverImage'), resize=(800, 0.6*800))

    data['text']=textToHtmlParser(data['text'])

    if 'coverImage' in data.keys():
        if data['coverImage']=='_DELETE':
            del data['coverImage'] 

    data['author'] = current_user._id
    data['authorName'] = current_user.name

    post = Post(data)
    post.save(pre_hooks=[post.slugify])

    return jsonify({
        'status': 'success',
        'data': [vars(post)],
        'message': 'Post created successfully.'
    })


def updateOne(postId):
    post = Post.findOne({'_id': postId})

    if((current_user._id != post.author) and (current_user.role != 'admin')):
        return AppError('This is not your post.', 401)

    data = Post.filterData(request.form.to_dict())

    if 'category' in data.keys():
        data['category'] = data['category'].split(',') if ',' in data['category'] else [data['category']]
    
    if request.files:
        data['coverImage']=saveImageFiles(request.files.getlist('coverImage'), resize=(800, 0.38*500))
    
    data['dateEdited'] = datetime.utcnow().strftime('%d-%m-%Y %H:%M')
    
    data['text']=textToHtmlParser(data['text'])

    operation = setPostOperation(data)
    post.update(operation)
    
    return jsonify({
        'status': 'success',
        'data': [vars(post)],
        'message': 'Post updated successfully'
    })