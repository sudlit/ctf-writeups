#!/usr/bin/env python3
import random
import binascii

def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b // a) * y, y)

def modinv(a, m):
	g, x, y = egcd(a, m)
	if g != 1:
		raise Exception('modular inverse does not exist')
	else:
		return x % m

def gcd(a, b): 
	if a == 0: 
		return b 
	return gcd(b % a, a) 

# print(f"Public Key = {b}")
# print(f"Private Key = {w,q}")
# print(f"Ciphertext = {c}")
# Public Key = [7352, 2356, 7579, 19235, 1944, 14029, 1084]
# Private Key = ([184, 332, 713, 1255, 2688, 5243, 10448], 20910)
# Ciphertext = [8436, 22465, 30044, 22465, 51635, 10380, 11879, 50551, 35250, 51223, 14931, 25048, 7352, 50551, 37606, 39550]

c = [8436, 22465, 30044, 22465, 51635, 10380, 11879, 50551, 35250, 51223, 14931, 25048, 7352, 50551, 37606, 39550]
b = [7352, 2356, 7579, 19235, 1944, 14029, 1084]
w = [184, 332, 713, 1255, 2688, 5243, 10448]
q = 20910

for r in range(100, q):
    if egcd(r, q)[0] != 1:
        continue
    flag = ""
    inv = modinv(r, q)
    for i in c:
        s = (i * inv) % q
        answer = ''
        for w_i in reversed(w):
            if s - w_i >= 0:
                answer += '1'
                s = s - w_i
            else:
                answer += '0'
        answer = chr(eval('0b' + answer[::-1]))
        flag += answer
    if "ACSC" in flag:
        print(flag)
        break
        
# plaintext += bytes([1 << j])


'''
def greedy(ll, target):
    out = []
    for i in range(len(ll) - 1, -1, -1):
        elem = ll[i]
        if elem <= target:
            target -= elem
            out.append(i)
    return out

'''
'''for r in range(100, q):
    if egcd(r, q)[0] != 1:
        continue
    s = modinv(r, q)
    flag = ""
    for cipher_item in c:
        cprime = cipher_item*s % q
        b = ''
        for w_i in reversed(w):
            if cprime - w_i >= 0:
                b += '1'
                cprime = cprime - w_i
            else:
                b += '0'
        b = b[::-1]
        flag += b
        if b'ACSC' in (long_to_bytes(int(flag, 2))):
            print((long_to_bytes(int(flag, 2))))
            break
'''
#https://jsur.in/posts/2020-04-06-auctf-2020-writeups