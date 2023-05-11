import re
from pwn import *

io = remote('challs.actf.co',31402)
context.log_level = "DEBUG"
for i in range(100):
    data = io.recvline().decode()
    if "{" not in data:
        pattern = re.compile(r"Combine the first 3 letters of (.+) with the last 3 letters of (.+)")
        match = pattern.match(data)
        a1, a2 = match.group(1)[:3], match.group(2)[-3:]
        c = a1 + a2
        io.sendline(c.encode())
    else:
        print(data)
        break