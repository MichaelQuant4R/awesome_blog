from flask_wtf import FlaskForm
from wtforms import (BooleanField, SubmitField, StringField, PasswordField, TextAreaField,
                     IntegerField, FloatField, SelectField)
from wtforms.validators import (DataRequired, Email, Length, EqualTo)

class RegisterForm(FlaskForm):
    
    
    username = StringField("username", validators = [DataRequired(), Length(min=3, max=20)],
                           render_kw = {"placeholder": "Enter a username..."})
    
    email = StringField("email", validators = [DataRequired(), Email(),  Length(min=10, max=35)],
                           render_kw = {"placeholder": "Enter a valid email..."})
      
    password = PasswordField("password", validators = [DataRequired(),   Length(min=3, max=20)],
                           render_kw = {"placeholder": "Enter a valid password..."})
    
    confirm_password = PasswordField("confirm_password", validators = [DataRequired(), 
                                                                      
                                          EqualTo("password", message="Password must match!")],
                                                                      
                           render_kw = {"placeholder": "Enter a valid confirm password..."})
    
    submit = SubmitField("Sign up")
    
    

class LoginForm(FlaskForm):
    
    
   
    email = StringField("email", validators = [DataRequired(), Email(),  Length(min=10, max=35)],
                           render_kw = {"placeholder": "Enter a valid email..."})
      
    password = PasswordField("password", validators = [DataRequired(),   Length(min=3, max=20)],
                           render_kw = {"placeholder": "Enter a valid password..."})
    
  
    submit = SubmitField("Login")
    
    

    

class RequestTokenForm(FlaskForm):
    
    email = StringField("email", validators = [DataRequired(), Email(),  Length(min=10, max=35)],
                           render_kw = {"placeholder": "Enter a valid email..."})
  
    submit = SubmitField("Request Token")
    
    

#     RequestTokenForm, ResetPasswordForm
    

class ResetPasswordForm(FlaskForm):
    
    password = PasswordField("New Password", validators = [DataRequired(),   Length(min=3, max=20)],
                           render_kw = {"placeholder": "Enter a valid password..."})
    
    confirm_password = PasswordField("confirm_password", validators = [DataRequired(), 
                                                                      
                                          EqualTo("password", message="Password must match!")],
                                                                      
                           render_kw = {"placeholder": "Enter a valid confirm password..."})
    
    submit = SubmitField("ResetPassword")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    