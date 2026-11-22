#!/usr/bin/env python3
"""Hadoop Streaming reducer. Input must be sorted by mapper key."""
import sys, json

current, rows = None, []
def emit(key, values):
    if not key: return
    kind, ident = key.split("|", 1)
    n = len(values)
    passengers = sum(x["passengers"] for x in values)
    avg_delay = sum(x["delay"] for x in values) / n if n else 0
    if kind == "ROUTE":
        result = {"type":"route","id":ident,"name":values[0]["route_name"],"passengers":passengers,"observations":n,"avg_delay":round(avg_delay,2)}
    elif kind == "HOUR":
        result = {"type":"hour","hour":int(ident),"passengers":passengers,"observations":n}
    elif kind == "STOP":
        result = {"type":"stop","id":ident,"name":values[0]["stop_name"],"passengers":passengers,"observations":n,"lat":values[0]["lat"],"lon":values[0]["lon"]}
    else:
        result = {"type":"delay","bucket":ident,"observations":n}
    print(json.dumps(result, separators=(",",":")))

for line in sys.stdin:
    line = line.rstrip("\n")
    if "\t" not in line: continue
    key, raw = line.split("\t",1)
    if current is not None and key != current:
        emit(current, rows)
        rows = []
    current = key
    try: rows.append(json.loads(raw))
    except json.JSONDecodeError: pass
emit(current, rows)
