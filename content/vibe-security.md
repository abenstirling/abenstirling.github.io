+++
title = "Vibe Security"
date = 2025-04-01
collaborators = "Eugene Van Der Watt"
stats = "1st SDx 2025 hackday, 150+ scans"
status = "V1.0 website"
+++

The whole idea of this came from when [Plumeria](../plumeria) was "hacked" one evening. 

What I mean by hacked is two things: 
1. Click-jacking 
2. Rate-limiting
(some friends were spamming the request endpoint)

How my workflow went to solve the problem: 
```
vulnerability memo -> ai fixes backend -> ai tests backend
```

I was blown away at how fast it fixed it. Since these security problems are likely common, the LLMs probably have great references on how to fix. 

Given I had a vibe hackathon coming up, I thought it would be a great hack: a security scanner for all the other vibe coded applications. 

My general plan was to follow the guidance from [this blog from replit](https://docs.replit.com/tutorials/vibe-code-security-checklist) in an automated 

```
put in url -> run tests -> give score (results too)
```

