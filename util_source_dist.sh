cd ~
git clone https://github.com/DasLab/Primerize --quiet
sudo cp -r Primerize/* NA_Thermo/
cd ~/NA_Thermo
sudo python setup.py install

cd ~
sudo rm -rf Primerize/.git
zip -rmq primerize_release.zip Primerize/
sudo mv primerize_release.zip ~/Server_Primerize/data/
