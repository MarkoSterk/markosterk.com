import secrets
from PIL import Image
from io import BytesIO
from flask import current_app, url_for
from base64 import b64decode
import os
from bs4 import BeautifulSoup

def imgConverter(imgSrc, resize=False):
    try:
        ext='PNG'
        hexName=secrets.token_hex(16)
        filename=hexName+'.'+ext
        pathP=os.path.join(current_app.root_path, 'static/images/postImages', filename)

        im = Image.open(BytesIO(b64decode(imgSrc.split(',')[1])))
        if resize:
            im.thumbnail(resize)
        im.save(pathP)

        imgSrc=url_for('static', filename="images/postImages/" + filename)

        return imgSrc
    except:
        return imgSrc


def textToHtmlParser(text):
    soup = BeautifulSoup(text, "html.parser")
    for img in soup.find_all('img'):
        img['src']=imgConverter(img['src'])

    return str(soup)