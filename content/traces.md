+++
title = "traces"
date = 2026-04-01
status = "active"

[extra.cover]
    image = "/posts/traces.webp"
+++
TO-DO: 
- [ ] add in the links / photos 
- [ ] discuss w/ nicco
- [ ] get traces in a state to open-source
	- [ ] remove the website 
	- [ ] remove the stripe 
	- [ ] publish for a new repo 
	- [ ] have the following 
		- [ ] mcp 
			- [ ] w/ w/o agent 
		- [ ] kicad extension working 

I have been getting back into hardware again. It is so frustrating its fun. 

I've noticed some pain-points in the the process, and developed a tool with a friend that is quite useful.

I believe there are two valuable aspects to PCB design that can be automated with: 
1. Part sourcing 
2. Semantic Rule Check (SRC)

**traces** is four pieces that form one loop: the **mcp** grounds an LLM in real supplier data so it can actually find parts, the **KiCad extension** uses that to populate your schematic so it becomes the source of truth, a tuned **agent** makes the sourcing cheap and fast enough to feel instant, and the **SRC** reads the now-complete schematic to catch the semantic bugs ERC can't. Source the parts → fill the schematic → check the schematic.

### Part Sourcing 
---
LLMs are horrible at finding parts for a project, mostly because all the part information are hosted on a few distributor sites that these labs weren't able to train on. 

Let us say there are three main suppliers for electronic parts: 
- Digikey 
- Mouser
- LCSC

The idea: ground a LLM query with real data from the supplier site. 

This is the **traces mcp**. 

It is very simple. You connect your LLM to the mcp, and ask it for a part.

Ok very useful. **Use it- its open-source.** 

Wouldn't it be nice if it could just populate the information so you can use the schematic as the source of truth so you didn't have to run around copy/pasting data... 

### KiCad Extension 
---
Imagine if your schematic was fully reconciled: 
- each part had a 
- each part had a datasheet downloaded locally
- each part had a price 

If you don't have all the information filled, don't worry. Press `Source` and 


![[Pasted image 20260620174134.png]]

But you might have noticed, there needs to be a LLM to run the query in order to fill the proper information? 

### traces agent / eval 
---
That `Source` button has to call *something*. The first version handed the request to a general-purpose Claude agent and let it drive the supplier APIs.

It worked, but it was ~$0.10 per part. That doesn't scale when a board has 80 parts.

Oh, and it could take up to a minute per part. Horrid. I don't have to have taste to know that is trash UX — if anything loads for more than 5 seconds my intuition is that it's borked.

So we treated model choice as a benchmark instead of a default. The sourcing work is small and well-defined — take a natural-language request, call a supplier tool, return a ranked in-stock part — so a frontier model is overkill. OpenRouter let us swap models behind one API and race them on the exact same workload:

```python
# bench.py — (model id, why test it, approx $/Mtok in/out)
MODELS = [
    ("google/gemini-3.1-flash-lite",             "Fast, cheap, Google-native tools, 1M ctx",  "$0.25 / $1.50"),
    ("google/gemini-3-flash-preview",            "More accurate than Lite, agentic focus",    "$0.50 / $3"),
    ("deepseek/deepseek-v4-flash",               "Best non-Google cheap MCP executor",        "~$0.13 / ~$0.26"),
    ("qwen/qwen3-coder-flash",                   "Code/tool agentic workflows",               "$0.195 / $0.975"),
    ("x-ai/grok-4.1-fast",                       "Strong real-world tool calling, 2M ctx",    "~$1.25 / $2.50"),
    ("mistralai/mistral-small-3.2-24b-instruct", "Very cheap, function calling + structured", "$0.075 / $0.20"),
    ("openai/gpt-oss-120b",                      "Cheap planner/validator/JSON-repair",       "~$0.039 / ~$0.18"),
    ("z-ai/glm-4.6",                             "Purpose-built-ish for tool use, mid tier",  "~$0.50 / ~$2.00"),
    ("inclusionai/ring-2.6-1t",                  "Long-horizon tool agent",                   "~$0.075 / $0.625"),
    ("google/gemini-3.5-flash",                  "Higher-end Google Flash lane",              "~$1.50 / $9"),
]
```

The things we cared about, in order: **accuracy, then cost, then speed.**

The harness spins up an isolated API + worker pair per model (unique queue and port so it never collides with a running stack), then runs the same sourcing eval `TRIES` times. The eval sources one real part — an `STM32G491C` in `LQFP48` — across all three suppliers (JLCPCB, Digi-Key, Mouser):

```python
# eval.py
TIMEOUT_S = 30   # hard cutoff — job is killed after this
SLOW_S    = 15   # pass/fail threshold

PART = "STM32G491C"
FOOTPRINT = "LQFP48"
```

A try "passes" only if it returns a real part number *under* the 15s threshold; a timeout counts as the full 30s, so flaky or slow models sink to the bottom automatically. Models are ranked by total wall time across all tries, accuracy as the tiebreak:

```python
ranked = sorted(results, key=lambda r: (r["grand_total"], -r["total_passed"]))
```

Our results:

| # | Model | Avg/try | Passed | $/Mtok (in/out) |
|---|-------|--------:|:------:|-----------------|
| _TODO: paste the bench leaderboard output here_ |

Net effect: dropping from a general-purpose agent to a benchmarked Flash-class model gave us a **~2 order-of-magnitude improvement in both cost and latency per part** — from ~$0.10 and up-to-a-minute down to fractions of a cent and a couple of seconds.

### Semantic Rule Check (SRC)
---
You already run a Design Rule Check (DRC) and Electrical Rule Check (ERC). Both are mechanical: spacing, connectivity, unconnected pins. Neither one reads your design.

I would like to propose a third: the **Semantic Rule Check (SRC)** — the class of bugs that pass DRC and ERC clean but are still wrong.

LLMs are good at language, so why not just have it find 
- rotated a usb-c connector 180* and now the `d+` is connected to the `d-`![[Pasted image 20260620172340.png]]
- you change a netlist label from `CAN_RXD` to `CAN_RX` and don't update all instances 
- check the rating of the passives for power-related things 

Ok those are basic. Imagine if the 
- 

Why now? 
1. KiCad is becoming widely adopted as a free and open-source EDA that is super capable
2. It is a local program with a CLI, and its files are just plain text 
3. **You can use an agent like Claude Code or Codex to actually make the changes once they are detected!**



### Looking Forward 
---
"Automating electrical engineering" would be the natural progression of these ideas. 

Economically, this is a juicy opportunity, and the value shows up in two places.

**The tools are expensive.** A seat of Altium runs ~$4k–$10k/yr; Siemens (Xpedition / Capital) is enterprise-quote territory north of that. The market already pays a lot for software that helps engineers not make mistakes — and none of it reads the design the way an LLM can.

**The mistakes are more expensive than the tools.** The real cost isn't the license, it's the respin. Walk one through:

- A semantic bug — a flipped USB-C connector, an underrated cap on a power rail — passes DRC and ERC clean and ships.
- You catch it on the bench. Now you eat a new fab + assembly run and the lead time that comes with it: call it ~2–4 weeks of slip plus ~10–20 hours of engineering time to diagnose, fix, and re-review at $100/hr.
- If it slipped into a production batch instead — say 1,000 boards at ~$100 of raw material each — that's up to **$100k of inventory** at risk over a single net-name typo.

So the bet is simple: an SRC that runs in seconds against a fully-populated schematic is cheap insurance against a five-figure mistake. That's the whole pitch.

Electrical engineers are smart, and their jobs are complicated. 

To list a few of the main roles of their jobs:  
- **supply chain management** 
- **update / create PCB designs** 
- physically testing 

The implications of a tool that ensures accuracy of PCB design likely means that there will be a consolidation of chips, biasing on ones that: 

1. have accessible information (datasheet, footprint, availability)
2. have good data about them (i.e. ones on the internet that people use)




