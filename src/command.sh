# port forward
#sudo pfctl -ef /Users/daslab/pf.config 
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to 8080

# run screen
screen 
# press [enter]
source ~/.bash_profile
python run_server.py release
# press [ctrl+A+D]

# kill screen
screen -ls
screen -S *** -X kill
# reattach screen
screen -dr ***
