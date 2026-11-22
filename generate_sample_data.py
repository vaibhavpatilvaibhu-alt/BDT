#!/usr/bin/env python3
"""Generate clearly-labelled synthetic Bengaluru-style transit observations."""
import csv, random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)
OUT = Path(__file__).resolve().parents[1] / "data" / "trips_sample.csv"
routes = [
    ("500D", "Hebbal - Banashankari", 12.9716, 77.5946),
    ("335E", "Shivajinagar - Whitefield", 12.9833, 77.6033),
    ("ನಮ್ಮ", "Majestic - Electronic City", 12.9767, 77.5713),
    ("G4", "Marathahalli - Kempegowda Bus Station", 12.9569, 77.7011),
    ("KIA-8", "Majestic - Airport", 13.1986, 77.7066),
    ("V-500", "Silk Board - Yeshwanthpur", 12.9177, 77.6233),
]
stops = [
    ("S001", "Majestic", 12.9767, 77.5713),
    ("S002", "Shivajinagar", 12.9833, 77.6033),
    ("S003", "Hebbal", 13.0358, 77.5970),
    ("S004", "Silk Board", 12.9177, 77.6233),
    ("S005", "Marathahalli", 12.9569, 77.7011),
    ("S006", "Banashankari", 12.9255, 77.5468),
    ("S007", "Whitefield", 12.9698, 77.7500),
    ("S008", "Electronic City", 12.8452, 77.6602),
    ("S009", "Yeshwanthpur", 13.0285, 77.5400),
    ("S010", "Airport", 13.1986, 77.7066),
]
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["trip_id","service_date","route_id","route_name","stop_id","stop_name","latitude","longitude","boarding_time","passengers","delay_minutes"])
    start = date(2025, 1, 1)
    for i in range(5000):
        route_id, route_name, _, _ = random.choice(routes)
        stop_id, stop_name, lat, lon = random.choice(stops)
        day = start + timedelta(days=random.randrange(90))
        hour = random.choices(range(5,24), weights=[1,1,2,4,8,10,9,6,4,3,3,4,5,6,8,10,9,5,2])[0]
        minute = random.randrange(60)
        passengers = max(1, int(random.gauss(24 if hour in (7,8,9,17,18,19) else 13, 7)))
        delay = max(0, int(random.gauss(8 if hour in (8,9,18,19) else 4, 5)))
        w.writerow([f"T{i+1:05d}",day.isoformat(),route_id,route_name,stop_id,stop_name,lat,lon,f"{hour:02d}:{minute:02d}:00",passengers,delay])
print(f"Wrote {OUT} (synthetic demo records)")
