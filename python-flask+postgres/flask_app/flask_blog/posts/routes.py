from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.models import Post
from flask_blog.posts.forms import PostForm


posts = Blueprint('posts', __name__)  # 'posts' is the name of our blueprint



@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    # use get() method when getting sth by id. In this case 'get_or_404()' method means give me the result with the provided id & if it doesn't exist, return 404 which stands for page doesn't exist.
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    # post is what is already in the database. form is what is being currently beeing populated/updated/added.
    post = Post.query.get_or_404(post_id)
    # this makes sure that if you're not the author of the post, you can't update the post.
    if post.author != current_user:
        abort(403)  # 403: Forbidden
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()  # we don't use .add() because that the content/data is already in the database. we'll use .commit() to make the changes
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        # populate title and content using existing data
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Title', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        about(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
