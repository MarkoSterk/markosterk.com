from flask import jsonify, request
from flask_jwt_extended import current_user

from app.controllers.errorController import AppError

def getAll(Model):
    
    query = Model.findMany({})
    return jsonify({
        'status': 'success',
        'results': len(query),
        'data': [vars(q) for q in query],
        'message': 'Query completed successfully'
    }), 200


def getN(Model):
    if(request.args
        and 'from' in request.args.keys()
        and 'length' in request.args.keys()):
        queryData = request.args.to_dict()
        fromN = int(queryData['from'])
        toN = fromN + int(queryData['length'])
    else:
        return AppError('You must provide a from and length query argument', 400)
    
    orderDirection = int(request.args['orderBy']) if 'orderBy' in request.args.keys() else -1

    query = Model.findMany({ '$query': {}, '$orderby': { '_createdAt' : orderDirection } })[fromN:toN]
    return jsonify({
        'status': 'success',
        'results': len(query),
        'data': [vars(q) for q in query],
        'message': 'Query completed successfully'
    }), 200


def getOne(queryId, Model, populate=False, populateData = {}):
    query = Model.findOne({'_id': queryId})
    
    if populate:
        query.populate(populateData)
    
    return jsonify({
        'status': 'success',
        'data': [vars(query)],
        'message': 'Query completed successfully'
    }), 200


def deleteOne(queryId, Model):
    query = Model.findOne({'_id': queryId})

    if Model.__name__ == 'Post':
        if((current_user._id != query.author) and (current_user.role != 'admin')):
            return AppError('Not your post.', 401)
    if Model.__name__ == 'User':
        if((current_user._id != queryId) and (current_user.role == 'admin')):
            return AppError('This is not your profile.', 401)
    
    query.delete()
    return jsonify({
        'status': 'success',
        'data': None,
        'message': f'{Model.__name__} deleted successfully'
    }), 204


def searchByQueryString(Model):
    queryData=request.args.to_dict()
    queryObject = {}
    if len(queryData)!=0:
        queryObject = {
            '$or': [{key: {'$regex': queryData[key]}} for key in queryData.keys()]
        }
    
    queryObject['active']=True

    #print(queryObject)
    query = Model.findMany(queryObject)
    return jsonify({
        'status': 'success',
        'results': 0,
        'data': [vars(q) for q in query],
        'message': 'Query completed successfully.'
    })