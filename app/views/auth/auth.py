from app.views.auth import bp
from app.extensions import *
from app.models.form import *
from app.models.tables import *
from werkzeug.security import generate_password_hash, check_password_hash

@bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not db.session.query(User).filter_by(email=form.email.data).first():
            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = User(
                email=form.email.data,
                name=form.name.data,
                password=hash_and_salted_password,
            )
            db.session.add(new_user)
            db.session.commit()
        else:
            flash('The email has been register before ')
        return redirect(url_for('auth.login'))
    return render_template("register/register.html", form=form)


@bp.route('/login', methods=['GET','POST'])
def login():
    form =  Longin()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
       
        if not user: 
            flash('Email is not found')
        elif not check_password_hash(user.password, form.password.data):
            flash('Password incorrect')
        else:
            session.clear()
            session['user_id'] = user.id
            session['is_authenticated'] = True
            return redirect(url_for('blog.get_all_posts'))
    return render_template("login/login.html", form= form)

@bp.route('/logout')
def logout():
    session.clear()
    session['is_authenticated'] = False
    return redirect(url_for('blog.get_all_posts'))

 # IMPLEMENT LOGIN MANAGER
def login_required(view):
    @wraps(view)
    def wrapped_View(**kwargs):
        if g.user is None:
            flash("Login Requiered")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_View

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter_by(id=user_id).first()
    
    
# @admin_only
def admin_only(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if session.get('user_id') == 1 or '1':
            return function(*args, **kwargs)
        else:
            return abort(403)
    return wrapper