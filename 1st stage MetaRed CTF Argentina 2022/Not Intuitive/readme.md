# Not Intuitive
## Flag Format
flag{xxxxx}
## Solution
Challenge : https://notintuitive.ctf.cert.unlp.edu.ar/

I entered this website and found a white page.
So I through this challenge should not be difficult. (guess from my experience)

I decided to change requests method in curl.
When I used OPTIONS method, Cookie will appear session and allowed methods.
So I tried request XXXXX to be method with cookie that recieved.

GOTCHA!.
Finally, I got the flag.

![](pic/1.jpg)
