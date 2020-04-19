from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog import db, bcrypt
from flask_blog.models import User, Post
from flask_blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flask_blog.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__) # 'users' is the name of our blueprint


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    # validate_on_submit will check if it is a POST request and if it is valid.
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account has been created! You are now able to log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():  # validate_on_submit(): This is a shortcut for form.is_submitted() and form.validate()
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # login_user() Logs a user in. form.remember.data is  a True/False value if checked(True) or unchecked(False)
            # login_user(): This will return True if the log in attempt succeeds, and False if it fails
            login_user(user, remember=form.remember.data)
            # after loggging in, access the page you were viewing before you logged in.
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login Unsuccessful. Please check email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
# login_required func - If you decorate a view with this, it will ensure that the current user is logged in and authenticated before calling the actual view.
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:  # if new image/picture is provided
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file  # returns the name and ext of the image
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':  # populate the form fields with current field data
        form.username.data = current_user.username
        form.email.data = current_user.email
    # unless changed current_user.image_file = default.png (in our case). filename= pics/default.png as specified from the models.py file
    image_file = url_for('static', filename='pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    return render_template('user_post.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():  # route where a user/person enters there email to request a password reset
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
# route where a user/person actually reset there password with the token active
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # found in the model.py file. the token is found through 'token = user.get_reset_token()'
    user = User.verify_reset_token(token)
    if user in None:  # if we don't get a user
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()  # if the token is valid
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
