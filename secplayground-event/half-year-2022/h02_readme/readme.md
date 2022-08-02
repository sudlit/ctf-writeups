# README.exe (Tower 2)
## Level
`HARD`
## Flag Format
flag{xxxxx}
## Solution
After downloading we will README.exe file
and if you run this file it will show a messagebox
so it is the fake flag.

I decided to debugging file with IDA Pro.
continuing disassembly at main to see source

![](pic/1.JPG)

analyze code and convert it to python for solving 

script : 
```
v17 = list('6cbdA~g6bPiB5q6bCqd4xH')
v4 = len(v17)
for i in range(0,v4,11):
    v6 = v17[i]
    v17[i] = v17[i+10]
    v17[i+10] = v6
v7 = v17

######################

log = []
for i in range(0,len(v7),2):
    log.append(list(reversed(v7[i:i+2])))

v8 = []
for i in log:
    for j in i:
        v8.append(j)

######################

for j in range(len(v8)):
    v8[j] = chr(ord(v8[j]) ^ 5)
print(''.join(v8))
```


> Another solution
> - set break point -> seeing at stack of register -> we will get flag too :D

