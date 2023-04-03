from datetime import date
from app.views.blog import bp
from app.extensions import *
from app.models.form import *
from app.models.tables import *
from app.views.auth.auth import login_required


@bp.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@bp.route("/post/<int:post_id>", methods=['GET', 'POST'])
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if g.user == None:
            flash('Login Requiered')
            return redirect(url_for('auth.login'))
        new_comment = Comment(
            comment_author=g.user,
            comment_date=date.today().strftime("%B %d, %Y"),
            parent_post = requested_post,
            body=form.body.data,
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("blog.show_post", post_id=post_id))
    comments =  Comment.query.filter_by(post_id=post_id).all()
    return render_template("post/post.html", post=requested_post, form=form, comments = comments)

@bp.route("/about")
def about():
    return render_template("about/about.html")


@bp.route("/contact")
def contact():
    return render_template("contact/contact.html")


@bp.route("/new-post", methods=['GET','POST'])
@login_required
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=g.user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("blog.get_all_posts"))
    return render_template("post/make-post.html", form=form)


@bp.route("/edit-post/<int:post_id>", methods=['GET','POST'])
@login_required
def edit_post(post_id):
    post = db.session.query(BlogPost).filter_by(post_id).first()
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("blog.show_post", post_id=post.id))
    return render_template("blog.make-post.html", form=edit_form)


@bp.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    # Find the blog post to delete
    
    # Delete all comments associated with the post
    
    # Commit changes to the database
    for comment in Comment.query.filter_by(post_id=post_id).all():
        print(comment)
        db.session.delete(comment)
    db.session.delete(BlogPost.query.filter_by(id=post_id).first())
    db.session.commit()
    return redirect(url_for('blog.get_all_posts'))



    
    


