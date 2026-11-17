#!/usr/bin/env python3
"""rig.py - water, gas and power arithmetic for a truck or van trip. No network. Standard library only (Python 3.8+).

  rig.py water --gal 10 --people 2 [--gpd 1] [--nights 4]
  rig.py gas   --gal 21 [--mpg 13] [--miles 120]
  rig.py power --battery-wh 1200 --load fridge:50:12 --load lights:20:5 [--solar-w 200] [--sun-hours 4]
               [--solar-eff 0.7] [--usable 0.5] [--starlink-hours 8] [--starlink-w 50]
  rig.py all   (the water, gas and power flags together; each part runs if its flags are given)
  add --json to any command for machine-readable output.

Every default is an assumption and is printed under "Assumptions". The person's own numbers always win.
This is arithmetic on stated numbers. It says nothing about any place, and it never says "enough".
"""
import argparse
import json
import sys

# Defaults. Each one is printed as an assumption whenever it is used.
DEFAULT_GPD = 1.0         # gallons of water per person per day
DEFAULT_MPG = 13.0        # miles per gallon, loaded, on dirt
DEFAULT_SUN_HOURS = 4.0   # full-sun-equivalent hours a day
DEFAULT_SOLAR_EFF = 0.7   # share of panel watts that reaches the battery
DEFAULT_USABLE = 0.5      # share of battery watt-hours you will use
DEFAULT_STARLINK_W = 50.0  # average watts a Starlink dish draws


class Bad(Exception):
    pass


def num(v, name, minimum=None, positive=False):
    if v is None:
        raise Bad("%s is needed" % name)
    if positive and not v > 0:
        raise Bad("%s must be more than 0" % name)
    if minimum is not None and v < minimum:
        raise Bad("%s must be %s or more" % (name, minimum))
    return float(v)


def r(x, places=3):
    return None if x is None else round(x, places)


def water(gal, people, gpd=None, nights=None):
    assumptions = []
    gal = num(gal, "water gallons", 0)
    people = num(people, "people", positive=True)
    if gpd is None:
        gpd = DEFAULT_GPD
        assumptions.append("%g gallon per person per day (a rule of thumb for drinking and cooking; washing, a shower and hot days take more)" % gpd)
    gpd = num(gpd, "gallons per person per day", positive=True)
    per_day = people * gpd
    out = {"gallons_aboard": gal, "people": people, "gallons_per_person_per_day": gpd,
           "gallons_per_day": r(per_day), "days": r(gal / per_day)}
    if nights is not None:
        nights = num(nights, "nights", positive=True)
        need = per_day * nights
        out.update({"nights": nights, "water_needed_gal": r(need), "difference_gal": r(gal - need)})
    out["assumptions"] = assumptions
    return out


def gas(gal, mpg=None, miles=None):
    assumptions = []
    gal = num(gal, "gas gallons", 0)
    if mpg is None:
        mpg = DEFAULT_MPG
        assumptions.append("%g miles per gallon (a loaded rig on dirt; your own number is better)" % mpg)
    mpg = num(mpg, "miles per gallon", positive=True)
    rng = gal * mpg
    out = {"gallons_aboard": gal, "mpg": mpg, "range_mi": r(rng),
           "one_way_third_mi": r(rng / 3)}
    assumptions.append("one_way_third_mi uses the rule of thumb of a third out, a third back, a third in reserve")
    if miles is not None:
        miles = num(miles, "miles", positive=True)
        used = miles / mpg
        out.update({"miles_counted": miles, "gallons_needed": r(used), "gallons_left": r(gal - used),
                    "reserve_pct": r((gal - used) / gal * 100) if gal > 0 else None})
        assumptions.append("miles_counted is the total you gave, out and back; the road runs longer than a straight line")
    out["assumptions"] = assumptions
    return out


def parse_load(text):
    parts = text.split(":")
    if len(parts) != 3:
        raise Bad("a load is name:watts:hours_per_day, got %r" % text)
    try:
        watts, hours = float(parts[1]), float(parts[2])
    except ValueError:
        raise Bad("watts and hours must be numbers in %r" % text)
    if watts < 0 or hours < 0 or hours > 24:
        raise Bad("watts must be 0 or more and hours between 0 and 24 in %r" % text)
    return parts[0], watts, hours


def power(battery_wh, loads=(), solar_w=0.0, sun_hours=None, solar_eff=None, usable=None,
          starlink_hours=None, starlink_w=None):
    assumptions = []
    battery_wh = num(battery_wh, "battery watt-hours", 0)
    solar_w = num(solar_w, "solar watts", 0)
    items = [parse_load(x) for x in loads]
    if starlink_hours is not None:
        if starlink_w is None:
            starlink_w = DEFAULT_STARLINK_W
            assumptions.append("Starlink draws %g W on average while on (your dish's own number is better); it needs open sky and power" % starlink_w)
        sh = num(starlink_hours, "starlink hours", 0)
        if sh > 24:
            raise Bad("starlink hours must be 24 or less")
        items.append(("starlink", float(starlink_w), sh))
    if not items:
        raise Bad("give at least one --load or --starlink-hours")
    if usable is None:
        usable = DEFAULT_USABLE
        assumptions.append("%g of the battery's watt-hours used (a cautious rule of thumb; the maker's number is better)" % usable)
    usable = num(usable, "usable share", positive=True)
    if usable > 1:
        raise Bad("usable share must be 1 or less")
    if solar_w > 0:
        if sun_hours is None:
            sun_hours = DEFAULT_SUN_HOURS
            assumptions.append("%g full-sun hours a day (shade, cloud and season change this a lot)" % sun_hours)
        if solar_eff is None:
            solar_eff = DEFAULT_SOLAR_EFF
            assumptions.append("%g of panel watts reaches the battery (wiring, heat and angle losses)" % solar_eff)
    else:
        sun_hours = sun_hours if sun_hours is not None else 0.0
        solar_eff = solar_eff if solar_eff is not None else DEFAULT_SOLAR_EFF
    sun_hours = num(sun_hours, "sun hours", 0)
    solar_eff = num(solar_eff, "solar efficiency", 0)
    load_wh = sum(w * h for _, w, h in items)
    solar_wh = solar_w * sun_hours * solar_eff
    net = solar_wh - load_wh
    usable_wh = battery_wh * usable
    out = {"loads": [{"name": n, "watts": w, "hours_per_day": h, "wh_per_day": r(w * h)} for n, w, h in items],
           "load_wh_per_day": r(load_wh), "battery_wh": battery_wh, "usable_wh": r(usable_wh),
           "solar_w": solar_w, "solar_wh_per_day": r(solar_wh), "net_wh_per_day": r(net)}
    if net >= 0:
        out["days_on_battery"] = None
        out["note"] = "by this arithmetic the solar covers the load on a day like the one assumed, so the battery is not drawn down; cloud or shade changes that"
    else:
        out["days_on_battery"] = r(usable_wh / -net)
        out["note"] = "by this arithmetic the battery's usable watt-hours last about this many days at this daily shortfall"
    out["assumptions"] = assumptions
    return out


def build_parser():
    p = argparse.ArgumentParser(prog="rig.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("command", choices=["water", "gas", "power", "all"])
    p.add_argument("--json", action="store_true", help="print JSON")
    p.add_argument("--gal", type=float, help="gallons of water (water) or of gas (gas, all uses --water-gal and --gas-gal)")
    p.add_argument("--water-gal", type=float)
    p.add_argument("--gas-gal", type=float)
    p.add_argument("--people", type=float)
    p.add_argument("--gpd", type=float, help="gallons per person per day")
    p.add_argument("--nights", type=float)
    p.add_argument("--mpg", type=float)
    p.add_argument("--miles", type=float)
    p.add_argument("--battery-wh", type=float)
    p.add_argument("--load", action="append", default=[], help="name:watts:hours_per_day, repeatable")
    p.add_argument("--solar-w", type=float, default=0.0)
    p.add_argument("--sun-hours", type=float)
    p.add_argument("--solar-eff", type=float)
    p.add_argument("--usable", type=float)
    p.add_argument("--starlink-hours", type=float)
    p.add_argument("--starlink-w", type=float)
    return p


def run(a):
    if a.command == "water":
        return water(a.gal, a.people, a.gpd, a.nights)
    if a.command == "gas":
        return gas(a.gal, a.mpg, a.miles)
    if a.command == "power":
        return power(a.battery_wh, a.load, a.solar_w, a.sun_hours, a.solar_eff, a.usable, a.starlink_hours, a.starlink_w)
    out = {}
    if a.water_gal is not None:
        out["water"] = water(a.water_gal, a.people, a.gpd, a.nights)
    if a.gas_gal is not None:
        out["gas"] = gas(a.gas_gal, a.mpg, a.miles)
    if a.battery_wh is not None:
        out["power"] = power(a.battery_wh, a.load, a.solar_w, a.sun_hours, a.solar_eff, a.usable, a.starlink_hours, a.starlink_w)
    if not out:
        raise Bad("give --water-gal, --gas-gal or --battery-wh")
    return out


def lines(title, d):
    out = ["%s" % title]
    for k, v in d.items():
        if k == "assumptions":
            continue
        out.append("  %s: %s" % (k, v))
    return out


def text(result, command):
    parts = result if command == "all" else {command: result}
    out, assumptions = [], []
    for name, d in parts.items():
        out += lines(name.upper(), d)
        assumptions += d["assumptions"]
    out.append("ASSUMPTIONS" + ("" if assumptions else ": none used; every number was given"))
    out += ["  - " + x for x in assumptions]
    out.append("This is arithmetic on stated numbers, not a promise. Your own numbers are better.")
    return "\n".join(out)


def main(argv=None):
    a = build_parser().parse_args(argv)
    try:
        result = run(a)
    except Bad as e:
        print("rig.py: %s" % e, file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2) if a.json else text(result, a.command))
    return 0


if __name__ == "__main__":
    sys.exit(main())
