# Bengaluru Transit Analytics
A reproducible public-transport analytics dashboard using Python, Hadoop Streaming MapReduce, Flask, Plotly-style Chart.js visualisations and Leaflet maps.

## Important data note
`data/trips_sample.csv` is **synthetic demonstration data** generated for this project. It is not official BMTC passenger-count, GPS or delay data. Route/stop coordinates are illustrative Bengaluru locations. Replace the sample with verified/licensed source data before making real-world claims.

## Features
- KPI summary: passenger boardings, trips, routes, stops and average delay
- Route-wise passenger totals and delay summaries
- Hourly passenger-demand profile
- Stop-wise passenger totals and map
- Delay category distribution
- CSV export of processed route metrics
- Local streaming-compatible MapReduce pipeline (mapper -> sort/shuffle -> reducer)
- Optional Hadoop HDFS + Hadoop Streaming execution

## Requirements
- Python 3.10+
- For local demo: Python packages in `requirements.txt`
- For distributed execution: a working Hadoop installation, HDFS and Hadoop Streaming JAR

## Run locally (recommended first)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_sample_data.py
python scripts/run_local_mapreduce.py
python app.py
```
Open http://127.0.0.1:5000

## Run the Hadoop Streaming job
Set `HADOOP_STREAMING_JAR` to the path of your Hadoop Streaming JAR. Example:
```bash
hdfs dfs -mkdir -p /transit/input
hdfs dfs -put -f data/trips_sample.csv /transit/input/
hadoop jar "$HADOOP_STREAMING_JAR" \
  -files scripts/mapper.py,scripts/reducer.py \
  -input /transit/input/trips_sample.csv \
  -output /transit/output/transit_analytics \
  -mapper "python mapper.py" \
  -reducer "python reducer.py"
hdfs dfs -cat /transit/output/transit_analytics/part-00000 > output/analytics.jsonl
```
On Windows, use the equivalent Hadoop command and ensure the Python executable is available on every worker node. Delete the previous HDFS output directory before rerunning:
`hdfs dfs -rm -r /transit/output/transit_analytics`

The Hadoop Streaming output is JSON Lines. For this dashboard, the simplest reproducible workflow is the local pipeline, which runs the same mapper and reducer scripts and writes `output/analytics.json`. You can adapt the Hadoop output into the same JSON structure using `scripts/convert_hadoop_output.py`.

## Dataset schema
`trip_id,service_date,route_id,route_name,stop_id,stop_name,latitude,longitude,boarding_time,passengers,delay_minutes`
Each row represents a trip's stop-level boarding observation. Passenger totals are boardings, not unique individuals.

## Replace sample data
1. Obtain data with a clear licence/permission.
2. Convert it to the schema above.
3. Keep `trip_id` unique per trip; use consistent route/stop IDs.
4. Use actual timestamps and coordinates from the source.
5. Do not infer passenger counts or delay from GTFS schedules alone.
6. Run `python scripts/run_local_mapreduce.py` again.

## Project structure
- `app.py`: Flask server and API
- `app/templates/index.html`: dashboard UI
- `app/static/style.css`, `dashboard.js`: UI and charts/map
- `scripts/mapper.py`, `scripts/reducer.py`: Hadoop Streaming mapper/reducer
- `scripts/run_local_mapreduce.py`: local streaming runner
- `scripts/generate_sample_data.py`: reproducible sample generator
- `data/`: sample CSV
- `output/`: aggregated results

## Academic integrity
Clearly label generated data as simulated in demonstrations, PPT, report and paper. Results from this sample validate the pipeline only; they do not establish actual BMTC service performance.
