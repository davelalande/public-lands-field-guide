# What you can ask for

A short menu. Show it when someone asks "what can you do?", or is new to overlanding and does not know where to start. Offer two or three that fit what they said, not the whole list.

Everything here is about the rig and the supplies, never about a place. Trips are planned for spring, summer and fall.

| Ask for | A camper would say | What you do |
|---|---|---|
| How long the water lasts | "I have 10 gallons for two of us. How many days is that?" | `scripts/rig.py water`. Print the assumptions. "By this arithmetic, about 5 days at 1 gallon each a day." Never "enough." |
| How much water to carry | "How much water should we bring for four nights?" | Ask the people and their own daily use. `rig.py water --nights` gives the gallons the arithmetic needs; say the rate you used. |
| A gas check | "I have a 21 gallon tank. How far does that go?" | `rig.py gas` with their mpg. The range, a third out, a third back, a third in reserve, with the assumptions. |
| A battery and solar budget | "Will my battery run the fridge for two days?" | `rig.py power` with the loads they give. Say how many days by this arithmetic, and what you assumed about sun. |
| Starlink power | "Can I run Starlink off my battery?" | Count it as a steady draw in `rig.py power --starlink-hours`. Say it needs open sky and power, and that nobody can promise it works at a camp. |
| The rig card | "Help me work out my numbers." | Ask the ten lines in rig-card.md, once. |
| A packing or camp checklist | "What should I check on the truck before I go?" | The lists in checklists.md. Use the truck or van lines that fit, and hand over only the lists that fit the trip. |
| Gear by kind | "What do I need for a camp kitchen?" | The kinds in gear-by-kind.md, each as set up, use, pack up. Kinds only, never a brand. |
| A trip sheet | "Give me a one-page plan I can print and leave with my wife." | The format in trip-sheet.md. Without the Public Lands Field Guide, the place lines say "not from this kit." |
| The town run | "What should I do on the town run?" | The town run list in checklists.md. |
| Packing up | "What do I do when I leave camp?" | The packing up list in checklists.md. |

What to say plainly when it comes up:

- This kit holds no facts about any place: no camps, rules, roads, weather or fire orders. For those, the Public Lands Field Guide and its connector do that work (SKILL.md says where to find them); otherwise the land manager's office does.
- It never says a trip is safe, and never says a place is open, legal or passable.
- A date in December, January or February gets "this kit plans spring, summer and fall trips" and an offer of a later date.
