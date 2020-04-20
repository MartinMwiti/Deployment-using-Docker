# Deployment-using-Docker
Containerizing and deployment of Python-flask+Django apps with Docker, Nginx and uWSGI.

The following is a guide on how i have containerized and deployed a python-flask app connected to an SQL database using Docker, Nginx, uWSGI and Postgres database.

## Prerequisites
* A server with Linux (I'm using Ubuntu 18.04) installed.

* Nginx installed. Follow [How To Install Nginx on Ubuntu 18.04.](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04)  

### uWSGI Configuration File
This will be dealt by the ``app.py`` file in our project directory:
   
  
      [uwsgi]
      wsgi-file = run.py
      callable = app
      socket = :8080 
      processes = 4
      threads = 2
      master = true
      chmod-socket = 660
      vacuum = true
      die-on-term = true
    
    
 * ``[uwsgi]`` header that lets uWSGI knows to apply the settings provided. 
 
 * wsgi-file = ``run.py`` is the python module responsible for running the app. callable = ``app`` refers to theobject in the ``run.py``    module. Together they can be replaced by a single line command ```module = run:app``` .
 
 * I'm using Nginx to handle actual client connections, which will then pass requests to uWSGI. Since these components are                operating on the same computer, a Unix socket is preferable because it is faster and more secure. I'll have my socket listen to port ``:8080`` for any requests.
 
 * Next, we’ll tell uWSGI to start up in ``master`` mode and spawn four worker processes to serve actual requests.
 
 * I have changed the permissions on the socket. I’ll be giving the Nginx group ownership of the uWSGI process later on, so i needed to make sure the group owner of the socket can read information from it and write to it. ``vacuum: true`` cleans up the socket when the process stops.
 
 * Lastly ``die-on-term`` option. This can help ensure that the init system and uWSGI have the same assumptions about what each process signal means. Setting this aligns the two system components, implementing the expected behavior
---
## General Layout:
* Using Nginx

   - Layout 1![Layout 1](https://hackernoon.com/photos/Ddx1Gu84SLTrEuGRGR6lu7txNc12-jvub3xvm)
   
   - Layout 2![Layout 2](https://camo.githubusercontent.com/b028531e5cd4eed10d4b9e7f873d57a91f1cdfd7/68747470733a2f2f696d6167652e736c696465736861726563646e2e636f6d2f707974686f6e6465766f70732d3133303330343138313532352d70687061707030322f39352f707974686f6e2d6465766f70732d796f75722d6f776e2d6865726f6b752d33322d3633382e6a70673f63623d31333633323635353735)
   
* Using gunicorn
   ![Layout](https://miro.medium.com/max/1000/1*_tIjoh9xdUe22ttIDFrZ9A.png)
---
### Building docker-compose
* After creating flask, database and Nginx images. Build a docker-compose based on those containers by running: 
         
        sudo docker-compose build
         
* After building the docker-compose, run the docker-compose by using the command:
         
       sudo docker-compose up
* To end/close the running docker containers, run:
         
       sudo docker-compose down
---
## Additional Info
[How to do rapid prototyping with Flask, uWSGI, NGINX, and Docker on OpenShift](https://towardsdatascience.com/how-to-do-rapid-prototyping-with-flask-uwsgi-nginx-and-docker-on-openshift-f0ef144033cb)
