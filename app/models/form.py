from app.extensions import *

##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password =  PasswordField('Password', validators=[DataRequired()])
    name =  StringField('Name', validators=[DataRequired()])
    submit = SubmitField("Sign")
    
class Longin(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password =  PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Sign")
    
class CommentForm(FlaskForm):
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")