+++
title = "B-24 Gym Pass"
date = 2026-02-01
status = "active"
+++

I have a 24 hour subscription. It isn’t the best gym, but the checking in is really annoying. 

My options are as follows: 

1. Use 24 hour app (laggy & bad UI) 
2. scan my fingerprint and type my phone number on a keypad (ew)

One day, I looked at my pass and noticed that it was a QR code. 

![image.png](/posts/b24_1.webp)

https://www.24hourfitness.com/programs/24go

![IMG_8577.jpeg](/posts/b24_2.webp)

Key things: 

```jsx
{"SR":"24GO","TP":"P","AP":"1.84.1","DT":1768963389103,"MB":"MBR123456","OS":"iOS","DI":"a7f3e8c2-91b4-4d6f-b5a2-3c9e7f1d4b6a"}
```

Where DI is a UUID: 

```jsx
8 hex digits (time_low)
4 hex digits (time_mid)
4 hex digits (time_hi_version)
4 hex digits (clock_seq)
12 hex digits (node)
```

## Unix Timestamp

A [unix timestamp](https://en.wikipedia.org/wiki/Unix_time) is a universal timestamp that number of non-leap seconds passed since `1970-01-01`. 

This is critical because I would guess that the reason why 24 hour has a whole app is to make sure that you can’t have a “stale” qr code that you pass around. 

Now I have a QR code, but i need to add it to my apple wallet.

I was messing around with 

## QR Code

This is a simple python script: 

```jsx
import json, time, qrcode
DT = int((time.time() + 63072000) * 1000)
qrcode.make(json.dumps({"SR":"24GO","TP":"P","AP":"1.84.1","DT":DT,"MB":"MBR123456","OS":"iOS","DI":"a7f3e8c2-91b4-4d6f-b5a2-3c9e7f1d4b6a"})).save("gym_pass.png") 
```

Single line to run: 

```jsx
uv run --with qrcode[pil] qr.py
```

![qr.png](/posts/b24_3.webp)

## Apple Wallet

I wanted to setup an application as follows:  

```jsx
scan pass -> generate qr code -> add to pass -> download
```

But since I wasn’t sure about renewing my apple subscription PLUS

[Pass2U Wallet - Add store card App - App Store](https://apps.apple.com/us/app/pass2u-wallet-add-store-card/id1142473931)

ultimately, i needed to test my ideas. 

### Was it worth it?

Yes, for 3 reasons:

- i deleted the app
- there is joy for me just being the fastest 24 hour member to sign in.
- successfully reverse engineered it

good thing i don’t go to la fitness, cause they hash that sh**
```
@1HFP61657L3DKK
```