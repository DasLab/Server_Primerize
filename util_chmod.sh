sudo usermod -a -G www-data ubuntu

sudo chgrp -R www-data *
sudo chown -R ubuntu *.py *.md *.txt src media config .gitignore
sudo chown -R www-data backup data cache
sudo chmod 640 *.py* *.md *.txt .gitignore
sudo chmod 640 *.py* robots.txt .gitignore
sudo chmod 600 *.md requirements.txt

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

sudo chmod 640 $(find config -type f)
sudo chmod 750 $(find config -type d)
sudo chown www-data config/cron.conf 

sudo chown -R ubuntu:ubuntu *.sh
sudo chmod -R 700 *.sh

sudo chown ubuntu:www-data ../yuicompressor.jar
sudo chmod 640 ../yuicompressor.jar
if [ $(whoami) = "ubuntu" ];
then
	sudo chown root:ubuntu ../NA_Thermo/build ../NA_Thermo/deprecated_MATLAB ../NA_Thermo/dist ../NA_Thermo/primerize ../NA_Thermo/primerize.egg-info
	sudo chmod 750 ../NA_Thermo/build ../NA_Thermo/deprecated_MATLAB ../NA_Thermo/dist ../NA_Thermo/primerize ../NA_Thermo/primerize.egg-info
	sudo chown ubuntu:www-data ../NA_Thermo/LICENSE.md
	sudo chmod 640 ../NA_Thermo/*.md ../NA_Thermo/*.txt ../NA_Thermo/*.py

fi
