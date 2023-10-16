from Crypto.Util.number import *
from tqdm import tqdm
from sage.all import pari

p1 = 401327687854144602104262478345650053155149834850813791388612732559616436344229998525081674131271
p2 = 500233813775302774885494989064149819654733094475237733501199023993441312997760959607567274704359
p3 = 969568679903672924738597736880903133415133378800072135853678043226600595571519034043189730269981
e1 = 398119
e2 = 283609
e3 = 272383
c = 104229015434394780017196823454597012062804737684103834919430099907512793339407667578022877402970

def mod_nth_root(x, e, n):
    r, z = pari(f"r = sqrtn(Mod({x}, {n}), {e}, &z); [lift(r), lift(z)]")
    r, z = int(r), int(z)
    roots = [r]
    if z == 0:
        return roots
    t = r
    while (t := (t*z) % n) != r:
        roots.append(t)
    return roots

for r3 in tqdm(mod_nth_root(c, e3, p3)):
    for r2 in mod_nth_root(r3, e2, p2):
        for flag in mod_nth_root(r2, e1, p1):
            flag = long_to_bytes(flag)
            if b'ISITDTU{' in flag:
                print(flag)


'''
#another-solution by bruteforcing all the modular nth roots

def mod_roots(x, e, p):
    return GF(p)(x).nth_root(e, all=True)

for r3 in tqdm(mod_roots(c, e3, p3)):
    for r2 in mod_roots(r3, e2, p2):
        for r1 in mod_roots(r2, e1, p1):
            try:
                print(long_to_bytes(int(r1)).decode())
            except:
                continue
'''
