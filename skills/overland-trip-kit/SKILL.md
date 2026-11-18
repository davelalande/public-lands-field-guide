---
name: overland-trip-kit
version: 1.0.2
description: Gets a truck or van ready for an overlanding, boondocking or dispersed camping trip in the US. Use when someone asks what to pack or check, wants a packing list or camp checklist, asks how long their water, gas, battery or solar will last, how much water to carry, or wants a one-page trip sheet. Gear is named by kind, never by brand. Every number is the person's own or a labeled rule of thumb. States no facts about any place and never says a trip is safe.
license: MIT-0. Credit is welcome, never required.
compatibility: Needs nothing. scripts/rig.py needs Python 3.8 or newer. Pairs with the Public Lands Field Guide skill and the davelalande.com MCP connector for place facts.
metadata:
  author: Dave Lalande (American Adventurer)
  version: "1.0.2"
  home: https://tinycorp.ai/install
---

# Overland Trip Kit

Get a truck or a van ready the way a careful overlander would. The rig, the supplies, the numbers. Every assumption shown. Never a fact about a place.

## What this is

This kit answers "am I ready, and will my supplies last?" It is about the rig and the people in it. It is not about the place. It needs no network and no connector, and it works on its own.

## Start with the rig card

Ask for the person's numbers once, using [references/rig-card.md](references/rig-card.md): tank, miles per gallon loaded on dirt, water aboard, people, battery watt-hours, solar watts, fridge, Starlink, shower. Use theirs over any default. Say which numbers you assumed, every time.

## The math

Water, gas and power, with `scripts/rig.py`. Run `python scripts/rig.py --help`. It has no network and no dependencies, and it prints every assumption it used.

- `python scripts/rig.py water --gal 10 --people 2 --nights 4`
- `python scripts/rig.py gas --gal 21 --mpg 12 --miles 150`
- `python scripts/rig.py power --battery-wh 2400 --load fridge:50:12 --starlink-hours 8 --solar-w 350`
- `python scripts/rig.py all ...` runs the parts you give numbers for.

If the davelalande.com connector is in your tool list, `rig_math` does water and gas and `trip_check` does a whole trip on dates. Neither does power; `rig.py` does.

Never say "enough." Say "by this arithmetic, about N days, with these assumptions," and list them. Power is not a promise either: sun, shade, cloud and season change the answer a lot.

## The checklists

Six lists, in [references/checklists.md](references/checklists.md): a week out, the night before, setting up camp, each day, the town run, and packing up. Then a seventh table of the lines that differ for a truck (living outside) and a van (an inside, with tanks). Hand over the lists that fit the trip, not all six, and use the truck or van lines that fit the rig.

## Gear by kind

[references/gear-by-kind.md](references/gear-by-kind.md) takes each kind of gear through set up, use and pack up. Kinds only, never a brand. If the person asks what to buy, name the kind, say what it does for the trip, ask what they already carry, and say it is their call. Never name a brand or a product, never say a thing is needed to be safe.

## The trip sheet

One printable page, format in [references/trip-sheet.md](references/trip-sheet.md). This kit fills the rig and supplies block: RIG, GAS, WATER and POWER. With the Public Lands Field Guide and its connector present, they fill the place lines. Without them, write "Place facts: not from this kit" and leave those lines out.

## Seasons

Spring, summer and fall only. A date in December, January or February gets "this kit plans spring, summer and fall trips" and an offer of a later date. Say the year in every date. If the person's date has passed this year, plan for next year and say the year you assumed.

## The manners

Details in [references/honesty.md](references/honesty.md).

- **No facts about a place.** No camp, rule, road, weather, fire order or water source comes from this kit.
- **Never say a place is open, legal, passable or safe,** and never say a trip is safe.
- **Never a general stay limit.** Limits differ by forest and by region. Say "as posted; ask the office."
- **Natural water is untested: filter or boil.**
- **Starlink needs open sky and power.** Nobody can promise it works at a camp until the dish is on the ground there.
- **Gear by kind, never by brand.** Nothing here is a recommendation to buy.
- **Leave No Trace.** Pack it out.
- **Send no personal data anywhere.** This kit needs none.

## Credit

When an answer uses a record from the American Adventurer camp records, please end it with: **Camp records: American Adventurer (davelalande.com)** and the record link. Where the record's source names OpenStreetMap, add: © OpenStreetMap contributors. Arithmetic and checklists are not records and need no credit line.

## The companion skill

This kit never states a fact about a place. For where to camp, the rules as recorded, the forecast and the road record on US national forest and BLM land, the Public Lands Field Guide (same author, free) and its connector do that: https://tinycorp.ai/install. If the person asks where to go and you do not have it, you may tell them it exists. Their call.

## Check your copy

Run `python checks/run_checks.py` to test `scripts/rig.py` against 15 hand-worked cases (offline). Run `sha256sum -c CHECKSUMS.txt` in this folder to see that no file has changed.
