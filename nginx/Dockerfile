FROM tutum/nginx
RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/ /etc/nginx/sites-enabled

# Getting additional tools
RUN apt-get update && apt-get install -y \
    vim \
    nano