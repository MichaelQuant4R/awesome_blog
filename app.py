from flask import (render_template, url_for, redirect, flash, jsonify, request, current_app, session)

### LOCAL IMPORTS ########################################################
from models import (db, app, mail, Message,  User, Blog, Comment,
                    Reply, Notification, AdminRole,
                    UserImage)
from forms import (RegisterForm, LoginForm, RequestTokenForm, ResetPasswordForm)
from flask_login import (LoginManager, login_user, login_required, logout_user, current_user)


from blogs.blog_section import app_blog
from comments.comment_section import app_comm
from notify.notify_section import app_bell

from config import allowed_extensions, max_file_size, header
import sys
from admin_section import admin

app.register_blueprint(app_blog)
app.register_blueprint(app_comm)
app.register_blueprint(app_bell)

# app.config.update(
#     SESSION_COOKIE_SECURE=True,
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE='Lax',
# )





@app.before_first_request
def before_first_request_func():
    print("This function will run once")

    session["blog_id"] = []
    


@app.context_processor
def inject_stage_and_region():
    return dict(header=header)


login_manager = LoginManager(app)
login_manager.login_view = "login" ### refers to the login view function, we use login_user(user)

@login_manager.user_loader
def load_user(user_id):
    
    return User.query.get(int(user_id))



@app.route("/")
@app.route("/home")
def home():
    
    
    blogs = Blog.query.all()
    

    if blogs != []:
        
        blogs = Blog.query.all()[::-1][:5]

    
    
    return render_template("home.html", title = "home",
                           blogs = blogs)
                           

    
    
    




@app.route("/register", methods = ["GET", "POST"])
def register():
    
    # if not true
    if current_user.is_authenticated:
        
        flash("You're already logged in", "info")
        return redirect(url_for("home"))
    
    form = RegisterForm()
    
    # True or False
    if form.validate_on_submit():
        
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
        
        check_user = User.query.filter_by(email = email).first()
        
        
        if check_user is None:
            
            
            user = User(username, email, password, confirm_password)
            db.session.add(user)
            db.session.commit()
            
            flash("Thanks for registering", "success")
            return redirect(url_for("login"))
        
        
        else:
            
            print("You've already registered!!")
            flash("You're already registered with this email", "warning")
            return redirect(url_for("login"))
            
            
            

    
    
    return render_template("register.html", title = "register", 
                           form = form)



@app.route("/login", methods = ["GET", "POST"])
def login():
    
    # if not true
    if current_user.is_authenticated:
        
        flash("You're already logged in", "info")
        return redirect(url_for("home"))
    
    form = LoginForm()
        
    # True or False
    if form.validate_on_submit():
       
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email = email).first()
        
        if user is not None:
            
            if user.checking_password(password):
                
                login_user(user)
                user.logged_in()
                
                if user.is_admin:

                    
                    session["PROFILE_LINK"] = "/profile/" + user.username + "/" + str(user.id)
                    session["ADMIN_NAME"] = user.username.title()
                    
                    
                print(session)
            
                flash("You've successfully logged in", "success")
                return redirect(url_for("profile", username = user.username, user_id = user.id))
            
            
            else:
                
                            
                print("This user does not exist!!")
                flash("Incorrect email and/or password", "danger")
                return render_template("login.html", title = "login", 
                           form = form)


        else:
            
            print("This user does not exist!!")
            flash("Incorrect email and/or password", "danger")
            return render_template("login.html", title = "login", 
                           form = form)

    
    return render_template("login.html", title = "login", 
                           form = form)



@app.route("/profile/<string:username>/<int:user_id>", methods = ["GET", "POST"])
@login_required
def profile(username, user_id):
    
    
    
    user_load_image = True
    describe = False
    
    user = User.query.filter_by(id = user_id).first()
    
    if user is None:
        
        flash("This user does not exist!", "warning")
        return redirect(url_for("home"))
    
    if user.description is not None:
        
        describe = True
    
    if current_user.id != user_id:
        
        user_load_image = False
        

    return render_template("profile.html", title = "profile",
                           user_load_image = user_load_image,
                           user = user, 
                           describe =describe)





@app.route("/upload_user_text", methods = ["GET", "POST"])
@login_required
def upload_user_text():
    
        
    if request.method == "POST":

        text = request.form.get("description")
        
        
        current_user.description = text
        db.session.commit()
        
       
        flash("You've updated your descripion", "info")
        return redirect(url_for("profile", username=current_user.username, user_id = current_user.id))





































@app.route("/upload_user_image", methods = ["GET", "POST"])
@login_required
def upload_user_image():
    
        
    if request.method == "POST":

        file = request.files["image"]
        
        print("FILE!")
        print(file)
        print(file.filename)
        
#         image = file.read()
        
        check_image = file.filename.split(".")[1] # png, jpg, jpeg, gif
        
        if check_image not in allowed_extensions:
            
            
            flash("Extension not allowed. Only .png, .jpg, .jpeg, or .gif is allowed", "warning")
            return redirect(url_for("profile", username=current_user.username, user_id = current_user.id))
        
        else:
        
            print([i for i in dir(file) if "__" not in i])
            
            print(file.content_length)
            
            image = file.read()
            
            file_size = sys.getsizeof(image)
            print("FILE SIZE", file_size)
            
            if file_size <= max_file_size:
            
                user_image = UserImage(file.filename, image, current_user.id)
                db.session.add(user_image)
                db.session.commit()
                
                
                flash("You've uploaded an image", "success")
                return redirect(url_for("profile", username=current_user.username, user_id = current_user.id))

            else:

                flash("File size is too large. Max file size is 15MB", "warning")
                return rredirect(url_for("profile", username=current_user.username, user_id = current_user.id))




@app.route("/logout")
@login_required
def logout():
    
    
    current_user.logged_out()
    logout_user()
    
    flash("You've logged out", "info")
    return redirect(url_for("home"))




















@app.route("/contact")
def contact():
    
    return render_template("contact.html", title = "contact")





################### RESET PASSWORD ##############################################################
#################################################################################################



@app.route("/request_token", methods = ["GET", "POST"])
def request_token():
    
    form = RequestTokenForm()
    
    if form.validate_on_submit():
        
        
        email = form.email.data
        
        user = User.query.filter_by(email = email).first()
        
        if user is None:
            
            flash("This email does not exist!", "danger")
            return redirect(url_for("home"))
        
        else:
            
            token = user.get_reset_token()
            print(email, user)
            print(token)
            
            send_reset_password_email(email, token)
            
            flash("You've been emailed a token to reset your password", "info")
            return redirect(url_for("home"))
    
    return render_template("request_token.html", title = "request_token",
                           form = form)


@app.route("/reset_password/<string:token>", methods = ["GET", "POST"])
def reset_password(token):
    
    form = ResetPasswordForm()
    
    if current_user.is_authenticated:
        
        return redirect(url_for("home"))
    
    user = User.verify_reset_token(token)
    if user is None:
        
        flash("Invalid or expired token", "danger")
        return redirect(url_for("request_token"))
    
    if form.validate_on_submit():
        new_password = form.password.data
        confirm_password = form.confirm_password.data
        hashed_password = generate_password_hash(new_password)
        user.password = hashed_password
        user.confirm_password = confirm_password
        db.session.commit()
        
        flash("Your password has been updated", "success")
        return redirect(url_for("login"))
        
    
    return render_template("reset_password.html", title = "reset_password",
                             form = form)




            
            






def send_reset_password_email(email, token):
    

        html_reset_password= """<!DOCTYPE html>
        <html>
        <head>
            <title></title>
            </head>
            <body style='background-color:lightblue;'>

            <h1><em>My Awesome Blog</em></h1>
            <img src='cid:blog-logo.png' height = '100px' width = '120px'><br>

            <p>Dear awesome person, we've provided you with a temporary link where you can reset your password.</p><br>
            <p>The link is valid for <strong>1 hour</strong>.</p>


        <br>


        <div><a href='https://mikes-awesome-blog.herokuapp.com/reset_password/""" + token + """'> Click here to reset password</a></div>

        </body>
        </html>"""


        #HTML(html_reset_password)


              
        
        
        msg = Message(subject = "Reset Password: My Awesome Blog",
                      sender = app.config.get("MAIL_USERNAME"),
                      recipients = ["Student", email],
                      body = "Reset Password",
                      html = html_reset_password)
        
        msg.attach("blog-logo.png", "image/png",
                   open("blog-logo.png", "rb").read(), "inline",
                   headers = [["Content-ID", "<blog-logo.png>"], ])
        
        print(Message)
        print(type(html_reset_password))
        print(type(Message))
     
        
        print("Email has been sent for resetting password!")
        
        print(type(msg))
        print(msg)
        mail.send(msg)

        return "Email sent!"





















################################################################################################


@app.errorhandler(404)
def not_found(e):
    
    return render_template("not_found.html", title = "not found"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('internal_server_error.html', title = "internal server error 500"), 500


@app.errorhandler(403)
def page_forbidden(e):
    return render_template('forbidden.html', title = "page forbidden"), 403






#################################################################################################





@app.route("/test_layout")
def test_layout():
    
    
    return render_template("test_layout.html", title = "test layout")
































































if __name__ == "__main__":
    app.run(debug = False, threaded=True)
