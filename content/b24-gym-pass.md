+++
title = "B-24 Gym Pass"
date = 2026-02-01
status = "active"
+++

I have a 24 hour subscription, and checking in really sucks. 

My options are as follows: 

1. Use 24 hour app (laggy & bad UI) 
2. Scan my fingerprint and type my phone number on a keypad (ew)

One day, I looked at my pass and noticed that it was a QR code. 

![Example pass](/posts/b24_1.webp)

We are going to use this [example pass](https://www.24hourfitness.com/programs/24go), to make sure I can still use mine and for you to make your own if you are interested. 

I used another phone to scan the contents of the QR code to see if we could reverse engineer it!

![scanning the qr code](/posts/b24_2.webp)

If we look at the content of the QR code we get the following: 
```jsx
{"SR":"24GO","TP":"P","AP":"1.84.1","DT":1768963389103,"MB":"MBR123456","OS":"iOS","DI":"a7f3e8c2-91b4-4d6f-b5a2-3c9e7f1d4b6a"}
```

Ok this is interesting!

Key things: 
- `DT` (presumably datetime)
- `MB` (member id, something I see on the app too, likely not to change) 

I scanned it twice, one a few seconds later than the other and noticed that only the `DT` changed, and it got a bit larger. 

## Unix Timestamp

A [unix timestamp](https://en.wikipedia.org/wiki/Unix_time) is a universal timestamp that number of non-leap seconds passed since `1970-01-01`. 

This is critical because I would guess that the reason why 24 hour has a whole app is to make sure that you can’t have a “stale” qr code that you pass around to your gym buddies. 

I realized something: 
- 24 checks for `time.now` > `DT` + ~1 min to make sure its a fresh pass
- BUT do they check for the `time.now` < `DT`???

So if I set the `DT` variable, say 2 years in the future, would that just be valid because its just not more than a minute in the past?  

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

![our pass qr code, from the future](/posts/b24_3.webp)

## Apple Wallet

I wanted to setup an application as follows:  

```jsx
scan pass -> generate qr code -> add to pass -> download
```
But you can't make a dynamic QR code with `.pkpass` aka apple wallet, so that sucks. 

But since I wasn’t sure about renewing my apple subscription PLUS [react-native-passkit-wallet](https://www.npmjs.com/package/react-native-passkit-wallet)
 wasn't a trivial setup I decided to go the simplest past forward to get a gym pass in my wallet. 

I used [Pass2U Wallet](https://apps.apple.com/us/app/pass2u-wallet-add-store-card/id1142473931). It took ~30 seconds and it looks like this: 

![B-24 Gym Pass](/images/b24gympass_cover.webp)


## The Test
I walked into 24 hour after a week of stalling. 

I was actually afraid I was gonna get banned, somehow. 

But in the end, I walked up. Scanned it, the dude working there said welcome in and yeah it works! 

## Was it worth it?

Yes, for 3 reasons:

- I deleted the app
- There is joy for me just being the fastest 24 hour member to sign in
- Successfully reverse engineered it

good thing i don’t go to la fitness, cause they hash that \s 