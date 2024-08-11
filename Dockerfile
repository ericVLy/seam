# Use an official Python runtime based on alpine as a parent image.
FROM python:3.12-alpine3.20

# Add user that will be used in the container.
RUN addgroup -g 1000 -S eam && adduser eam -h /home/eam -D -G eam  -u 1000 -s /bin/sh 

# Port used by this container to serve HTTP.
EXPOSE 8080

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by eam and Django.
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories;\
apk update;\
apk upgrade;\
apk add --no-cache nginx nodejs npm libcap;


# Install the project requirements.
COPY requirements.txt /
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/;\
pip install --root-user-action=ignore -r /requirements.txt;\
pip install --root-user-action=ignore "gunicorn==20.0.4";

# Use /app folder as a directory where the source code is stored.
WORKDIR /home/eam/qr_yx_dy_eam

# Set this directory to be owned by the "eam" user. This eam project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN mkdir --parents /usr/local/nginx/logs/; \
rm -rf /var/lib/nginx/logs;\
mkdir --parents /var/lib/nginx/logs/;\
mkdir --parents /home/eam/qr_yx_dy_eam/;\
chown -Rch eam:eam /usr/local/nginx/;\
chown -Rch eam:eam /home/eam/;\
chown -Rch eam:eam /var/lib/nginx/;\
setcap cap_net_bind_service=+ep /usr/sbin/nginx;
# Copy the source code of the project into the container.
COPY --chown=eam:eam . /home/eam/qr_yx_dy_eam/

# Use user "eam" to run the build commands below and the server itself.
USER eam


RUN nginx -t -c /home/eam/qr_yx_dy_eam/nginx/nginx.conf

# Collect static files.
RUN \
python manage.py install_node_dependencies; \
python manage.py collectstatic --noinput --clear

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   eam instance can be started with a simple "docker run" command.
CMD set -xe; \
nginx -c /home/eam/qr_yx_dy_eam/nginx/nginx.conf;\
python manage.py makemigrations --noinput; \
python manage.py migrate --noinput; \
gunicorn qr_yx_dy_eam.wsgi:application
