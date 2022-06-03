
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash,session,url_for
from sqlalchemy import DateTime
from flask_mail import Mail
import json
import datetime

with open('config.json','r')as c:
    test=json.load(c)["test"]
local_server=True

app = Flask(__name__)
app.secret_key = 'kirtiverma'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SLL=True,
    MAIL_USERNAME=test['gmail_user'],
    MAIL_PASSWORD=test['gmail_password'],
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True
)
mail=Mail(app)


if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] =test["local_uri"]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Contacts(db.Model):

    id=db.Column(db.Integer, primary_key=True)
    created_date = db.Column(DateTime,default=datetime.datetime.utcnow)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(12))
    message= db.Column(db.String(120), nullable=False)
class Posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(70),nullable=False)
    tagline=db.Column(db.String(70),nullable=True)
    content=db.Column(db.String(100),nullable=False)
    created_date = db.Column(db.String(12), nullable=True)
    slug=db.Column(db.String(80),nullable=False)
    img_file=db.Column(db.String(30),nullable=False)

@app.route("/")
def home():
    posts=Posts.query.filter_by().all()[0:test['blogs_no']]
    return render_template('index.html',test=test,posts=posts)
@app.route("/about")
def about():
    return render_template('about.html',test=test)
@app.route("/dashboard", methods = ['GET', 'POST'])
def dashboard():

    if ('user' in session and session['user']==test['admin_user']):
        posts = Posts.query.all()
        return render_template("dashboard.html",test=test,posts=posts)
    if (request.method =='POST'):

       username=request.form.get('uname')
       userpass=request.form.get('pass')

       if (username==test['admin_user'] and userpass==test["admin_password"]):

           session['user']= username
           posts = Posts.query.all()
           return render_template('dashboard.html',test=test,posts=posts)
    return render_template('login.html',test=test)

@app.route("/post/<string:post_slug>",methods=['get'])
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()

    return render_template('post.html',post=post,test=test)

@app.route("/edit/<string:id>",methods=['GET','POST'])
def edit(id):
    if('user' in session and session['user']==test['admin_user']):
        if(request.method=='POST'):
            box_title=request.form.get('title')
            tagline=request.form.get('tagline')
            slug=request.form.get('slug')
            content=request.form.get('content')
            img_file=request.form.get('img_file')
            date=datetime.now()
            if id =='0':
                post=Posts(title=box_title,tagline=tagline,content=content,slug=slug,img_file=img_file,created_date=date)
                db.session.add(post)
                db.session.commit()
    return  render_template('edit.html',test=test,id=id)






@app.route("/contact",methods=['GET','POST'])
def contact():
    if (request.method == 'POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        contact = Contacts.query.with_entities(Contacts.phone).filter(Contacts.phone == phone).first()
        if not contact:
            obj_contact=Contacts()
            obj_contact.name=name
            obj_contact.email=email
            obj_contact.phone=phone
            obj_contact.message=message
            db.session.add(obj_contact)
            db.session.commit()
            mail.send_message('messsage from blog'+obj_contact.name,
                              sender=obj_contact.email,
                              recipients=[test['gmail_user']],
                              body=obj_contact.message+"\n"+obj_contact.phone)
            flash('form succesfully submitted',"success")
            return render_template('contact.html',test=test)
        else:
            flash('This phone no. is already use, Please update or use other no.',"danger")
            return render_template('contact.html', test=test)

    else:

        return render_template('contact.html', test=test)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5001)
