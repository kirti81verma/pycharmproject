from flask import Flask,render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, desc, func,select, Column, Integer, String, DATETIME, ForeignKey,or_,and_
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:root12345@localhost:3306/test5"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Subject(db.Model):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key = True)
    name = Column(String(245))
    subject=Column(String(200))
@app.route("/subject",methods=["POST","GET"])
def sub():
    if (request.method == 'POST'):
        name=request.form.get("name")
        subject=request.form.get("sub")
        subs=Subject(name=name,subject=subject)
        db.session.add(subs)
        db.session.commit()
    return render_template("subject.html")

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,port=3000)





