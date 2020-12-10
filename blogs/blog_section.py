from flask import (Blueprint, render_template, url_for, redirect, flash, jsonify, request,
                   current_app)

### LOCAL IMPORTS ########################################################
from models import (db, app,  User, Blog, Comment, Reply, Notification, AdminRole)
from flask_login import (login_required, current_user)
import lorem

from flask_wtf import CSRFProtect

csrf = CSRFProtect(app)

current_app.config["blog_id"] = []



app_blog = Blueprint("blog_section", __name__, url_prefix = "/awesome_blog",
                     template_folder = "templates_blog")


@app_blog.route("/blogs/<int:page>")
def blogs(page=1):
    
    blogs = Blog.query.all()
    
    pages = 0
    
    if blogs != []:
        
        blogs = Blog.query.paginate(page, 4).items[::-1]
        paginate = Blog.query.paginate(page, 4)


        pages = list(paginate.iter_pages())
        
    
    
    return render_template("blogs.html", title = "blogs",
                           blogs = blogs,
                           pages = pages,
                           page = page)


@app_blog.route("/new_blog/<string:username>/<int:user_id>")
@login_required
def new_blog(username, user_id):
    
    
    return render_template("new_blog.html", title = "new_blog")



@app_blog.route("/one_blog/<int:blog_id>/<string:blog_title>")
def one_blog(blog_id, blog_title):
    
    
    blog = Blog.query.filter_by(id = blog_id).first()
    
    visitor = True
    blog_author_edit = False
    

    
    
    if blog is None:
        
        
        flash("This blog does not exist or has been deleted!", "info")
        return redirect(url_for("home"))
    
    
    print(current_app.config
    
    current_app.config["blog_id"].append(blog.id)
    
    if current_user.is_anonymous:
        
        current_user_id = 0
        
    else:
        
        current_user_id = current_user.id
        
        visitor = False
        
        
        if current_user.id == blog.user_id:
            
            blog_author_edit = True
        
        
    
    
    author =  blog.user
    
    blog_text = blog.data
    
    #     text = lorem.text()
    #     #text = lorem.text() + lorem.text() + lorem.text()

    #     blog_text = "<p>"

    #     for t in text.split(" "):

    #         if "\n" in t:

    #             blog_text += "</p>"

    #         else:

    #             blog_text += " "+ t



    
    
    return render_template("one_blog.html", title = "one blog",
                           blog = blog, 
                           blog_id = blog_id,
                           author = author,
                           blog_text = blog_text,
                           current_user_id = current_user_id,
                           visitor = visitor,
                           blog_author_edit = blog_author_edit)
                           



@app_blog.route("/blog_grid")
def blog_grid():
    
    blog = Blog.query.filter_by(id = 1).first()
    
    
    text = lorem.text()
    
    blog_text = "<p>"

    for t in text.split(" "):

        if "\n" in t:

            blog_text += "</p>"

        else:

            blog_text += " "+ t

    

    
    
    return render_template("blog_grid.html", title = "blog grid", 
                           blog = blog,
                           blog_text = blog_text)





@app_blog.route("/blog_grid3")
def blog_grid3():
    
    blog = Blog.query.filter_by(id = 1).first()
    
    
    text = lorem.text()
    
    blog_text = "<p>"

    for t in text.split(" "):

        if "\n" in t:

            blog_text += "</p>"

        else:

            blog_text += " "+ t

    
    return render_template("blog_grid3.html", title = "blog grid3", 
                           blog = blog,
                           blog_text = blog_text)













@app_blog.route("/blog_grid4")
def blog_grid4():
    
    blog = Blog.query.filter_by(id = 1).first()
    
    
    text = lorem.text() + lorem.text() + lorem.text()
    
    blog_text = "<p>"

    for t in text.split(" "):

        if "\n" in t:

            blog_text += "</p>"

        else:

            blog_text += " "+ t

    
    return render_template("blog_grid4.html", title = "blog grid4", 
                           blog = blog,
                           blog_text = blog_text)






@app_blog.route("/blog_grid5")
def blog_grid5():
    
    blog = Blog.query.filter_by(id = 1).first()
    
    
    text = lorem.text() + lorem.text() + lorem.text()
    
    blog_text = "<p>"

    for t in text.split(" "):

        if "\n" in t:

            blog_text += "</p>"

        else:

            blog_text += " "+ t

    
    return render_template("blog_grid5.html", title = "blog grid5", 
                           blog = blog,
                           blog_text = blog_text)





@app_blog.route("/blog_grid6")
def blog_grid6():
    
    blog = Blog.query.filter_by(id = 1).first()
    
    
    text = lorem.text() + lorem.text() + lorem.text()
    
    blog_text = "<p>"

    for t in text.split(" "):

        if "\n" in t:

            blog_text += "</p>"

        else:

            blog_text += " "+ t

    
    return render_template("blog_grid6.html", title = "blog grid6", 
                           blog = blog,
                           blog_text = blog_text)








@app_blog.route("/blog_grid7")
def blog_grid7():
    
    blog = Blog.query.filter_by(id = 1).first()
    
    
    text = lorem.text() + lorem.text() + lorem.text()
    
    blog_text = "<p>"

    for t in text.split(" "):

        if "\n" in t:

            blog_text += "</p>"

        else:

            blog_text += " "+ t

    
    return render_template("blog_grid7.html", title = "blog grid7", 
                           blog = blog,
                           blog_text = blog_text)








@app_blog.route("/blog_grid8")
def blog_grid8():
    
    blog = Blog.query.filter_by(id = 1).first()
    
    
    text = lorem.text() + lorem.text() + lorem.text()
    
    blog_text = "<p>"

    for t in text.split(" "):

        if "\n" in t:

            blog_text += "</p>"

        else:

            blog_text += " "+ t

    
    return render_template("blog_grid8.html", title = "blog grid8", 
                           blog = blog,
                           blog_text = blog_text)





@app_blog.route("/blog_grid9")
def blog_grid9():
    
    blog = Blog.query.filter_by(id = 1).first()
    
    
    text = lorem.text() + lorem.text() + lorem.text()
    
    blog_text = "<p>"

    for t in text.split(" "):

        if "\n" in t:

            blog_text += "</p>"

        else:

            blog_text += " "+ t

    
    return render_template("blog_grid9.html", title = "blog grid9", 
                           blog = blog,
                           blog_text = blog_text)






@app_blog.route("/blog_grid10")
def blog_grid10():
    
    blog = Blog.query.filter_by(id = 1).first()
    
    
    text = lorem.text() + lorem.text() + lorem.text()
    
    blog_text = "<p>"

    for t in text.split(" "):

        if "\n" in t:

            blog_text += "</p>"

        else:

            blog_text += " "+ t

    
    return render_template("blog_grid10.html", title = "blog grid10", 
                           blog = blog,
                           blog_text = blog_text)























@app_blog.route("/my_blogs")
def my_blogs():
    
    
    return render_template("my_blogs.html", title = "my blogs")


























