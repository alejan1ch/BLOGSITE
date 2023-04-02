from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin


db = SQLAlchemy()


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask import render_template, redirect, url_for, flash, abort, session, g

from flask_migrate import Migrate
import os
from dotenv import load_dotenv
load_dotenv()

from  functools import wraps
