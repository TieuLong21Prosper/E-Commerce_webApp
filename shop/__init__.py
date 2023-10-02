from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, UploadSet
import os

# create the extension
# create the app
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myshop.db"
app.config['SECRET_KEY'] = 'fdsui23eufsd3439rfhds' 
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(base_dir, 'static/images')
photos = UploadSet('photos', IMAGES)
media = UploadSet('media', default_dest=lambda app: app.instance_path)
configure_uploads(app, (photos, media))
db = SQLAlchemy(app)
migrate = Migrate(app,db)
bcrypt = Bcrypt(app)


from shop.admin import routes,models
from shop.products import routes,models
from shop.Navigate_site import routes