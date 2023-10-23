#!/bin/bash

# config
source .env

if [[ -z $(echo $aws_access_key | xargs) ]]
then
      echo "aws_access_key is empty"
      exit
fi

if [[ -z $(echo $aws_secret_key | xargs) ]]
then
      echo "aws_secret_key is empty"
      exit
fi

if [[ -z $(echo $aws_region | xargs) ]]
then
      echo "aws_region is empty"
      exit
fi

if [[ -z $(echo $aws_bucket | xargs) ]]
then
      echo "aws_bucket is empty"
      exit
fi

sudo apt-get update

# system dependencies
sudo apt install python3 python3-pip imagemagick libreoffice unoconv ffmpeg p7zip-full jpegoptim pngquant npm apache2 libapache2-mod-wsgi redis-server  poppler-utils supervisor -y
if ! command -v ebook-convert &> /dev/null
then
    sudo -v && wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sudo sh /dev/stdin
fi

# app dependencies
sudo npm install -g svgo
sudo pip3 install -r requirements.txt
sudo pip3 install gunicorn

# configuring background services
sudo cp ./redis-worker.conf /etc/supervisor/conf.d/redis-worker.conf
sudo cp ./website.service /etc/systemd/system/website.service

sudo sed -i "s|<<app_directory>>|$PWD|g" /etc/supervisor/conf.d/redis-worker.conf
sudo sed -i "s|<<app_directory>>|$PWD|g" /etc/systemd/system/website.service

# setup aws
sudo aws configure set aws_access_key_id "$aws_access_key"
sudo aws configure set aws_secret_access_key "$aws_secret_key"
sudo aws configure set default.region "$aws_region"
sudo aws configure set default.s3.signature_version s3v4

# update imagemagick polic
sudo cp ./policy.xml /etc/ImageMagick-*/policy.xml

# setup file/folder permissons
sudo chown -R $USER:www-data ./static

# start all services
sudo supervisorctl reread
sudo supervisorctl update

sudo systemctl daemon-reload

sudo systemctl start website
sudo systemctl enable website.service


# setup apache2 proxy
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_balancer
sudo a2enmod lbmethod_byrequests
sudo systemctl restart apache2 

sudo cp ./proxy.conf /etc/apache2/sites-available/000-default.conf
sudo systemctl restart apache2 
echo "Done!"

