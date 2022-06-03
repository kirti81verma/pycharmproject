from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:root12345@localhost:3306/code1"
app.config['SQLALCHEMY_BINDS']={'two':'mysql+pymysql://root:root12345@localhost:3306/code2',
                                'second':'mysql+pymysql://root:root12345@localhost:3306/code3'}
db=SQLAlchemy(app)
class One(db.Model):
    id=db.Column(db.Integer,primary_key=True)
class Two(db.Model):
    __bind_key__='two'
    id=db.Column(db.Integer,primary_key=True)
class Three(db.Model):
    __bind_key__='second'
    id=db.Column(db.Integer,primary_key=True)
# @app.route('/')
# def index():
#     second=Two(id=20)
#     db.session.add(second)
#     db.session.commit()
#     return 'added value in second table'
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)



