from flask import Flask
from config import Config
from app.extensions import *


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
        
    db.init_app(app)
    migrate = Migrate(app, db)
    
    ckeditor = CKEditor(app)
    Bootstrap(app)
    gravatar = Gravatar(
        app,
        size=100,
        rating="g",
        default="retro",
        force_default=False,
        force_lower=False,
        use_ssl=False,
        base_url=None,
    )



    from app.views.auth import auth
    app.register_blueprint(auth.bp)
    
    from app.views.blog import blog 
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
   

    return app
