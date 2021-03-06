from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField,  SubmitField, TextAreaField
from wtforms.validators import Required, Length, Email ,EqualTo, Regexp
from wtforms import ValidationError
from ..models import User   

class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('keep me logged in')
    sumbit = SubmitField('Log In')

class RegistForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('username', validators=[Required(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9._]*$', 0, '用户名必须是字母数字下划线')])
    password = PasswordField('password', validators=[Required(), EqualTo('password2', message="密码要相等")])
    password2 = PasswordField('ensure_pwd', validators=[Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError("该邮箱已经注册")

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError("该用户名已经注册")

class AboutForm(Form):
   location = StringField('loaction', validators=[Length(0,64)])
   about_me = TextAreaField('about_me')
   submit = SubmitField('submit')
