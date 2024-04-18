+++
title = 'PCB Business Card'
date = 2023-09-19T15:57:22-07:00
draft = false

[cover]
    image = "/posts/businesscard_cover.png"
    relative = true
+++

## I Made a Business Card Because I Didn't Have One. 

The thought behind this one is that I needed a way to stand out. I've always been a bit of a non-traditional student, and my background is unique. I wanted to highlight how I build real things. I don't *just* build real things, I ship real things. 

I initially started with just a bare PCB with a QR code. Everyone always asked, "Does it work?" That is when I knew that functionality had to be added. I am not the first to do NFC. I owned a dot.card and it was cool but my main issues revolved around how it wasn't customizable. It was blank and the site was not mine. 

I fixed that. The first version had my name as silkscreen. It worked, though the LED didn't work due to me not properly grounding the chip. Frankly, if the first version didn't work I probably wouldn't have known what to do. There were too many variables, specifically the antenna which I knew nothing about. Plus at that point, it was just mine and it wasn't that big of a deal- a total backburner project. 

Then it worked, and most people I showed wanted one. I got a list of about 5 people, enough to buy a custom order from JLC and from Digikey. A week later everything came, I started to assemble and had no luck. It just wouldn't turn on. Then I tried reworking, even tried to order a new stencil (which would be helpful for other versions).

I couldn't figure it out, I would be down $200+ if my next version didn't work I *and* I would likely have to refund because it had been a month. I called Dusty, and he recommended trying to use the lasers. I got so darn lucky; I designed a ground plane of copper on the top and bottom. I just copied a reference schematic and didn't think to much about it. I did a laser engrave test with another board I had on loan and it turned out picture perfect. It removed the black mask and unveiled a gorgeous copper layer. At that point, I ordered 25 blank cards. I did a change to to the LED and wasn't sure if that would affect the functionality of the NFC protocol, specifically how it could mess up the impedance. 

The boards arrived and sure enough they worked. I went to the makerspace and made a nice metal jig for holding the cards in and just ripped them in one pass. Around 75% turned out great and the rest were tolerable. I also found out that I could program a link to the invoice on the card. I shipped off that afternoon and felt super great.


---
### Demo Video

{{<youtube SqF1A_pn7E8>}}

---

I have since made a thinner version and a version with two sides (business in the front and party in the back). I have also published the [app to program them](https://abenstirling.com/posts/botionnfc/), available on the App Store.

I sell them for $25 a pop, [email me](mailto:abenstirling@pm.me) if you want one!