from flask_wtf import Form
from wtforms import SubmitField
from wtforms.validators import Required
from flask_pagedown.fields import PageDownField


class PostForm(Form):
    body = PageDownField("What do you want to say?", validators=[Required()])
    submit = SubmitField("提交")
            
