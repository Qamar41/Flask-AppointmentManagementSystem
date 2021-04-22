from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_restful import Resource, Api
import os
from flask_migrate import Migrate


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}



app=Flask(__name__)
api = Api(app)

db=SQLAlchemy(app=app,metadata=MetaData(naming_convention=naming_convention))

migrate = Migrate(app, db,render_as_batch=True)


# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:1234@localhost/appointment_relation'
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://spaceos:spaceos@localhost/todorelations'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


app.config['SECRET_KEY']='somesecret'

# Configuring Database Uri

base_dir=os.path.abspath(os.path.dirname(__file__))


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(base_dir , 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False




from application import routes