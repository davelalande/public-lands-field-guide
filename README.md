# Public Lands Field Guide

An agent skill that helps your AI plan a camping or overlanding trip on US national forest and BLM land the careful way: it shows each record's link, source and date, names what is not recorded, and never says a place is open, legal, passable or safe. It uses the free American Adventurer camp records (about 19,000 sourced camps). No sign-in, no API key.

## A 30-second look

You ask: *"Find me a free camp near Bozeman, MT for three nights in September, and a backup."*

The skill walks your agent through the order of work: land and who manages it, rules, season, road, water, town run, fire and weather, rig math, a backup camp, a last check. The answer comes back in this shape (illustrative; real answers use live records):

```
Camp: <name>, <national forest>   [record link]
Source: <where the record came from>   Record date: <date>
Cost: free, on the record's evidence   Stay limit: <as recorded, or "unrecorded">
Water: <what the record holds, nothing more>
Road: not in our records. Call the ranger district before you go.
Backup: <a second camp, with its own link and source>
Camp records: American Adventurer (davelalande.com)
```

Where the records are silent, the answer says "unrecorded" and names the office to call. The last word is always the land manager's office.

## What is in the box

| Folder | What it is |
| --- | --- |
| `skills/public-lands-field-guide/SKILL.md` | The instructions your agent reads |
| `.../scripts/aa.py` | Read-only helper for the API. Python 3.8+, standard library only |
| `.../references/` | Order of work, honesty rules, coverage, sources |
| `.../checks/` | 20 questions that test the data path (needs internet) |
| `.../CHECKSUMS.txt` | SHA-256 of every file |

The skill version is `1.1`.

## Install

The skill is one folder: `skills/public-lands-field-guide/`. Copy that folder into your tool's skills location. Locations below were checked against each tool's own docs on November 14, 2026; docs change, so check yours if it does not load.

```sh
git clone https://github.com/davelalande/public-lands-field-guide
cd public-lands-field-guide
```

**Claude Code**
- Personal (all projects): copy to `~/.claude/skills/public-lands-field-guide/`
- One project: copy to `.claude/skills/public-lands-field-guide/` in that repo

**Cursor**
- One project: `.agents/skills/public-lands-field-guide/` or `.cursor/skills/public-lands-field-guide/`
- All projects: `~/.agents/skills/` or `~/.cursor/skills/`
- Cursor also reads `.claude/skills/` and `~/.claude/skills/`.

**Codex**
- One repo: `.agents/skills/public-lands-field-guide/` (Codex scans from where you launch it up to the repo root)
- All projects: `$HOME/.agents/skills/public-lands-field-guide/`

**Kiro**
- One workspace: `.kiro/skills/public-lands-field-guide/`
- All projects: `~/.kiro/skills/public-lands-field-guide/` (IDE and CLI)

Example, Claude Code, personal:

```sh
mkdir -p ~/.claude/skills && cp -r skills/public-lands-field-guide ~/.claude/skills/
```

Check the copy is intact: `cd skills/public-lands-field-guide && sha256sum -c CHECKSUMS.txt`

## Connect the MCP (best way to use it)

The skill works best with the American Adventurer MCP connector. Address:

```
https://davelalande.com/mcp
```

**No sign in.** Add it as a remote (streamable HTTP) server in your tool. In Claude Code: `claude mcp add --transport http american-adventurer https://davelalande.com/mcp`. It is also listed in the official MCP Registry as `com.davelalande/camps`. Setup page: https://davelalande.com/ai?via=github

Without the connector, the skill falls back to `scripts/aa.py` (run `python scripts/aa.py --help`), then to plain fetches of https://davelalande.com/api/.

## What is live, and what is not

Live today (16 tools): `find_camps`, `camp_detail`, `camps_near`, `free_camping_near_town`, `plan_four_nights`, `forest_weather`, `changes_since`, `what_we_cover`, `land_at`, `rig_math`, `trip_check`, `posted_orders`, `road_to_camp`, plus three that serve the free camping game Dispersed 3D (`game_leaderboard`, `one_call`, `trip_status`).

Limits, stated plainly:
- `land_at` answers for national forests only. Anywhere else it says so and names no manager.
- `posted_orders` quotes what a forest posted on its own alerts page, for the forests we read. "Nothing posted when we read it" is not "no fire ban," and "could not read" is never "none."
- `road_to_camp` gives the Forest Service's recorded road to a camp in 20 national forests. It is the record, not today's condition. Anywhere else roads are not in the records, and the skill sends you to the office.
- Distances are straight-line miles, not drive time.
- Records are a starting point, not a promise that a place is open, legal or safe.

## Data credit

End any answer that uses a record with: **Camp records: American Adventurer (davelalande.com)** and the record link. Where a record's source names OpenStreetMap, add: (c) OpenStreetMap contributors.

## Links

- The skill page: https://davelalande.com/skill/?via=github
- Use the records from any AI: https://davelalande.com/ai?via=github

## License

Instructions and scripts: MIT, see [LICENSE](LICENSE). The camp data the skill reads is not MIT: it is free to use and copy unchanged, with the credit line above and a link to the record.
