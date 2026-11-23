#!/usr/bin/env python3
"""aa.py - read-only calls to the American Adventurer keyless API and its MCP connector.

Python standard library only. Makes HTTPS GET requests to https://davelalande.com
and HTTPS POST requests to https://davelalande.com/mcp (JSON-RPC tools/call, no key).
Sends no personal data: neither one needs any.

Every output keeps what you must show a reader: the record url, the source, and
the record date, where the call returns them. The data is printed as it was sent,
inside a small envelope.

  aa.py root
  aa.py find "hyalite" [--state MT] [--cost free|fee] [--water] [--forest ORGCODE]
                       [--rules] [--open YYYY-MM-DD|today] [--limit 10]
  aa.py camp SLUG [--date YYYY-MM-DD]
  aa.py near LAT LON [--radius 25] [--cost free|fee] [--limit 10]
  aa.py poi LAT LON CATEGORY [--radius 25]      (fuel, grocery, potable_water, dump_station, coffee, ...)
  aa.py town "Bozeman" [--state MT] [--radius 25] [--limit 5]   (free camps near a town)
  aa.py forest "gallatin"                       (search; or give a slug for the record)
  aa.py land "adirondack"                       (named state lands that are not national forests)
  aa.py weather LAT LON                         (National Weather Service forecast, via the API)
  aa.py fire LAT LON                            (wildfire reports near a point, via the API)
  aa.py trip-check --start YYYY-MM-DD [--forest SLUG] [--camp SLUG] [--nights N]
                   [--rig truck|van|custom] [--tank-gal N] [--water-gal N]
                   [--pump-paved-mi N] [--pump-unpaved-mi N]
  aa.py rig WATER_GAL GAS_GAL PEOPLE [--nights N] [--mpg N] [--water-gal-per-person-per-day N]
  aa.py orders FOREST
  aa.py road SLUG RIG [--date YYYY-MM-DD]       (RIG: car, SUV, high-clearance, van, truck)
  aa.py land-at LAT LON                         (national forests only)
  aa.py changes CAMP [CAMP ...] --since YYYY-MM-DD   (one to three camps)
  aa.py coverage [--job WORD]

Add --summary BEFORE the command (aa.py --summary camp SLUG) for a short plain-text
summary instead of JSON.
All distances are straight-line miles. A null or missing field means UNRECORDED.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://davelalande.com"
MCP = BASE + "/mcp"
UA = "aa-skill/1 (+https://davelalande.com/skill/)"
CREDIT = "Camp records: American Adventurer (davelalande.com)"
OSM = "Where a record's source names OpenStreetMap, also credit: (c) OpenStreetMap contributors (ODbL)."
PACE = 0.5  # seconds between calls: the site asks for about two requests a second
_last = [0.0]
_mcp_session = [None]   # Mcp-Session-Id, sent back only after the server returns one
_mcp_version = [None]   # protocol version the server agreed to at initialize
_mcp_ready = [False]
_rpc_id = [0]


def _pace():
    wait = PACE - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()


def get(path, params=None):
    """GET one API address. Returns (url, parsed_json). Retries once on 429/5xx."""
    url = BASE + path
    if params:
        clean = {k: v for k, v in params.items() if v not in (None, "", False)}
        if clean:
            url += "?" + urllib.parse.urlencode(clean)
    last_err = None
    for attempt in range(2):
        _pace()
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return url, json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            last_err = "HTTP %s from %s" % (e.code, url)
            if e.code in (429, 500, 502, 503, 504) and attempt == 0:
                time.sleep(3)
                continue
            break
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            last_err = "could not read %s (%s)" % (url, e)
            if attempt == 0:
                time.sleep(3)
                continue
            break
    # A failed read is "could not read", never "none".
    sys.exit("ERROR: " + str(last_err) + ". Could not read; that is not the same as none.")


def _parse_mcp(raw, content_type, want_id):
    """One JSON-RPC message from a JSON body or a text/event-stream body."""
    text = raw.decode("utf-8").strip()
    if not text:
        return None
    ct = (content_type or "").lower()
    streamed = "text/event-stream" in ct or text.startswith("data:") or text.startswith("event:")
    if not streamed:
        return json.loads(text)
    found = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("data:"):
            continue
        chunk = line[5:].strip()
        if not chunk or chunk == "[DONE]":
            continue
        try:
            found.append(json.loads(chunk))
        except ValueError:
            continue
    if want_id is not None:
        for item in found:
            if isinstance(item, dict) and item.get("id") == want_id:
                return item
    for item in reversed(found):
        if isinstance(item, dict) and ("result" in item or "error" in item):
            return item
    if found:
        return found[-1]
    raise ValueError("event-stream had no JSON data")


def _mcp_post(method, params=None, notify=False):
    """One POST to the connector. Returns the JSON-RPC message, or None for an empty reply."""
    _rpc_id[0] += 1
    payload = {"jsonrpc": "2.0", "method": method}
    want_id = None
    if not notify:
        want_id = _rpc_id[0]
        payload["id"] = want_id
    if params is not None:
        payload["params"] = params
    body = json.dumps(payload).encode("utf-8")
    last_err = None
    for attempt in range(2):
        _pace()
        headers = {
            "User-Agent": UA,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if _mcp_session[0]:
            headers["Mcp-Session-Id"] = _mcp_session[0]
        if _mcp_version[0]:
            headers["MCP-Protocol-Version"] = _mcp_version[0]
        req = urllib.request.Request(MCP, data=body, method="POST", headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                sid = r.headers.get("Mcp-Session-Id")
                if sid:
                    _mcp_session[0] = sid
                return _parse_mcp(r.read(), r.headers.get("Content-Type"), want_id)
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = e.read().decode("utf-8", "replace")[:300]
            except Exception:
                pass
            last_err = "HTTP %s from %s %s" % (e.code, MCP, detail)
            if e.code in (429, 500, 502, 503, 504) and attempt == 0:
                time.sleep(3)
                continue
            break
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            last_err = "could not read %s (%s)" % (MCP, e)
            if attempt == 0:
                time.sleep(3)
                continue
            break
    sys.exit("ERROR: " + str(last_err) + ". Could not read; that is not the same as none.")


def _mcp_ready_session():
    if _mcp_ready[0]:
        return
    msg = _mcp_post("initialize", {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "aa-skill", "version": "1.4.0"},
    })
    if not isinstance(msg, dict) or msg.get("error") or "result" not in msg:
        detail = msg.get("error") if isinstance(msg, dict) else msg
        sys.exit("ERROR: connector initialize failed (%s). Could not read; that is not the same as none." % detail)
    agreed = (msg.get("result") or {}).get("protocolVersion") or "2025-03-26"
    _mcp_version[0] = agreed
    note = _mcp_post("notifications/initialized", notify=True)
    if isinstance(note, dict) and note.get("error"):
        sys.exit("ERROR: connector initialize failed (%s). Could not read; that is not the same as none." % note.get("error"))
    _mcp_ready[0] = True


def _mcp_object(result):
    """The tool's object: structuredContent, or JSON parsed from the text content."""
    if not isinstance(result, dict):
        sys.exit("ERROR: the connector returned no result. Could not read; that is not the same as none.")
    if result.get("isError"):
        text = ""
        for item in result.get("content") or []:
            if isinstance(item, dict) and item.get("text"):
                text = item["text"]
                break
        sys.exit("ERROR: the connector could not answer (%s). Could not read; that is not the same as none." % (text[:300] or "isError"))
    data = result.get("structuredContent")
    if isinstance(data, dict):
        return data
    text = ""
    for item in result.get("content") or []:
        if isinstance(item, dict) and item.get("type") == "text" and item.get("text"):
            text = item["text"]
            break
    if not text:
        sys.exit("ERROR: the connector returned nothing we could read. Could not read; that is not the same as none.")
    try:
        parsed = json.loads(text)
    except ValueError:
        parsed = {"text": text}
    if not isinstance(parsed, dict):
        parsed = {"data": parsed}
    return parsed


def mcp_call(name, arguments):
    """Call one connector tool. Returns (url, object). Argument names are the tool's own."""
    _mcp_ready_session()
    msg = _mcp_post("tools/call", {"name": name, "arguments": arguments or {}})
    if not isinstance(msg, dict) or msg.get("error") or "result" not in msg:
        detail = msg.get("error") if isinstance(msg, dict) else msg
        sys.exit("ERROR: %s. Could not read; that is not the same as none." % detail)
    return MCP, _mcp_object(msg["result"])


def _filled(value):
    return value.strip() if isinstance(value, str) and value.strip() else None


def _http_url(value):
    text = _filled(value)
    return text if text and text.startswith("http") else None


def tool_record_url(data, fallback):
    """A record url the tool itself returned, or the connector address."""
    found = _http_url(data.get("camp_record"))
    if found:
        return found
    recs = data.get("records")
    if isinstance(recs, list) and recs and isinstance(recs[0], dict):
        found = _http_url(recs[0].get("url"))
        if found:
            return found
    place = data.get("place")
    if isinstance(place, dict):
        found = _http_url(place.get("page"))
        if found:
            return found
    src = data.get("source")
    if isinstance(src, dict):
        for key in ("file", "page", "record"):
            found = _http_url(src.get(key))
            if found:
                return found
    found = _http_url(data.get("alerts_page"))
    if found:
        return found
    office = data.get("office")
    if isinstance(office, dict):
        found = _http_url(office.get("page"))
        if found:
            return found
    return fallback


def tool_source(data):
    """The source line the tool itself returned, or None when it named none."""
    src = data.get("source")
    if isinstance(src, str):
        return _filled(src)
    if isinstance(src, dict):
        bits = []
        for key in ("file", "page", "record"):
            text = _filled(src.get(key))
            if text:
                bits.append(text)
        if bits:
            return "; ".join(bits)
    land = data.get("land")
    if isinstance(land, dict):
        text = _filled(land.get("source"))
        if text:
            return text
    by = data.get("brought_to_you_by")
    if isinstance(by, dict):
        return _filled(by.get("source_line"))
    return None


def tool_record_date(data):
    """The record date the tool itself returned, or None when it named none."""
    recs = data.get("records")
    if isinstance(recs, list) and recs and isinstance(recs[0], dict):
        found = _filled(recs[0].get("record_date"))
        if found:
            return found
    by = data.get("brought_to_you_by")
    if isinstance(by, dict):
        m = re.search(r"data built (\S+)", by.get("source_line") or "")
        if m:
            return m.group(1)
    found = _filled(data.get("as_of"))
    if found:
        return found
    cov = data.get("coverage")
    if isinstance(cov, dict):
        found = _filled(cov.get("as_of"))
        if found:
            return found
    office = data.get("office")
    if isinstance(office, dict):
        found = _filled(office.get("read_at"))
        if found:
            return found
    found = _filled(data.get("read_at"))       # posted_orders (11/22 on): the alerts page read time sits at the top level
    if found:
        return found
    land = data.get("land")
    if isinstance(land, dict):
        found = _filled(land.get("source_date"))
        if found:
            return found
    found = _filled(data.get("last_good_read"))
    if found:
        return found
    forecast = data.get("forecast")
    if isinstance(forecast, dict):
        return _filled(forecast.get("fetched_at"))
    return None


def present(pairs):
    """Drop arguments the person did not give. Never send a key the tool was not given."""
    out = {}
    for key, value in pairs:
        if value is None or value == "":
            continue
        out[key] = value
    return out


def record_date(data):
    """The record date the API states: 'data built ...' in its cite line, or its own date field."""
    pub = data.get("publisher") if isinstance(data, dict) else None
    if isinstance(pub, dict):
        m = re.search(r"data built (\S+)", pub.get("cite", ""))
        if m:
            return m.group(1)
    for k in ("updated", "generated", "data_built_at"):
        if isinstance(data, dict) and data.get(k):
            return data[k]
    src = data.get("source") if isinstance(data, dict) else None
    if isinstance(src, dict) and src.get("newest_record_date"):     # /api/water (11/17): the newest record date in the answer
        return src["newest_record_date"]
    return None


def envelope(url, data, source=None):
    d = dict(data) if isinstance(data, dict) else {"data": data}
    d.pop("publisher", None)  # replaced by the credit line below
    src = source or (data.get("source") if isinstance(data, dict) and isinstance(data.get("source"), str) else None)
    return {
        "request_url": url,
        "source": src or "American Adventurer records (davelalande.com); the record's own source is named inside",
        "record_date": record_date(data),
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "credit": CREDIT,
        "osm_note": OSM,
        "distance_unit": "straight-line miles",
        "unrecorded_rule": "A null or missing field is UNRECORDED. Do not estimate it.",
        "data": d,
    }


def fmt_camp(c):
    bits = [c.get("name", "?"), "(%s)" % c.get("state", "?"), c.get("cost", "unrecorded cost"),
            c.get("land_manager") or "manager unrecorded"]
    if c.get("miles") is not None:
        bits.append("%s mi straight-line" % c["miles"])
    r = c.get("rules") or {}
    if r.get("stay_limit_days") is not None:
        bits.append("stay limit %s days" % r["stay_limit_days"])
    elif r.get("stay_limit_status"):
        bits.append("stay limit: %s" % r["stay_limit_status"])
    else:
        bits.append("stay limit unrecorded")
    bits.append("water on record" if c.get("water") else "no water recorded")
    return " | ".join(str(b) for b in bits) + "\n    url: " + str(c.get("url"))


def summarize(env):
    d = env["data"]
    out = []
    if "camp" in d:
        out.append(fmt_camp(d["camp"]))
        s = d["camp"].get("season")
        if s:
            out.append("  season on %s: %s. %s" % (s.get("state_on"), s.get("state"), s.get("why")))
        else:
            out.append("  season: unrecorded")
    elif "camps" in d:
        out.append("%s camps match (showing %d)" % (d.get("total", "?"), len(d["camps"])))
        out += ["  " + fmt_camp(c) for c in d["camps"]]
    elif "forests" in d:
        for f in d["forests"]:
            out.append("%s | states %s | %s camps | %s" % (f["name"], f.get("states"), f.get("camp_count"), f.get("url")))
    elif "forest" in d:
        f = d["forest"]
        out.append("%s | %s camps | %s free | url: %s" % (f["name"], f.get("camps_in_corpus"), f.get("camps_free"), f.get("url")))
    elif "lands" in d:
        for l in d["lands"]:
            out.append("%s | %s | %s" % (l.get("name"), l.get("kind"), l.get("url")))
    elif "periods" in d:
        out.append("Forecast near %s (NWS)" % d.get("nearest"))
        for p in d["periods"][:6]:
            out.append("  %s: %s F, %s, wind %s" % (p["name"], p["temp"], p["short"], p["wind"]))
        out.append("  Only plan spring, summer and fall trips. A snow forecast means not this trip.")
    elif "fires" in d:
        out.append("%s wildfire reports, %s planned burns. Reports only: not perimeters, closures or restrictions." % (d.get("fire_count"), d.get("rx_count")))
        for f in d["fires"][:5]:
            out.append("  %s | %s acres | %s mi %s%s" % (f["name"], f["acres"], f["mi"], f["dir"], " | planned burn" if f.get("rx") else ""))
    elif d.get("type") == "poi":
        out.append("%s %s points within %s mi (a floor, never a survey)" % (d.get("total"), d.get("category"), d.get("radius_miles")))
    elif isinstance(d.get("summary"), str):
        out.append(d["summary"])
    else:
        out.append(json.dumps(d)[:400])
    shown_date = env["record_date"] if env.get("record_date") else "UNRECORDED"
    out.append("record: %s" % env.get("request_url"))      # every summary names the exact record it came from
    out.append("source: %s | record date: %s | fetched: %s" % (env["source"], shown_date, env["fetched_at"]))
    out.append(env["credit"] + ". " + env["osm_note"])
    return "\n".join(out)


def keep_cost(data, cost, limit):
    """/api/near ignores a cost filter (checked 2026-11-11), so filter here and say so."""
    camps = data.get("camps", [])
    if cost:
        camps = [c for c in camps if c.get("cost") == cost]
        data["filtered_here"] = "Kept only camps whose cost verdict is %r, from the nearest %d returned by /api/near; the API's own total counts all costs." % (cost, len(data.get("camps", [])))
    data["camps"] = camps[:limit]


def find_town(name, state):
    url, data = get("/towns.json")
    want = name.strip().lower()
    hits = [t for t in data["towns"] if t[2].lower() == want and (not state or t[3].upper() == state.upper())]
    if not hits:
        sys.exit("ERROR: no town named %r%s in towns.json. Try find or near with coordinates." % (name, " in " + state if state else ""))
    hits.sort(key=lambda t: -(t[4] or 0))
    return hits[0]


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Read-only calls to the American Adventurer API and its MCP connector.")
    p.add_argument("--summary", action="store_true", help="short plain-text summary instead of JSON")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("root")
    s = sub.add_parser("find"); s.add_argument("q"); s.add_argument("--state"); s.add_argument("--cost", choices=["free", "fee", "unpriced"])
    s.add_argument("--water", action="store_true"); s.add_argument("--forest"); s.add_argument("--rules", action="store_true")
    s.add_argument("--open", dest="open_"); s.add_argument("--limit", type=int, default=10)
    s = sub.add_parser("camp"); s.add_argument("slug"); s.add_argument("--date")
    s = sub.add_parser("near"); s.add_argument("lat"); s.add_argument("lon"); s.add_argument("--radius", default="25")
    s.add_argument("--cost", choices=["free", "fee", "unpriced"]); s.add_argument("--limit", type=int, default=10)
    s = sub.add_parser("poi"); s.add_argument("lat"); s.add_argument("lon"); s.add_argument("category"); s.add_argument("--radius", default="25")
    s = sub.add_parser("toilets"); s.add_argument("lat"); s.add_argument("lon"); s.add_argument("--radius", default="25"); s.add_argument("--limit", type=int, default=5)
    s = sub.add_parser("water"); s.add_argument("lat"); s.add_argument("lon"); s.add_argument("--radius", default="10"); s.add_argument("--type", help="spring, hot_spring, waterfall, lake, reservoir, river, creek or fill_point"); s.add_argument("--limit", type=int, default=10)
    s = sub.add_parser("town"); s.add_argument("name"); s.add_argument("--state"); s.add_argument("--radius", default="25"); s.add_argument("--limit", type=int, default=5)
    s = sub.add_parser("forest"); s.add_argument("q")
    s = sub.add_parser("land"); s.add_argument("q")
    s = sub.add_parser("weather"); s.add_argument("lat"); s.add_argument("lon")
    s = sub.add_parser("fire"); s.add_argument("lat"); s.add_argument("lon")
    # Argument names below are the connector's input schema from tools/list on 2026-11-20.
    s = sub.add_parser("trip-check")
    s.add_argument("--start", required=True)
    s.add_argument("--forest"); s.add_argument("--camp"); s.add_argument("--nights", type=int)
    s.add_argument("--rig", choices=["truck", "van", "custom"])
    s.add_argument("--tank-gal", type=float); s.add_argument("--water-gal", type=float)
    s.add_argument("--pump-paved-mi", type=float); s.add_argument("--pump-unpaved-mi", type=float)
    s = sub.add_parser("rig")
    s.add_argument("water_gal", type=float); s.add_argument("gas_gal", type=float); s.add_argument("people", type=int)
    s.add_argument("--nights", type=int); s.add_argument("--mpg", type=float)
    s.add_argument("--water-gal-per-person-per-day", type=float, dest="water_gal_per_person_per_day")
    s = sub.add_parser("orders"); s.add_argument("forest")
    s = sub.add_parser("road"); s.add_argument("camp")
    s.add_argument("rig", choices=["car", "SUV", "high-clearance", "van", "truck"]); s.add_argument("--date")
    s = sub.add_parser("land-at"); s.add_argument("lat", type=float); s.add_argument("lon", type=float)
    s = sub.add_parser("changes"); s.add_argument("camps", nargs="+"); s.add_argument("--since", required=True)
    s = sub.add_parser("coverage"); s.add_argument("--job")
    a = p.parse_args(argv)

    source = None
    if a.cmd == "root":
        url, data = get("/api/")
    elif a.cmd == "find":
        url, data = get("/api/camps", {"q": a.q, "state": a.state, "cost": a.cost, "water": 1 if a.water else None,
                                       "forest": a.forest, "rules": 1 if a.rules else None, "open": a.open_, "limit": a.limit})
    elif a.cmd == "camp":
        url, data = get("/api/camps/" + urllib.parse.quote(a.slug), {"date": a.date})
    elif a.cmd == "near":
        url, data = get("/api/near", {"lat": a.lat, "lon": a.lon, "radius": a.radius, "limit": 100 if a.cost else a.limit})
        keep_cost(data, a.cost, a.limit)
    elif a.cmd == "poi":
        url, data = get("/api/near", {"lat": a.lat, "lon": a.lon, "radius": a.radius, "type": "poi", "cat": a.category})
    elif a.cmd == "water":        # 11/17: the water records (Montana game forests + every Oregon national forest), nearest first, each with its sources
        url, data = get("/api/water", {"lat": a.lat, "lon": a.lon, "radius": a.radius, "type": a.type, "limit": a.limit})
    elif a.cmd == "toilets":      # 11/17 (Dave: "Does our skill help you with finding a toilet?"): the 21,390 recorded toilets, nearest first
        url, data = get("/api/near", {"lat": a.lat, "lon": a.lon, "radius": a.radius, "type": "toilets", "limit": a.limit})
    elif a.cmd == "town":
        lat, lon, name, st, _ = find_town(a.name, a.state)
        url, data = get("/api/near", {"lat": lat, "lon": lon, "radius": a.radius, "limit": 100})
        keep_cost(data, "free", a.limit)
        data["town"] = {"name": name, "state": st, "lat": lat, "lon": lon, "source": "davelalande.com/towns.json"}
    elif a.cmd == "forest":
        if "-" in a.q and re.fullmatch(r"[a-z0-9-]+", a.q):
            url, data = get("/api/forests/" + a.q)
        else:
            url, data = get("/api/forests", {"q": a.q, "limit": 10})
    elif a.cmd == "land":
        url, data = get("/api/lands", {"q": a.q, "limit": 10})
    elif a.cmd == "weather":
        url, data = get("/api/weather", {"lat": a.lat, "lon": a.lon})
        source = "National Weather Service (weather.gov), via davelalande.com/api/weather"
    elif a.cmd == "fire":
        url, data = get("/api/fire", {"lat": a.lat, "lon": a.lon})
        source = "NIFC wildfire incident reports, via davelalande.com/api/fire (reports, not perimeters or restrictions)"
    elif a.cmd == "trip-check":
        url, data = mcp_call("trip_check", present([
            ("forest", a.forest), ("camp", a.camp), ("start", a.start), ("nights", a.nights),
            ("rig", a.rig), ("tank_gal", a.tank_gal), ("water_gal", a.water_gal),
            ("pump_paved_mi", a.pump_paved_mi), ("pump_unpaved_mi", a.pump_unpaved_mi),
        ]))
    elif a.cmd == "rig":
        url, data = mcp_call("rig_math", present([
            ("water_gal", a.water_gal), ("gas_gal", a.gas_gal), ("people", a.people),
            ("nights", a.nights), ("mpg", a.mpg),
            ("water_gal_per_person_per_day", a.water_gal_per_person_per_day),
        ]))
    elif a.cmd == "orders":
        url, data = mcp_call("posted_orders", {"forest": a.forest})
    elif a.cmd == "road":
        url, data = mcp_call("road_to_camp", present([("camp", a.camp), ("rig", a.rig), ("date", a.date)]))
    elif a.cmd == "land-at":
        url, data = mcp_call("land_at", {"lat": a.lat, "lon": a.lon})
    elif a.cmd == "changes":
        if len(a.camps) > 3:
            sys.exit("ERROR: changes takes one to three camps (the connector's own limit).")
        url, data = mcp_call("changes_since", {"camps": a.camps, "since": a.since})
    elif a.cmd == "coverage":
        url, data = mcp_call("what_we_cover", present([("job", a.job)]))
    else:
        sys.exit("ERROR: unknown command %r. Could not read; that is not the same as none." % a.cmd)
    env = envelope(url, data, source)
    if a.cmd in ("trip-check", "rig", "orders", "road", "land-at", "changes", "coverage"):
        env["request_url"] = tool_record_url(data, url)
        named = tool_source(data)
        if named:
            env["source"] = named
        env["record_date"] = tool_record_date(data)
    print(summarize(env) if a.summary else json.dumps(env, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
