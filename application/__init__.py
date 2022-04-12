from flask import Flask, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = "Aliev@123321asSs"




from application import models
from application import routes

def create_db():
    with app.app_context():
        db.create_all()

# create_db()
