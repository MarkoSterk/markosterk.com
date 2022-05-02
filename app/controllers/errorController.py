from flask import abort, jsonify, render_template
from werkzeug.exceptions import HTTPException

"""
Error handling controllers.

AppError <- controller for raising/returning predictable app errors

handle_error: overrides the default error responses for all exception codes.
"""

##function for raising exceptions when needed.
def AppError(msg, statusCode):
    response = jsonify({
        'status': 'error',
        'message': msg,
        'code': statusCode
        })
    return response, statusCode


###function for exception handling
def handle_error(err):
    code = 500
    if isinstance(err, HTTPException):
        code = err.code
        description = err.description
    
    if code == 500:
        description('An error occured. Please come back later. We are sorry.')
    
    error={
        'status': 'error',
        'message': description,
        'code': code
    }
    return render_template('errors/error_page.html', error=error, title='Error')
    # return jsonify({
    #     'status': 'error',
    #     'message': description,
    #     'code': code
    # }), code   