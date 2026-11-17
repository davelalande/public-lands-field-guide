# The rig card

The person's rig in ten lines. Ask for these once, at the start of a trip plan. Write the answers down and use them for every number after. A number the person gives always beats a default. If they do not know one, say which default you used and that you used it.

Do not ask for all ten if the question needs three. A water question needs lines 3 and 4. A gas question needs lines 1 and 2. A power question needs 5 to 9.

| # | Line | What to ask | Where it goes |
|---|---|---|---|
| 1 | Gas tank | "How many gallons does your tank hold?" | `rig.py gas --gal` |
| 2 | Miles per gallon, loaded, on dirt | "What do you really get, loaded, on a dirt road? Your own number from a fill-up is best." | `rig.py gas --mpg` (default 13, an assumption) |
| 3 | Water aboard | "How many gallons of water do you carry, all containers and tanks together?" | `rig.py water --gal` |
| 4 | People | "How many of you will use the water?" And how many nights. | `rig.py water --people --nights` |
| 5 | Battery watt-hours | "What is the house battery's size? Amp-hours times volts gives watt-hours (200 amp-hours at 12 volts is 2,400)." | `rig.py power --battery-wh` |
| 6 | Solar watts | "How many watts of panels, fixed or portable? Zero is fine." | `rig.py power --solar-w` |
| 7 | Fridge | "Is there a powered fridge or cooler? Roughly how many watts does it draw while running, and how many hours a day does it run?" | a `--load fridge:watts:hours` |
| 8 | Starlink | "Do you carry Starlink? How many hours a day would it be on?" | `--starlink-hours` (default 50 W, an assumption) |
| 9 | Other loads | "Lights, a fan, phones, a laptop, a heater: watts and hours a day for each, roughly." | more `--load name:watts:hours` |
| 10 | Shower and wash water | "Do you carry a shower tank? How much does one shower take?" | counts against line 3 |

The usable share of the battery (default 0.5, cautious), the full-sun hours (default 4) and the share of panel watts that reaches the battery (default 0.7) are assumptions too. Offer the person a chance to give their own.

## Two examples

These are one rig we know of each kind, to show the shape. Do not offer them as the person's numbers.

**A truck (living outside).** Water in jugs, and a separate hand-wash jug. A roof shower tank of about 4 gallons, using about 2 gallons a shower. Two house batteries of 100 amp-hours each (200 amp-hours, so about 2,400 watt-hours at 12 volts). Two fixed panels of 175 watts each (350 watts). A portable battery with two portable panels for the Starlink dish. A 12-volt fridge-freezer. Tank size and miles per gallon: the person's own, from a fill-up.

**A van (an inside, with tanks).** A fresh water tank filled in town; van campers use creek water only to bathe or fish. A 15-gallon gray water tank, emptied at a dump station only. A 400 amp-hour lithium bank (watt-hours are 400 times the bank's voltage). Two roof panels, 400 watts together. A 70-liter compressor fridge. A diesel air heater for a cool spring or fall night. Tank size and miles per gallon: the person's own.

## What the card is not

It is not a promise about the rig and it is not advice to buy anything. It holds the person's numbers so the arithmetic is theirs.
