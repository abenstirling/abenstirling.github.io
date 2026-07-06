+++
title = "opentag"
date = 2024-01-01
+++

The goal here was to have an open-source device that could talk to your iPhone. 

It started as a school project called AirPark. You can see our demo video below:

<div class="video-container">
  <iframe src="https://www.youtube.com/embed/mPeMMJG-1Rs" title="OpenTag video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

I turned our demo one into a PCB, which probably didn't work because I didn't know how to program an esp32 properly. 

![opentag](/posts/opentag_1.webp)

I made another version, dipping the circular shape. 

![opentag](/posts/opentag_2.webp)

I got to a point where I wanted it to have a proper battery. I did the right thing by making an evaluation board, but in hindsight I should have just used the same coin-cell battery as the airtag. 

![opentag](/posts/opentag_3.webp)

![opentag](/posts/opentag_4.webp)

The project picked up again when they made some solid progress that can be found on this [github page](https://github.com/open-tags/opentag). 

![opentag](/posts/opentag_5.webp)

<div class="video-container">
  <iframe src="https://www.youtube.com/embed/eHUctjyQn7U" title="OpenTag iPhone demo" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>
Funny enough, I didn't get into the class so the project progressed without my direct contribution. Nobody wanted to work on it after the class, so naturally I picked up from there. 

I think the thing that was missing was the application. The application should have driven the design. 

A big problem was that there had to be middleware living on a specific MCU in order to talk to an iPhone. The tags can nicely talk to each other, so why wouldn't I just do that? 