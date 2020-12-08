from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from datetime import datetime as dt
import os, base64
from werkzeug.security import (generate_password_hash, check_password_hash)
from flask_gravatar import Gravatar
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail, Message
from filters import read_datetime

from flask_wtf import CSRFProtect


app = Flask(__name__)

csrf = CSRFProtect(app)

app.jinja_env.filters["read_datetime"] = read_datetime


gravatar = Gravatar(app,
                    size = 100,
                    rating = "g",
                    default = "retro",
                    force_default = False,
                    force_lower = False,
                    use_ssl= False,
                    base_url=None)

mail_settings = {
    
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USER_SSL": False,
    "MAIL_USERNAME": "dummyemail2019test1@gmail.com",
    "MAIL_PASSWORD": "123dummy123",
}


app.config.update(mail_settings)
mail = Mail(app)


# file_path = os.path.abspath(os.getcwd()) + "\database.db"

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + file_path

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://qydsslidyyppsi:8cb1a4405fc248fd3e247e0009c1976c4132f91b4467246dbe29c5931b9cd539@ec2-52-208-138-246.eu-west-1.compute.amazonaws.com:5432/dcs0iiilrb05ov"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'I\x94\x90\xdf\x15\x88\x1e\xb2\xa2\xa9-k\x93\xdf\\\xaa\xa5\xa2\xedQ\xc08\xaa""Q\xc0\xd0r\x15\x1c\x8c\x80\xc5Ik$\x10\xf3\x06'

db = SQLAlchemy(app)

migrate = Migrate(app, db)


with app.app_context():
    
    
    if db.engine.url.drivername == "sqlite":
        
        migrate.init_app(app, db, render_as_batch = True)
        
    else:
        
        migrate.init_app(app, db)
        
        




        
class User(db.Model, UserMixin):
    
    
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40))
    email = db.Column(db.String(35), unique=True)
    password = db.Column(db.String(128))
    confirm_password = db.Column(db.String(20))
    timestamp = db.Column(db.String(40))
    
    online = db.Column(db.Boolean, default = False)
    login_count = db.Column(db.Integer, default = 0)
    
    description = db.Column(db.Text)
    
    is_admin = db.Column(db.Boolean, default = False)
    
    
    ######## RELATIONSHIPS ########################################
    blogs = db.relationship("Blog", backref="user", lazy="dynamic")
    comments = db.relationship("Comment", backref="user", lazy="dynamic")
    replies = db.relationship("Reply", backref="user", lazy="dynamic")
    notifications = db.relationship("Notification", backref="user", lazy="dynamic")
    
    user_image = db.relationship("UserImage", backref="user", uselist = False)
    
    role = db.relationship("AdminRole", backref="user", uselist = False)
    
    
    
    def __init__(self, username, email, password, confirm_password):
        
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.confirm_password = confirm_password
        self.online = False
        self.login_count = 0
        self.timestamp = dt.strftime(dt.now(), "%Y/%m/%d %H:%M:%S")
        self.description = None
        self.is_admin = False
        
    def get_image(self):
        
        if self.user_image is None:
            
            pic = gravatar(self.email)
            
        else:
            
            file_name_type = self.user_image.file_name.split(".")[1]
            
            bytes_pic = self.user_image.picture
            
            if file_name_type == "png":
                
                file_type_base = "data:image/png;base64,"
                
            elif file_name_type == "jpeg":
                 file_type_base = "data/:image/jpeg;base64," 
                
            elif file_name_type == "jpg":
                
                 file_type_base = "data:image/jpg;base64," 
                
            elif file_name_type == "gif":
                
                 file_type_base = "data:image/gif;base64,"
                
            
            pic = file_type_base + base64.b64encode(bytes_pic).decode("utf-8")
            
        
        return pic
        
        
    def checking_password(self, check_password):
        
        return check_password_hash(self.password, check_password)
    
    
    def logged_in(self):
        
        self.online = True
        self.login_count += 1
        db.session.commit()
        print("LOGGED IN!!")
        
        
    def logged_out(self):
        
        self.online = False
        db.session.commit()
        print("LOGGED OUT!!")
        
        
        
        
    def get_reset_token(self, expires_sec = 3600):
        
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")
    
    def verify_reset_token(token):
        
        s = Serializer(app.config["SECRET_KEY"])
        try:
            
            user_id = s.loads(token)["user_id"]
            
        except:
            
            return None
        
        return User.query.get(int(user_id))
        
    def __repr__(self):
        
        
        return "<User {}, ID {}>".format(*[self.username, self.id])
    
    
    
    
    
class AdminRole(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    role = db.Column(db.String(40))
    timestamp = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    def __init__(self, role, user_id):
        
        self.role = role
        self.user_id = user_id
        self.timestamp = dt.strftime(dt.now(), "%Y/%m/%d %H:%M:%S")
        

        
    def __repr__(self):
        
        
        return "<AdminRole {}, ID {}>".format(*[self.user_id, self.id])
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    data = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.String(40))
    
    comments = db.relationship("Comment", backref="blog", lazy="dynamic")
    
    def __init__(self, title, data, user_id):
        
        self.title = title
        self.data = data
        self.user_id = user_id
        self.timestamp = dt.strftime(dt.now(), "%Y/%m/%d %H:%M:%S")
        
        
        
    def count_comments(self):
        
        count = 0

        for comm in self.comments.all():

            rep_value = comm.replies.count()

            count += rep_value

        total = count + self.comments.count()
        
        return total

        
    def __repr__(self):
        
        
        return "<Blog {}, userID {}>".format(*[self.id, self.user_id])
    
    
    
    
    
    

class Comment(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"))
    timestamp = db.Column(db.String(40))
    
    replies = db.relationship("Reply", backref="comment", lazy="dynamic")
    
    def __init__(self, comment, blog_id, user_id):
        
        self.comment = comment
        self.blog_id = blog_id
        self.user_id = user_id
        self.timestamp = dt.strftime(dt.now(), "%Y/%m/%d %H:%M:%S")

        
    def __repr__(self):
        
        
        return "<Comment {}, blogID {}, userID {}>".format(*[self.id, self.blog_id, self.user_id])
    
    
    
    
    

class Reply(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    reply = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comment_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    timestamp = db.Column(db.String(40))
    
    
    
    def __init__(self, reply, comment_id, user_id):
        
        self.reply = reply
        self.comment_id = comment_id
        self.user_id = user_id
        self.timestamp = dt.strftime(dt.now(), "%Y/%m/%d %H:%M:%S")

        
    def __repr__(self):
        
        
        return "<Reply {}, comID {}, userID {}>".format(*[self.id, self.comment_id, self.user_id])
    
    
    
    
           
class Notification(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    text_id = db.Column(db.Integer)
    text_type = db.Column(db.String(40)) ### REPLY, COMMENT, BLOG POST
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.String(40))
    bell = db.Column(db.Boolean, default = True)
    
    def __init__(self, text_type, text_id, user_id):
        
        self.text_type = text_type
        self.text_id = text_id
        self.user_id = user_id
        self.timestamp = dt.strftime(dt.now(), "%Y/%m/%d %H:%M:%S")
        self.bell = True

        
    def __repr__(self):
        
        
        return "<Notification {}, type {}, userID {}>".format(*[self.id, self.text_type, self.user_id])
    
    
    

           
           
           
           
           
           
           
           
           
           
           
           
           
           
class UserImage(db.Model):
    
    
    id = db.Column(db.Integer, primary_key = True)
    file_name = db.Column(db.String(100))
    picture = db.Column(db.LargeBinary)
    timestamp = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    def __init__(self, file_name, picture, user_id):
        
        self.file_name = file_name
        self.picture = picture
        self.user_id = user_id
        self.timestamp = dt.strftime(dt.now(), "%Y/%m/%d %H:%M:%S")
        
        
    def __repr__(self):
        
        return "<UserImage {}, userID {}>".format(*[self.id, self.user_id])
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           












