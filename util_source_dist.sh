cd ~
git clone https://github.com/DasLab/Primerize
zip -r primerize_release.zip Primerize/
sudo mv primerize_release.zip ~/Server_Primerize/data/
sudo cp -r Primerize/* NA_Thermo/
sudo python setup.py install
