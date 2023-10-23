#!/bin/bash
if [ -z "$1" ]
then
      echo "Domain requires as argument without www. i-e example.com"
      exit
fi

if ! command -v certbot &> /dev/null
then
    echo "Installing certbot package"
    sudo apt install python3-certbot-apache
fi
sudo certbot --apache -d "$1" -d "www.$1"