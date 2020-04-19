from flask import render_template, request, Blueprint
from flask_blog.models import Post

main = Blueprint('main', __name__)  # 'main' is the name of our blueprint


# route() decorator to tell Flask what URL should trigger our function.
@main.route("/")
@main.route("/home")
def home():
    # specify the page. default is 1. this function checks for 'page' string/word  and 1 in the url. args is used as a general for any kind of variable that can mainear in the url. eg /, '<' etc
    page = request.args.get('page', 1, type=int)
    # this will only get the 1st page. But by adding 'page=page'. It seicifies the page being requested.
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
