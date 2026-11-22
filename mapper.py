#!/usr/bin/env python3
"""Hadoop Streaming mapper. Emits key<TAB>JSON value records."""
import sys, csv, json

def delay_bucket(delay):
    if delay <= 5: return "0-5 min"
    if delay <= 15: return "6-15 min"
    return "16+ min"

reader = csv.DictReader(sys.stdin)
for row in reader:
    try:
        route = row["route_id"]
        hour = row["boarding_time"][:2]
        stop = row["stop_id"]
        passengers = int(float(row["passengers"]))
        delay = float(row["delay_minutes"])
        payload = {"passengers": passengers, "delay": delay,
                   "route_name": row["route_name"], "stop_name": row["stop_name"],
                   "lat": float(row["latitude"]), "lon": float(row["longitude"])}
        for key in (f"ROUTE|{route}", f"HOUR|{hour}", f"STOP|{stop}", f"DELAY|{delay_bucket(delay)}"):
            print(f"{key}\t{json.dumps(payload, separators=(',', ':'))}")
    except (KeyError, ValueError, TypeError):
        continue
