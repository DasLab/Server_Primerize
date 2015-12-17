sudo usermod -a -G www-data ubuntu

sudo chgrp -R www-data *
sudo chown -R ubuntu *.py *.md *.txt src media config .gitignore
sudo chown -R www-data backup data cache
sudo chmod 640 *.py* *.md *.txt .gitignore

sudo chmod 640 $(find src -type f)
sudo chmod 750 $(find src -type d)
sudo chmod 640 $(find media -type f)
sudo chmod 750 $(find media -type d)

sudo chmod 660 $(find cache -type f)
sudo chmod 770 $(find cache -type d)
sudo chmod 660 $(find backup -type f)
sudo chmod 770 $(find backup -type d)
sudo chmod 660 $(find data -type f)
sudo chmod 770 $(find data -type d)
sudo chmod 660 src/pymerize/__pycache__/*
sudo chmod 770 src/pymerize/__pycache__

sudo chmod 640 $(find config -type f)
sudo chmod 750 $(find config -type d)
sudo chown www-data config/cron.conf 

sudo chown -R ubuntu:ubuntu *.sh
sudo chmod -R 700 *.sh

sudo chown ubuntu:www-data ../yuicompressor.jar
sudo chmod 640 ../yuicompressor.jar
