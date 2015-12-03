sudo usermod -a -G www-data ubuntu

sudo chgrp -R www-data *
# sudo chgrp -R ubuntu cache
sudo chown -R ubuntu *.py *.md *.txt src media config .gitignore
sudo chown -R www-data backup data cache

sudo chmod 640 *.py* *.md *.txt .gitignore
sudo chmod 640 src/*.py* src/management/* src/management/commands/* src/templatetags/* src/pymerize/* 
sudo chmod 750 src src/management src/management/commands src/templatetags src/pymerize 
sudo chmod 640 media/css/* media/fonts/* media/html/* media/fonts/Helvetica/* media/js/* media/js/admin/* media/js/public/* media/js/suit/*
sudo chmod 750 media/css media/fonts media/fonts/Helvetica media/html media/js media/js/admin media/js/public media/js/suit media
sudo chmod 640 media/images/*.*g* media/images/docs/* media/images/icons/*
sudo chmod 750 media/images media/images/docs media/images/icons
sudo chmod 640 media/admin/*.html media/admin/img/*.*g* media/admin/img/gis/* media/admin/img/filemanager/* media/admin/js/*.js 
sudo chmod 750 media/admin media/admin/img media/admin/img/gis media/admin/img/filemanager media/admin/js 

sudo chmod 640 media/css/min/* media/js/public/min/* media/js/admin/min/* media/js/suit/min/*
sudo chmod 750 media/css/min media/js/public/min media/js/admin/min media/js/suit/min

sudo chmod 660 cache/* src/pymerize/__pycache__/*
sudo chmod 770 cache src/pymerize/__pycache__
sudo chmod 640 backup/* data/primerize_release.zip data/1d/* data/2d/* data/3d/*
sudo chmod 750 backup data data/1d data/2d data/3d

sudo chmod 640 config/*.py* config/*.example config/*.conf
sudo chown www-data config/cron.conf 
sudo chmod 750 config

sudo chown -R ubuntu:ubuntu *.sh
sudo chmod -R 700 *.sh
