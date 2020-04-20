FROM python:3.7.2-stretch

# working directory in our container
WORKDIR /app

# copy the current directory contents into the container at /app
ADD . /app

# Install the dependencies
RUN pip install -r requirements.txt

CMD [ "uwsgi", "app.ini" ]