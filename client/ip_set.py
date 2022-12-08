import os

os.system('ip rule add from 169.254.173.173 table 1')
os.system('ip route add 169.254.0.0/16 dev eth0 scope link table 1')
os.system('ip route add default via 169.254.0.1 dev eth0 table 1')

os.system('ip rule add from 169.254.219.127 table 2')
os.system('ip route add 169.254.0.0/16 dev eth1 scope link table 2')
os.system('ip route add default via 169.254.0.1 dev eth1 table 2')
