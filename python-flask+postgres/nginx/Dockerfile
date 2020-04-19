# Use the Nginx image
FROM nginx

#Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Replace with our own nginx.conf and copy into the directory(/etc/nginx/conf.d/) in our container
COPY nginx.conf /etc/nginx/conf.d