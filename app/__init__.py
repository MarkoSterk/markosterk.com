from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_compress import Compress
from flask_share import Share
from werkzeug.exceptions import default_exceptions
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail_sendgrid import MailSendGrid
from flask_jwt_extended import JWTManager

from app.config import Config
from .controllers import errorController

"""
Main entry point of the app. 
It needs a Config object which is located in the same folder (config.py)
"""
mongo = PyMongo() ##instance of the flask_pymongo PyMongo object for db connection
bcrypt = Bcrypt() ##creates Bcrypt instance for passord hashing
jwt = JWTManager() ##creates JSON Web Token Manager instance for authentication
mail = MailSendGrid() ##creates sendgrid instance for sending of emails
cors = CORS() #creates CORS instance for x-site resource sharing (protection)
compress = Compress() #extension for compressed responses
share = Share() #extension for social media sharing

def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(config_class)
    
    ##registers/initializes all extensions 
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    compress.init_app(app)
    share.init_app(app)

    #limiter - prevents flooding of the app with requests
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["400 per day", "200 per hour"]
    )

    ##registers blueprints
    from .routes.main.mainRoutes import mainRoutes
    app.register_blueprint(mainRoutes)

    from .routes.user.userRoutes import userRoutes
    app.register_blueprint(userRoutes)

    from .routes.post.postRoutes import postRoutes
    app.register_blueprint(postRoutes)

    from .routes.cms.cmsRoutes import cmsRoutes
    app.register_blueprint(cmsRoutes)

    ##override the default exception responses and replace them with handle_error
    for ex in default_exceptions:
        app.register_error_handler(ex, errorController.handle_error)

    ##sets the maximum hourly request rate from one IP
    ##to the userRoutes and houseRoutes
    limiter.limit("200/hour")(mainRoutes)
    

    return app
    
    
