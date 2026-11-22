from flask import Flask, jsonify, render_template, send_file
from pathlib import Path
import json, csv, io, subprocess, sys

ROOT = Path(__file__).resolve().parent
app = Flask(__name__)

def load_data():
    path = ROOT / "output" / "analytics.json"
    if not path.exists():
        subprocess.run([sys.executable, str(ROOT/"scripts"/"run_local_mapreduce.py")], check=True)
    return json.loads(path.read_text(encoding="utf-8"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analytics")
def analytics():
    return jsonify(load_data())

@app.route("/api/export/routes.csv")
def export_routes():
    data = load_data()
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["route_id","route_name","passenger_boardings","observations","average_delay_minutes"])
    writer.writeheader()
    for r in data["routes"]:
        writer.writerow({"route_id":r["id"],"route_name":r["name"],"passenger_boardings":r["passengers"],
                         "observations":r["observations"],"average_delay_minutes":r["avg_delay"]})
    mem = io.BytesIO(output.getvalue().encode("utf-8"))
    mem.seek(0)
    return send_file(mem, mimetype="text/csv", as_attachment=True, download_name="bengaluru_route_analytics.csv")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
