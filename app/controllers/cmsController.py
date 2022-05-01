from flask import request, jsonify
from ..utils.email import sendContactEmail

def sendContactForm():
    contactData = request.get_json()
    print(contactData)
    sendContactEmail(contactData['message'], contactData['email'], contactData['name'], contactData['surname'])

    return jsonify({
        'status': 'success',
        'message': 'Contact form submited successfully'
    }), 200