if [ -z "$1" ]
then
      echo "Domain requires as argument without www. i-e example.com"
      exit
fi

sudo cp ./proxy-domain.conf /etc/apache2/sites-available/000-default.conf
sudo sed -i "s|domain|$1|g" /etc/apache2/sites-available/000-default.conf
sudo systemctl reload apache2 