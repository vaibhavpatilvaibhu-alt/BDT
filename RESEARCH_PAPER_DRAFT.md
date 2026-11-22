# A MapReduce-Based Analytics Dashboard for Public Transportation Data: A Bengaluru-Oriented Demonstration

**Author(s):** [Student name(s)]  
**Affiliation:** [Department, College, City]  
**Email:** [Institutional email]

## Abstract
Public transportation systems generate records that can be aggregated to reveal route demand, temporal patterns and operational indicators. This paper presents a MapReduce-based analytics pipeline and web dashboard for a Bengaluru-oriented public transportation demonstration. Python Hadoop Streaming scripts aggregate stop-level boarding observations by route, hour and stop, while also grouping delay observations into bands. A Flask application exposes the results to a browser dashboard with charts, a map and CSV export. The implementation is reproducible using a synthetic dataset, and the data provenance is explicitly stated: the demonstration passenger and delay values are simulated and are not official BMTC measurements. The contribution is therefore an end-to-end technical prototype and evaluation method, not a claim about actual city-wide transit performance.

**Keywords:** Big Data, Hadoop, MapReduce, Public Transportation, Bengaluru, Data Visualization, Flask.

## I. INTRODUCTION
Public transport planning benefits from understanding how demand varies by route, stop and time of day. As datasets grow, distributed processing frameworks provide a systematic way to aggregate records. This work demonstrates a pipeline based on the MapReduce model and presents its output through a browser-based dashboard.

## II. RELATED DATA AND BACKGROUND
Publicly catalogued Bengaluru resources include bus stop and route information and a historical GTFS feed. GTFS describes transit entities such as routes, stops and scheduled trips; it should not be treated as a source of actual passenger boardings or measured delays unless those fields are separately supplied. Apache Hadoop Streaming allows executable scripts to act as mapper and reducer programs.

## III. SYSTEM DESIGN
The system consists of (1) CSV ingestion and validation, (2) HDFS storage for distributed execution, (3) a mapper that emits route/hour/stop/delay keys, (4) shuffle and sort, (5) a reducer that computes aggregates, and (6) a Flask dashboard. A local runner invokes the same scripts for reproducible development without a Hadoop cluster.

## IV. METHODOLOGY
For each valid observation, the mapper emits four key-value records. Route keys are grouped to compute total boardings, observation count and average delay. Hour keys calculate hourly boardings. Stop keys calculate stop-level boardings and retain illustrative coordinates. Delay keys count records in 0–5, 6–15 and 16+ minute bands. The reducer receives sorted keys and produces JSON Lines output.

## V. IMPLEMENTATION
The prototype is implemented in Python. Flask serves the user interface and analytics endpoint. Chart.js renders route, hourly and delay charts. Leaflet displays stop markers using OpenStreetMap tiles. Route aggregates can be exported as CSV. The repository includes a fixed-seed synthetic data generator and a local MapReduce runner.

## VI. EVALUATION PLAN
The prototype should be evaluated using: (a) correctness, by comparing reducer totals with independently calculated CSV totals; (b) completeness, by checking all valid rows are represented; (c) scalability, by measuring runtime for increasing input sizes; (d) reliability, by testing malformed and missing fields; and (e) usability, by asking representative users to complete route and peak-hour analysis tasks. Report actual measurements only after running the experiments. Do not invent performance numbers.

## VII. RESULTS AND DISCUSSION
The current prototype demonstrates the end-to-end processing and visualisation workflow on generated data. It is suitable for testing MapReduce logic and dashboard integration. Because passenger and delay values are simulated, no inference about actual BMTC ridership, punctuality or congestion is warranted.

## VIII. LIMITATIONS AND FUTURE WORK
Future work includes ingesting licensed current operational datasets, validating stop and route geometries, adding date filters, comparing actual scheduled and observed arrivals, running on a multi-node Hadoop cluster and evaluating scalability with documented hardware and input sizes.

## IX. CONCLUSION
The project shows how Hadoop Streaming can aggregate transportation observations and how web visualisation can expose the results. Real-world conclusions require verified operational data and a transparent data-quality process.

## REFERENCES
[1] Apache Software Foundation, “Hadoop Streaming,” Apache Hadoop Documentation. https://hadoop.apache.org/docs/stable/hadoop-streaming/HadoopStreaming.html  
[2] Apache Software Foundation, “MapReduce Tutorial,” Apache Hadoop Documentation. https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html  
[3] TUMI Datahub, “GTFS: Bengaluru.” https://hub.tumidata.org/dataset/gtfs-bengaluru  
[4] OpenCity, “Bengaluru Bus Stops and Routes.” https://data.opencity.in/dataset/bengaluru-bus-stops-and-routes  
[5] OpenStreetMap contributors, “Copyright and License.” https://www.openstreetmap.org/copyright

**Submission note:** Replace placeholders, add genuine experiment measurements, verify the current dataset licence, and follow the college's research-paper template before submission. This is a draft, not a peer-reviewed or published paper.
