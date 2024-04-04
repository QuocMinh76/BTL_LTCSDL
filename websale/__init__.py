from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary


app = Flask(__name__)
app.secret_key = '^&%@$#!^jdfhei4kdivjfpwsog2343rwef'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/websale?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 8

db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name = 'dhhpxhskj',
    api_key = '398599846358987',
    api_secret = 'jNqe-OCxgo98G-K6_OAL0nuvyEk'
)

login = LoginManager(app=app)