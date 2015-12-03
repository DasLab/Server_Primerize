echo "$(tput setab 1) ubuntu $(lsb_release -a | head -2 | tail -1 | sed 's/.*Ubuntu //g') | \
linux $(uname -r | sed 's/[a-z]//g' | sed 's/\-//g') | \
screen $(screen --version | sed 's/.*version//g' | sed 's/(.*//g' | sed 's/[a-z ]//g') | \
bash $(bash --version | head -1 | sed 's/.*version//g' | sed 's/-release.*//g' | sed 's/[ ()]//g') | \
ssh $(cut -d$'\t' -f18 cache/stat_sys.txt | sed 's/ $*//') $(tput sgr 0)" > ~/.ver_txt

echo "$(tput setab 172) gcc $(gcc --version | head -1 | sed 's/.*) //g') | \
make $(make --version | head -1 | sed 's/.*Make//g' | sed 's/ //g') | \
cmake $(cmake --version | head -1 | sed 's/.*version//g' | sed 's/ //g') | \
ninja $(ninja --version) | \
llvm $(cut -d$'\t' -f20 cache/stat_sys.txt | sed 's/ $*//') | \
numba $(cut -d$'\t' -f33 cache/stat_sys.txt | sed 's/ $*//') $(tput sgr 0)" >> ~/.ver_txt

echo -n "$(tput setab 11)$(tput setaf 16) python $(cut -d$'\t' -f2 cache/stat_sys.txt | sed 's/ $*//') | \
java $(javac -version 2> temp.txt && sed 's/.*javac //g' temp.txt | sed 's/_/./g') | \
mysql $(cut -d$'\t' -f6 cache/stat_sys.txt | sed 's/ $*//') |$(tput sgr 0)" >> ~/.ver_txt

echo "$(tput setab 2) apache $(cut -d$'\t' -f7 cache/stat_sys.txt | sed 's/ $*//') | \
wsgi $(cut -d$'\t' -f8 cache/stat_sys.txt | sed 's/ $*//') | \
openssl $(cut -d$'\t' -f9 cache/stat_sys.txt | sed 's/ $*//') $(tput sgr 0)" >> ~/.ver_txt

echo "$(tput setab 22) coreutils $(tty --version | head -1 | sed 's/.*) //g') | \
wget $(wget --version | head -1 | sed 's/.*Wget//g' | sed 's/built.*//g' | sed 's/ //g') | \
tar $(tar --version | head -1 | sed 's/.*)//g' | sed 's/-.*//g' | sed 's/ //g') | \
curl $(cut -d$'\t' -f23 cache/stat_sys.txt | sed 's/ $*//') | \
gdrive $(cut -d$'\t' -f22 cache/stat_sys.txt | sed 's/ $*//') | \
yuicompressor $(cut -d$'\t' -f34 cache/stat_sys.txt | sed 's/ $*//') $(tput sgr 0)" >> ~/.ver_txt

echo "$(tput setab 39) $(python -c "import celery, virtualenv, Tkinter, setuptools; \
print 'tkinter', Tkinter.Tcl().eval('info patchlevel'), '| virtualenv', virtualenv.__version__, '| setuptools', setuptools.__version__") | \
requests $(cut -d$'\t' -f26 cache/stat_sys.txt | sed 's/ $*//') | \
simplejson $(cut -d$'\t' -f27 cache/stat_sys.txt | sed 's/ $*//') $(tput sgr 0)" >> ~/.ver_txt

echo "$(tput setab 20) django $(cut -d$'\t' -f3 cache/stat_sys.txt | sed 's/ $*//') | \
crontab $(cut -d$'\t' -f4 cache/stat_sys.txt | sed 's/ $*//') | \
environ $(cut -d$'\t' -f5 cache/stat_sys.txt | sed 's/ $*//') | \
suit $(cut -d$'\t' -f12 cache/stat_sys.txt | sed 's/ $*//') | \
adminplus $(cut -d$'\t' -f13 cache/stat_sys.txt | sed 's/ $*//') | \
filemanager $(cut -d$'\t' -f14 cache/stat_sys.txt | sed 's/ $*//') $(tput sgr 0)" >> ~/.ver_txt

echo "$(tput setab 55) numpy $(cut -d$'\t' -f30 cache/stat_sys.txt | sed 's/ $*//') | \
scipy $(cut -d$'\t' -f31 cache/stat_sys.txt | sed 's/ $*//') | \
matplotlib $(cut -d$'\t' -f32 cache/stat_sys.txt | sed 's/ $*//') | \
boto $(cut -d$'\t' -f24 cache/stat_sys.txt | sed 's/ $*//') | \
pygithub $(cut -d$'\t' -f25 cache/stat_sys.txt | sed 's/ $*//') | \
gviz $(cut -d$'\t' -f17 cache/stat_sys.txt | sed 's/ $*//') $(tput sgr 0)" >> ~/.ver_txt

echo -n "$(tput setab 171) jquery $(cut -d$'\t' -f10 cache/stat_sys.txt | sed 's/ $*//') | \
bootstrap $(cut -d$'\t' -f11 cache/stat_sys.txt | sed 's/ $*//') | \
d3 $(cut -d$'\t' -f15 cache/stat_sys.txt | sed 's/ $*//') | \
zeroclipboard $(cut -d$'\t' -f16 cache/stat_sys.txt | sed 's/ $*//') |$(tput sgr 0)" >> ~/.ver_txt

echo "$(tput setab 15)$(tput setaf 16) rdatkit $(cut -d$'\t' -f35 cache/stat_sys.txt | sed 's/ $*//') | \
na_thermo $(cut -d$'\t' -f36 cache/stat_sys.txt | sed 's/ $*//') $(tput sgr 0)" >> ~/.ver_txt

echo "$(tput setab 8) git $(cut -d$'\t' -f19 cache/stat_sys.txt | sed 's/ $*//') | \
pip $(cut -d$'\t' -f29 cache/stat_sys.txt | sed 's/ $*//') | \
nano $(cut -d$'\t' -f21 cache/stat_sys.txt | sed 's/ $*//') | \
imagemagick $(mogrify -version | head -1 | sed 's/\-.*//g' | sed 's/.*ImageMagick //g') | \
htop $(htop --version | head -1 | sed 's/.*htop //g' | sed 's/ \-.*//g') | \
awscli $(aws --version 2> temp.txt && sed 's/ Python.*//g' temp.txt | sed 's/.*\///g') $(tput sgr 0)" >> ~/.ver_txt

echo -e "\n\n$(tput setab 15)$(tput setaf 16) Primerize PCR Assembly Design Server $(tput sgr 0)" >> ~/.ver_txt
echo -e "$(tput setab 15)$(tput setaf 16) primerize.stanford.edu / 52.33.71.43 $(tput sgr 0)\n" >> ~/.ver_txt
rm temp.txt
echo "Done."


