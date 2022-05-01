from app import bcrypt
import secrets
from flask import current_app
import os
from PIL import Image

"""
Helper functions which can be used across the app. 

hashUrlSafe: creates a URL safe hashed string

saveImageFiles: saves image files from a form into the static folder and asignes
random string names (it keeps the provided extension) but it only accepts provided
image formats (allowed_formats). Default: allowed_formats=['png', 'jpg', 'jpeg', 'bmp']
"""

def hashUrlSafe(stringToHash):
    hashed_string = '/'
    while True:
        if '/' in hashed_string:
            hashed_string = bcrypt.generate_password_hash(str(stringToHash)).decode('utf-8')
        else:
            break
        
    return hashed_string


def saveImageFiles(files, resize = False, allowed_formats=['png', 'jpg', 'jpeg', 'bmp']):
    fileNames = []
    for file in files:
        ext = file.filename.split('.')[-1]
        if ext in allowed_formats:
            #fileName = secure_filename(file.filename)
            fileName = secrets.token_hex(16) + '.' + ext
            filePath=os.path.join(current_app.root_path, 'static', 'images', 'covers', fileName)

            if resize!=False:
                file = Image.open(file)
                file.thumbnail(resize)

            file.save(filePath)
            fileNames.append(fileName)
    return fileNames

def setPostOperation(data):
    operation={}
    if 'coverImage' in data.keys():
        if data['coverImage'] == '_DELETE':
            del data['coverImage']
            operation = {'$set': data,
                        '$unset': {'coverImage': ''}}
        else:
            operation = {'$set': data}
    else:
        operation = {'$set': data}
    
    return operation