# Checklists

Short lists to hand a person. Print the ones that fit the trip. Paste them into the trip sheet (see [trip-sheet.md](trip-sheet.md)) or give them alone.

How to use them:

- These are general know-how. A checklist never states a fact about a place. Where a line needs one (a posted order, the road, a stay limit), the person asks the land manager's office, or you use the Public Lands Field Guide and its connector, which show each record's link, source and date.
- Every number here is a rule of thumb and says so. The person's own numbers are better. For real arithmetic, use `scripts/rig.py` (or `rig_math` and `trip_check` when the connector is present) and print what it assumed.
- Where a blank needs a fact about a place, write "ask <office>" and name the office.
- Gear is named by kind, never by brand.
- A box is a thing to look at, not a promise. None of these lists says a place is open, legal, passable or safe. The office and the signs on the ground have the last word.
- Spring, summer and fall trips only.

## 1. A week out

**The rig**

- [ ] Tires: tread, sidewalls and pressure, all four.
- [ ] The spare: aired up, and you can get it off the rig. The jack and lug wrench are aboard and you have used them.
- [ ] Fluids: oil, coolant, brake fluid, washer fluid. Look under the rig for drips.
- [ ] Battery terminals tight. Lights work.
- [ ] Recovery gear aboard: a shovel, a tow strap, rated recovery points on the rig, traction boards, a tire repair kit, an air compressor, work gloves.
- [ ] Fuel range: know how far your rig goes on a tank, loaded, on dirt. Use your own number. Run `scripts/rig.py gas` for the trip. Dirt and low gear burn more than pavement.

**The plan**

- [ ] Camp and a backup camp picked, so a full or closed camp is not the end of the trip.
- [ ] The dates, with the year said out loud.
- [ ] The forest's posted orders on fire, food storage and closures read on the forest's own site, then the office called to confirm. Not finding an order is not the same as there being none. (The Field Guide's `posted_orders` quotes them for the forests it reads.)
- [ ] The camp's rules read from the posting or the office: stay limit, season, fire rules. Stay limits differ by forest and by region, so use the posted one and nothing general.
- [ ] The road asked about at the ranger district: its condition today, and its Motor Vehicle Use Map. This kit holds no road facts. (The Field Guide's `road_to_camp` gives the Forest Service record of the road, not today's condition.)
- [ ] Offline maps saved to a phone or a GPS unit: the forest, the way in, the town. A paper map of the forest rides along. Ask the ranger district for its Motor Vehicle Use Map.
- [ ] Water plan: gallons aboard, people, nights. Rule of thumb: 1 gallon per person per day for drinking and cooking. That is an assumption, not a rule. Washing, a shower and hot days take more. Use your own number if you know it.
- [ ] Food planned by the meal, plus one spare day.
- [ ] Power plan: what you run (fridge, lights, phone, Starlink) and what fills the battery (solar, the alternator). Starlink is a steady draw, so count its hours.
- [ ] Starlink: it needs open sky and power. Trees and canyon walls block the dish. Nobody can see the sky at a camp from home. Nobody can say it will work at a camp until the dish is on the ground there.
- [ ] First aid kit checked and restocked. Any medicine you need, plus spare days.

## 2. The night before

- [ ] Fuel tank full. Top off again at the last pump before the dirt.
- [ ] Water full: drinking jugs, the hand-wash jug, the shower tank or the van's fresh tank.
- [ ] Forecast read for the trip dates from the National Weather Service (the connector's `forest_weather` and `trip_check` read it too). It covers about a week. A later date has no forecast yet. If it shows snow, pick other dates.
- [ ] Posted orders read again (the connector's `posted_orders` and `changes_since` help). Read what is new. Call the office in the morning.
- [ ] Wildfire reports read for the area. They are reports, not closures.
- [ ] Phone, headlamp and battery packs charged. Offline maps tested with the phone in airplane mode.
- [ ] Tell someone your plan: leave them the trip sheet. It names the forest, the camp, the backup camp, the rig, who is going, the day you will be back, and the day they should call the ranger district or the county sheriff if they have not heard from you.
- [ ] Cash or a card for the town run. Trash bags aboard.

## 3. Arriving and setting up camp

- [ ] Arrive with daylight to spare. Rule of thumb: two hours before sunset. Forest roads are slow. A common rule of thumb is about 20 mph on a fair one and 5 to 10 mph on a rough one. Your road will set its own pace.
- [ ] Read every sign and gate on the way in. A sign on the ground beats anything written elsewhere.
- [ ] Use a spot that has been used before: bare ground, an existing pullout. Do not make a new one.
- [ ] Walk the spot before you park. Engine off. Look and listen.
- [ ] Look up: no dead trees or hanging limbs over the rig or the tent.
- [ ] Level: park so you sleep level, head uphill if it is not. Your eyes decide.
- [ ] Wind: note where it comes from. The door and the kitchen go on the sheltered side. Stake the tent and the awning. Put the awning away when you leave camp or the wind comes up.
- [ ] Water: camp back from streams and lakes. The common Leave No Trace guidance is 200 feet, about 70 adult steps. The forest's own rule wins where it has one.
- [ ] Sky view for Starlink, if you carry it: an open view of the sky, away from tall trees.
- [ ] Food storage: where wildlife is around, food, coolers, trash and anything with a smell go in a hard-sided vehicle or a wildlife-resistant container, day and night. If the forest posted a food storage order, follow its words.
- [ ] Toilet: a vault toilet if the camp has one. If not, a cathole 6 to 8 inches deep and 200 feet from water, camp and trails (Leave No Trace guidance), or a pack-out toilet system. Pack out the paper.
- [ ] Hand-wash station set up: a water jug with a spigot, soap, a towel. Use it before you cook and after the toilet.
- [ ] Fire: a night with no fire is a normal night. Before any fire, read the forest's posted orders and the camp's rules, then the signs. If one is allowed and you want it: use an existing ring, keep it small, keep water and a shovel beside it.
- [ ] Write down what you set up. That list is your pack-up list.

## 4. Each day in camp

- [ ] Water check: gallons left against the plan. Gallons left, divided by (people times your daily use), is the days you have.
- [ ] Gas check: enough for the drive out and on to the pump, with a reserve. A common rule of thumb is a third out, a third back, a third in reserve. Your own numbers are better.
- [ ] Battery check: the level at sunset and at sunrise.
- [ ] Forecast, if you have a connection. Clouds building, wind rising or a creek coming up are reasons to rethink the day.
- [ ] Food and trash stored every time you leave camp, and every night.
- [ ] Treat all natural water before you drink it: filter, boil or purify.
- [ ] Count your nights against the posted stay limit.
- [ ] If water or gas runs behind the plan, move the town run up or head home early. That is a good call, not a failed trip.

## 5. The town run

A longer trip usually has one. Plan it before you leave: the nearest fuel, water, groceries and dump, from your map or the Field Guide's records. The drive is longer than a straight line. If you do not know, phone ahead.

- [ ] Before you leave camp: stow food and trash. If a tent stays to hold the site, stake it and close it.
- [ ] Fuel: fill the tank.
- [ ] Water: fill every container, the hand-wash jug, and the shower tank or the fresh tank. Ask before you use a spigot.
- [ ] Groceries and ice.
- [ ] Dump (vans and rigs with tanks): gray and black tanks at a dump station only.
- [ ] Trash: into a bin that allows it, or keep carrying it. Never leave it at camp or at a trailhead.
- [ ] Propane or stove fuel, if you are low.
- [ ] With a connection in town: read the forecast and the posted orders again, and message your contact.
- [ ] Back at camp with daylight left.

## 6. Packing up

- [ ] Gear set up is gear packed up. Go down your set-up list: tent, awning, table, chairs, stove, hand-wash station, shower, solar panels, the Starlink dish and its cable, leveling blocks, wheel chocks.
- [ ] Fire, if one was allowed and you had one: dead out. Drown it with water, stir it, feel it with the back of your hand. Repeat until it is cold. If it is too hot to touch, it is too hot to leave.
- [ ] Pack it out: all trash, food scraps and paper. Check the fire ring for trash and take that too.
- [ ] Walk-around of the site: look for the small things, such as stakes, bottle caps and twist ties.
- [ ] Walk-around of the rig: tires, nothing under it, nothing on the roof or the bumper, doors and boxes latched, the tent or the pop-top down and latched.
- [ ] Leave it a little better than you found it.
- [ ] Message your contact when you are back in range: "out and headed home."

## 7. Truck camping and van life: where the lists differ

A truck lives outside. A van has an inside and tanks. Use the lines that fit the rig.

| | Truck (living outside) | Van (an inside, with tanks) |
|---|---|---|
| Water | Jugs, and a separate hand-wash jug. Maybe a roof shower tank: one rig we know uses about 2 gallons a shower, so measure yours. A filter for creek water as a backup. | A fresh tank, filled in town. Most van campers do not put creek water in the tank. |
| Kitchen | Outside, on a table or the tailgate. Set up, cook, pack up. Wind and rain matter. | A galley inside. Sink water goes to the gray tank. |
| Toilet | A vault toilet where the camp has one, or a cathole (list 3), or a pack-out system. | The van's own toilet. The black tank or cassette is emptied at a dump station only. |
| Waste water | No tanks. Strain the dishwater, pack out the scraps, scatter the water 200 feet from streams and lakes (Leave No Trace guidance). | Gray and black tanks. Dump stations only. Add a dump stop to the town run. |
| Light | A headlamp or a flashlight. | House lights off the battery. |
| Power | A portable battery and portable panels: set out in the sun, charge, pack up before you drive or the wind rises. Fixed panels need the rig parked in the sun. | A house battery and roof panels. Shade keeps the van cool and costs charge. |
| Sleeping | A tent on the rig or on the ground. Wind and level matter more. | Inside. Level still matters. |
| Town run | Fuel, water, groceries, trash. | The same, plus the dump station. |
| Packing up | More gear outside, so a longer list. Walk it twice. | Less outside. Latch every cabinet and the fridge. |
