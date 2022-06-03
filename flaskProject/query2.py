from flask import Flask,render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, desc, func,select, Column, Integer, String, DATETIME, ForeignKey,or_,and_
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:root12345@localhost:3306/test5"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Auth(db.Model):
    __tablename__ = 'auth'
    id = Column(Integer, primary_key = True)
    email = Column(String(245))
    pwd = Column(String(245))
    company_id = Column(Integer)
    student = db.relationship('Student', back_populates='auth')
    teacher = db.relationship('Teacher', back_populates='auth')


class Student(db.Model):
    __tablename__ = 'student'
    id = Column(Integer, primary_key = True)
    name =Column(String(245))
    phone = Column(String(245))
    auth_id = Column(db.ForeignKey('auth.id'))
    auth = db.relationship('Auth', foreign_keys=[auth_id], back_populates = 'student')


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key = True)
    name = Column(String(245))
    phone = Column(String(245))
    auth_id = Column(db.ForeignKey('auth.id'))
    auth = db.relationship('Auth', foreign_keys=[auth_id], back_populates='teacher')




@app.route("/student", methods=['POST','GET'])
def student():
    if(request.method=='POST'):
        email=request.form.get('email')
        password=request.form.get('pwd')
        compId=request.form.get('compId')
        name = request.form.get('name')
        phone=request.form.get('phone')

        auths=Auth(email=email,pwd=password,company_id=compId)
        db.session.add(auths)
        db.session.commit()
        # print(func.concat(auths.email,'',auths.pwd))

        auth_ids = auths.id
        if auth_ids:
            students = Student(name=name, auth_id = auth_ids,phone=phone)
            db.session.add(students)
            db.session.commit()
            data = Student.query.with_entities(func.concat(Student.name, '-', Student.auth_id)).first()
            print(data)
            data1=Student.query.filter(Student.id >2)
            for i in data1:
                print(i.name)
            data2 =Student.query.filter(Student.name.ilike("k%")).all()
            # data3 =Student.query.filter(Student.name.match)
            print("name starting with k")
            for i in data2:
                print("name starting with k",i.name)
            data5=Student.query.filter(Student.id.in_([1,10]))
            for i in data5:
                print(i.name)
            data4=Student.query.filter(and_(Student.id>2,Student.name.ilike("k%")))
            print("and")
            for i in data4:
                print("and",i.name)
            data4 = Student.query.filter(or_(Student.id > 2, Student.name.ilike("k%")))
            print("or")
            for i in data4:
                print(i.name)
            data5=Student.query.filter(or_(Student.id > 2, Student.name.ilike("k%"))).order_by(desc(Student.name))
            print("oderby")
            for i in data5:
               print(i.name)



            return render_template('student.html')






    else:
        data = Student.query.with_entities(func.concat(Student.name,'-',Student.auth_id)).first()
        print(data)
        test=Auth.query.join(Student).filter(Student.auth_id==Auth.id)
        for i in test:
            print(i.pwd)
        print("gchcjhvkblnl,nknlnkbkvhjmjvjv")
        dd = Auth.query.join(Student, Student.auth_id == Auth.id).all()
        for i in dd:
            print(i.pwd)

        return render_template('student.html')



@app.route("/teacher", methods=['POST','GET'])
def teacher():
    if( request.method=='POST'):
        email = request.form.get('email')
        password = request.form.get('pwd')
        compId = request.form.get('compId')
        name = request.form.get('name')
        phone = request.form.get('phone')

        auths=Auth(email=email,pwd=password,company_id=compId)

        db.session.add(auths)
        db.session.commit()

        auth_id=auths.id
        if auth_id:
            teacher=Teacher(name=name,phone=phone,auth_id=auth_id)
            db.session.add(teacher)
            db.session.commit()

    return render_template('teacher.html')
@app.route('/auth')
def auth():
    student=Student.query.all()
    teacher=Teacher.query.all()
    auth=Auth.query.all()

    return render_template("auth.html",students=student,teachers=teacher,auths=auth)



# @app.route("/student",methods=['POST','GET'])
# def student():
#     if(request.method =='POST'):
#         name=request.form.get('name')
#         phone=request.form.get('phone')
#         auth_id=request.form.get('authid')
#         stud=Student(name=name,phone=phone,auth_id=auth_id)
#         db.session.add(stud)
#         db.session.commit()
#     return render_template('student.html')








if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,port=3000)



