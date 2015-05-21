# port forward
#sudo pfctl -ef /Users/daslab/pf.config 
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to 8080

# run screen
screen -dmL python run_server.py release
# kill screen
screen -ls
screen -S *** -X kill
# reattach screen
screen -dr
