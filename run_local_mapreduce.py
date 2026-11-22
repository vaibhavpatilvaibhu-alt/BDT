#!/usr/bin/env python3
"""Run the same streaming mapper/reducer locally for development and demos."""
import subprocess, sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
data = ROOT / "data" / "trips_sample.csv"
mapper = ROOT / "scripts" / "mapper.py"
reducer = ROOT / "scripts" / "reducer.py"
out = ROOT / "output"
out.mkdir(exist_ok=True)
if not data.exists():
    subprocess.run([sys.executable, str(ROOT/"scripts"/"generate_sample_data.py")], check=True)
with data.open("rb") as f:
    mapped = subprocess.run([sys.executable, str(mapper)], stdin=f, stdout=subprocess.PIPE, check=True)
sorted_lines = b"".join(sorted(mapped.stdout.splitlines(keepends=True)))
reduced = subprocess.run([sys.executable, str(reducer)], input=sorted_lines, stdout=subprocess.PIPE, check=True)
jsonl = reduced.stdout.decode("utf-8").splitlines()
records = [json.loads(x) for x in jsonl if x.strip()]
analytics = {"data_note":"Synthetic demonstration data; not official BMTC passenger counts or delays.",
             "record_count":sum(x.get("observations",0) for x in records if x["type"]=="route"),
             "routes":[x for x in records if x["type"]=="route"],
             "hours":sorted([x for x in records if x["type"]=="hour"], key=lambda x:x["hour"]),
             "stops":[x for x in records if x["type"]=="stop"],
             "delays":[x for x in records if x["type"]=="delay"]}
(ROOT/"output"/"analytics.json").write_text(json.dumps(analytics, indent=2), encoding="utf-8")
(ROOT/"output"/"analytics.jsonl").write_text("\\n".join(jsonl)+"\\n", encoding="utf-8")
print("MapReduce complete:", len(records), "aggregate groups")
print("Output:", ROOT/"output"/"analytics.json")
