import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_blog import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # interested with the file extension so as to maintain the same extension while saving the image.
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/pics', picture_fn)

    output_size = (125, 125)  # tuple of our own size. Resize the picture
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)  # save the adjusted image file to the specified path

    return picture_fn  # after completing the above processes of resizing, renaming. return the image name+extension


def send_reset_email(user):
    # found in the model.py file. user = User.query.filter_by(email=form.email.data).first(). token = user.get_reset_token() is a code containing the payload(user_id i.e the id of the user requesting password change)
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@blog.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)} 

If you did not make this request then simply ignore this email and no changes will be made.
'''
# {url_for('reset_token', token=token, _external=True)} within the f-string shows a string or the url+token. when clicked. it trigges the 'reset_token' func
    mail.send(msg)
