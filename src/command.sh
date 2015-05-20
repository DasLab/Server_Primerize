# port forward
sudo pfctl -ef /Users/daslab/pf.config 

# run screen
screen -dmL python run_server.py release
# kill screen
screen -ls
screen -S *** -X kill
# reattach screen
screen -dr
