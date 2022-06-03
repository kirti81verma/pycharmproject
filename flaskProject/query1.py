from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:root12345@localhost:3306/test4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(100))
    date=db.Column(db.Date,default=datetime.utcnow)

test=User(name='SOi',email='kkkkkkkkk@gmail.com')
a=User.query.all()
for i in a:
    print(i.name,i.email,i.date)
print(User.query.count())
print(User.query.filter_by(name='kirti').all())
db.session.add(test)
db.session.commit()


db.create_all()
