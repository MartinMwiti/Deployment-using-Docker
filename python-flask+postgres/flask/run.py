# when working with packages, this will import from the the __init__.py file within this package(flask_blog). The 'app' variable has to exist within __init__.py file
from flask_blog import create_app

app = create_app()  # we don't pass anaything because we're using 'Config' as the default input

if __name__=='__main__':
    app.run(host='0.0.0.0')
