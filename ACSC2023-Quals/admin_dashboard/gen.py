#	// csrf-token=0x2482d495da6cd9022e88409822651761=gmp_mod(gmp_add(gmp_mul($A, 0x7a7a7a7a7a7a),$C),gmp_init("0xc4f3b4b3deadbeef1337c0dedeadc0dd"))
#	// csrf-token=0xb974b18916255da2e7d093cfad37a366=gmp_mod(gmp_add(gmp_mul($A, 0x2482d495da6cd9022e88409822651761),$C),gmp_init("0xc4f3b4b3deadbeef1337c0dedeadc0dd"))
#   //gmp_mod(gmp_add(gmp_mul($A, $X),$C),$M);

import binascii
from gmpy2 import *

def gen(A,I1,C,M):
    A = mpz(A)
    I1 = mpz(I1)
    C = mpz(C)
    M = mpz(M)
    result = hex(mod(add((mul(A, I1)), C),M))
    return result

I1 = int(binascii.hexlify(b'123456781'),16) #Input_1 (Username)
M = int('0xc4f3b4b3deadbeef1337c0dedeadc0dd',16) #Modulo
R1 = 0x1a452416ff80f50031f6d234144feb8 #Result_1
R2 = 0xa74bb23b99500da1a6703aa55dc177cf #Result_2


print(f"{R1} = ((A*({I1}))+C) && {R2} = ((A*({R1}))+C)")
print(f"{M=}")

#receiving A,C from modulo equations solver
######################################################
I2 = int(binascii.hexlify(b'admin'),16)
A = 32695124578757063299293091702847209330
C = 60610712695462011086335162323425538811
if A and C:
    print(gen(A,I2,C,M))




#print(f"{R2-R1} = (A*({R1-I1})) mod {M}")
#R2-R1 = A*(R1-I1) % M
#197981568320113421229440852166257576965 = (A * (48531518183298008719106939019787410663)) mod 261794080394952939563792136599736533213