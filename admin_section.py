##################### FLASK ADMIN ##############################################
from flask_admin import (Admin,  BaseView, expose, AdminIndexView)
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.menu import MenuLink
###############################################################################

from flask_login import (current_user, login_required, logout_user)
from flask import (render_template, redirect, url_for, jsonify, 
                   request, flash, abort, Response, current_app, 
                   session)


################# MODELS #######################################################
from models import (db, app, User, AdminRole, Blog, Comment, Reply)
from config import admin_theme

global admin_info
admin_info = {"profile_link": None, "admin_name": None}
import os

app.config["FLASK_ADMIN_SWATCH"] = admin_theme
# THEMES = cosmos darkly cyborg default flatly simplex yeti readable sandstone lumen paper



class MyAdmin(FileAdmin):
    
    allowed_extensions = ("jpg", "jpeg", "png", "gif")
    editable_extensions = ("txt", "py", "html", "css", "js")
    
    
    def is_accessible(self):
        
        
        if current_user.is_anonymous:
            
            flash("You do not have permission!", "danger")
            return abort(404)
        
        
        else:
            
            if current_user.is_admin:
            
                if current_user.role.role == "super-admin":
           
                    return True
                
                else:
                    
                    return False
            
            else:
                
                flash("User does not have permission!", "danger")
                abort(404)
                
                
                
class LogoutMenuLink(MenuLink):
    
    def is_accessible(self):
        return current_user.is_authenticated == True and current_user.is_admin == True
    
    
class UserIconLink(MenuLink):
    
    def is_accessible(self):
        return current_user.is_authenticated == True and current_user.is_admin == True
    
    
    
    
class MyHomeView(AdminIndexView):
    
        
    def is_accessible(self):
        if current_user.is_anonymous:
            
            flash("You do not have permission!", "danger")
            return abort(404)
        
        else:
            
            if current_user.is_admin:
            
                if current_user.role.role == "super-admin" or current_user.role.role == "admin-member":
                    
                        print("SESSION!!!!")
                        print(session)
                        
                        admin_info["profile_link"] = session["PROFILE_LINK"]
                        admin_info["admin_name"] = session["ADMIN_NAME"]
                        
                        print("ADMIN INFO")
                        
                        print(admin_info)

                        return True
                
                else:
                    
                    return False
            
            else:
                
                flash("User does not have permission!", "danger")
                abort(404)
                
                
                
                
    @expose("/")
    def index(self):


        return self.render("admin/admin_home.html", title = "admin home")
                
        

class MyView(BaseView):
    
    
    def is_accessible(self):
        
        if current_user.is_authenticated:
            
            if current_user.is_admin:
                
                return True
                
            else:
                    
                return False
        else:
            
            return redirect(url_for("home"))
    
    
    @expose('/')
    def test1(self):
        return self.render('admin/test1.html', title = "test 1")
    

class MyView2(BaseView):
    
    def is_accessible(self):
        
        if current_user.is_authenticated:
            
            if current_user.is_admin:
                
                return True
                
                
            else:
                    
                return False
                
        else:
            
            return redirect(url_for("home"))
    
    
    @expose('/')
    def test2(self):
        return self.render('admin/test2.html', title = "test 2")
    

class MyView3(BaseView):
    
    def is_accessible(self):
        
        if current_user.is_authenticated:
            
            if current_user.is_admin:
                
                return True
                
            else:
                    
                return False
        else:
            
            return redirect(url_for("home"))
    
    @expose('/')
    def test3(self):
        return self.render('admin/test3.html', title = "test 3")
    
        
        
      
        
        
        
        
        
        
    
class MyModelView(ModelView):
    
    column_exclude_list = ("password", "confirm_password", "data", "description")
    
    def render(self, template, **kwargs):
        
#         self.extra_js = [url_for("static", filename="js/custom_admin_page.js")]
#         self.extra_css = [url_for("static", filename="css/custom_admin_page.css")]
        
        
        return super(MyModelView, self).render(template, **kwargs)
    
    
    def is_accessible(self):
        
        if current_user.is_authenticated:
            
            if current_user.is_admin:
   
                    return True
                
           
            else:
                
                print("NO 1")
                flash("You do not have permission!", "danger")
                return abort(404)
                
        else:
            
            print("NO 2")
            flash("You do not have permission!", "danger")
            return abort(404)
        
        
    def not_auth(self):
        
        print("NO AUTHORIZED!")
        return abort(404)
    

        
        

        
        
        
class BlogAdminView(BaseView):
    
    def is_accessible(self):


        if current_user.is_authenticated:

            if current_user.is_admin:

                if current_user.role.role == "super-admin":
                    
                    return True
                else:

                    return False

            else:

                flash("You do not have permission", "danger")
                return redirect(url_for("home"))

        else:

            flash("You do not have permission", "danger")
            return redirect(url_for("home"))
        
        
    @expose('/')
    def index(self):
        
        return self.render('admin/blog_admin_view.html', title = "blog admin view")
    
        
    @expose('/new_blog', methods = ["GET", "POST"])
    def new_blog(self):
        
        
                
        if request.method == "POST":
            
            print("POSTING NEW BLOG!!!")
            
            title = request.form.get("title")
            
            check_title = Blog.query.filter_by(title = title).first()
            
            if check_title is not None:
                
                
                
                flash("This blog title is not unique!", "warning")
                return redirect(url_for("blog_admin_view.new_blog"))
        
        
            else:
                
                
                data = request.form.get("blog-textarea")
                
                print("NEW BLOG!!")
                print(data)
                
                
                #Blog(title, data, user_id)
                new_blog = Blog(title, data, current_user.id)
                db.session.add(new_blog)
                db.session.commit()
                
                # http://127.0.0.1:5000/admin/blog_admin_view/new_blog
                
                blog = Blog.query.filter_by(title = title).filter_by(user_id = current_user.id).first()
                flash("You've submitted a new blog!", "success")
                return redirect(url_for("blog_section.one_blog", blog_id = blog.id, blog_title = blog.title))
        
        

        
        return self.render('admin/new_blog.html', title = "new_blog")
    
    @expose("/edit_blog/<string:author>/<int:blog_id>/<string:blog_title>", methods = ["GET", "POST"])
    @login_required
    def edit_blog(self, author, blog_id, blog_title):
        
        
        blog = Blog.query.filter_by(id = blog_id).first()
        
        
        if blog is None:
            
            flash("This blog does not exist!", "warning")
            return redirect(url_for("admin.admin_home"))
        
        blog_title = blog.title
        data = blog.data
        
        if request.method == "POST":
            
            blog_title = request.form.get("title")
            data = request.form.get("blog-textarea")
            
            print("REQUEST BLOG TITLE!!!")
            print(blog_title)
            
            if blog_title != blog.title:
                
                check_title = Blog.query.filter_by(title = blog_title).first()
                
                if check_title is None:
                    
                    blog.title = blog_title
                    blog.data = data
                    db.session.commit()
                    flash("You've updated your blog", "success")
                    return redirect(url_for("blog_section.one_blog", blog_id = blog.id, blog_title = blog.title))
                
            else:

                blog.title = blog_title
                blog.data = data
                db.session.commit()
                flash("You've updated your blog", "success")
                return redirect(url_for("blog_section.one_blog", blog_id = blog.id, blog_title = blog.title))

        return self.render('admin/edit_blog.html', title = "edit_blog",
                           blog_title = blog_title,
                           data = data)
    
    
    
        
            
    @expose('/blog_container', methods = ["GET", "POST"])
    @login_required
    def blog_container(self):

        return self.render('admin/blog_container.html', title = "blog_container")
    
        
    
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
        
        
        


        
admin = Admin(app, name="Awesome Blog", 
              template_mode = "bootstrap3",
              index_view = MyHomeView(menu_icon_type="glyph",
                                      menu_icon_value = "glyphicon-home"))


        



admin.add_view(MyView(name='Hello 1', endpoint='test1', category='Test'))
admin.add_view(MyView2(name='Hello 2', endpoint='test2', category='Test'))
admin.add_view(MyView3(name='Hello 3', endpoint='test3', category='Test'))





#  BLOGS #######################################################################


admin.add_view(MyModelView(Blog, db.session, menu_icon_type="glyph",
                           menu_icon_value = "glyphicon glyphicon-comment",
                          name = "Blogs", endpoint = "blog", category="Blogs"))

admin.add_view(BlogAdminView(name = "Blog Admin",  menu_icon_type="glyph",
                           menu_icon_value = "glyphicon glyphicon-comments",
                             
                            endpoint = "blog_admin_view", category="Blogs"))













    
admin.add_link(UserIconLink(name= "admin", category='', url="/home"))

admin.add_view(MyModelView(User, db.session, menu_icon_type="glyph",
                           menu_icon_value="glyphicon glyphicon-user"))
        
        

admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))



path = os.path.join(os.path.dirname(__file__), "static")

admin.add_view(MyAdmin(path,"/static", name="Static Files",
                       menu_icon_type="glyph",
                       menu_icon_value="glyphicon glyphicon-file"))

# admin.add_view(MyAdminView())

# admin.add_view(MyModelView(User, db.session, menu_icon_type="glyph",
#                            menu_icon_value="glyphicon glyphicon-user"))
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        