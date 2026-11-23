# Changelog

Two skills live in this repo, each with its own version (the `metadata.version` line in its `SKILL.md`). Each release is also a git tag: `field-guide-v1.3.0`, `trip-kit-v1.0.1`.

## Claude Code plugin

### 1.0.0 (2026-11-20)
- The repo is now a Claude Code plugin and marketplace, `national-forest-overlanding`: one command installs both skills (as they sit in `skills/`, no second copy) and the American Adventurer connector (`https://davelalande.com/mcp`, no sign-in). The skills themselves are unchanged.

## Public Lands Field Guide

### 1.4.1 (2026-11-23)
- Step 2 of the order of work now names the area-wide stay rule itself (Montana national forests 16 days on one site, order R1-2025-01; Region 1 Idaho forests and the Dakota Prairie Grasslands 14 days; BLM 14 days in any 28; unless posted; the forest's own posted order wins), so an answer cites the order without opening references/order-of-work.md. No other change.

### 1.4.0 (2026-11-20)
- `aa.py` calls the seven connector tools it used to skip: `trip_check`, `rig_math`, `posted_orders`, `road_to_camp`, `land_at`, `changes_since` and `what_we_cover` (`trip-check`, `rig`, `orders`, `road`, `land-at`, `changes`, `coverage`). Same envelope. A null field is unrecorded. `rig_math` reads no record, so its record date stays unrecorded.
- Two short sections: toilets and resupply, and water. Natural water stays "untested: filter or boil."
- The checks exercise those seven subcommands live. 34 checks.
- Stay limits: when a record names none, or someone asks in general, quote the area-wide rule with its order (Montana national forests 16 days on one site, R1-2025-01; Region 1 Idaho and the Dakota Prairie 14; BLM 14), never a number from memory. The description now says "how long you can stay" so the skill is picked for that question.
- The shared trip sheet (both skills) names the `aa.py` commands that reach the connector tools.

### 1.3.1 (2026-11-18)
- The tool list now names all 18 connector tools, `water_near` and `nearby` included (it still said 16). No change to how the skill works.

### 1.3.0 (2026-11-17)
- Water near a camp: springs, hot springs, waterfalls, lakes, creeks and Forest Service fill points, each with its government sources (Montana's game forests and every Oregon national forest). Natural water is always "untested: filter or boil". (`aa.py water`, the connector's `water_near`)
- The nearest recorded toilets (21,390 on public land) and resupply nearby: drinking water, showers, dump stations, fuel, groceries, propane, laundry. (`aa.py toilets`, `aa.py poi`, the connector's `nearby`)
- Coffee for the town run: 22,954 cafes, only those within 25 straight-line miles of a camp record. (`aa.py poi LAT LON coffee`, `nearby` kind coffee)
- Works with all 18 connector tools.
- The checks run `aa.py` in the same process (no subprocess); every `--summary` names the record it came from. 27 checks.

### 1.2.0 (2026-11-17)
- Printable trip sheet, before-you-go list, the tool menu and the dates rule; `posted_orders` (a forest's posted alerts and orders) and `road_to_camp` (the recorded Forest Service road).
- License MIT-0: credit is welcome, never required.

### 1.1.0 (2026-11-16)
- First public release: national forest and BLM camping from sourced camp records, with the connector's tools listed.

## Overland Trip Kit

### 1.0.3 (2026-11-20)
- The shared trip sheet says the Field Guide's `aa.py` (1.4 or newer) reaches the connector tools when the connector is missing. No other change.

### 1.0.2 (2026-11-18)
- A version line ClawHub can read; no change to the skill itself.

### 1.0.1 (2026-11-17)
- The checks run `rig.py` in the same process (no subprocess). 15 offline cases.

### 1.0.0 (2026-11-17)
- Rig card, six checklists, gear by kind, a printable trip sheet, and `rig.py` water, gas and power math with its assumptions stated. MIT-0.
