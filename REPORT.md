# Bengaluru Transit Analytics – Project Report

## Abstract
This project demonstrates a public transportation analytics workflow using Python and the Hadoop MapReduce programming model. Stop-level boarding observations are transformed into route-, hour-, stop- and delay-category summaries. The results are displayed in a Flask dashboard with charts, a map and CSV export. The supplied dataset is synthetic and is intended to validate the end-to-end pipeline; it is not official BMTC ridership or punctuality data.

## 1. Introduction
Urban public transportation produces structured information about routes, stops, schedules, vehicle operations and passenger activity. Processing such data can help planners understand demand distribution and service patterns. This project applies distributed data-processing concepts to a Bengaluru-oriented demonstration.

## 2. Problem statement
Raw transportation records are difficult to inspect manually at scale. A repeatable pipeline is needed to group observations and calculate route-level, stop-level and time-based indicators, then present them in an accessible dashboard.

## 3. Objectives
- Prepare and validate transportation records.
- Demonstrate MapReduce mapping, shuffle/sort and reduction.
- Aggregate passenger boardings by route, hour and stop.
- Summarise delay observations into defined bands.
- Visualise the aggregates and support CSV export.
- Keep data provenance and simulation limitations explicit.

## 4. Scope and assumptions
Each CSV row is one stop-level boarding observation for a trip. `passengers` means boardings recorded in that observation, not unique passengers. The sample contains generated records, illustrative Bengaluru stop coordinates and simulated delays. It does not represent current BMTC operations. GTFS schedule data can provide route/stop/trip structure but does not itself provide passenger counts or actual delays.

## 5. System architecture
Data preparation -> HDFS -> Hadoop Streaming mapper -> shuffle and sort -> reducer -> aggregated JSON -> Flask API -> browser dashboard. A local streaming-compatible runner is supplied for development on machines without Hadoop.

## 6. Dataset schema
`trip_id, service_date, route_id, route_name, stop_id, stop_name, latitude, longitude, boarding_time, passengers, delay_minutes`

## 7. MapReduce methodology
The mapper emits four key families per observation: `ROUTE|route_id`, `HOUR|hour`, `STOP|stop_id`, and `DELAY|delay_band`. The shuffle/sort stage groups identical keys. The reducer calculates boarding totals, observation counts, average delay for routes and stop metadata. The local runner invokes the same mapper and reducer processes and sorts mapper output to reproduce Hadoop Streaming semantics.

## 8. Dashboard modules
1. KPI cards: total boardings, route groups, stop locations and weighted average delay.
2. Route analysis: passenger boardings by route.
3. Hourly analysis: boardings by hour.
4. Stop map: illustrative stop coordinates and aggregated boardings.
5. Delay distribution: observations grouped into 0–5, 6–15 and 16+ minute bands.
6. Export: route-level CSV download.

## 9. Implementation
Python is used for data generation and streaming scripts. Flask serves the dashboard and JSON API. Chart.js renders charts; Leaflet and OpenStreetMap tiles render the stop map. Hadoop Streaming can run the mapper and reducer across HDFS input.

## 10. Testing
- Confirm CSV header and row schema.
- Confirm mapper emits four keys for each valid input row.
- Confirm reducer groups sorted keys and returns expected aggregates.
- Compare total route boardings with the sum of input `passengers`.
- Confirm Flask `/` and `/api/analytics` return successfully.
- Confirm CSV export opens and contains route metrics.
- Confirm dashboard labels simulated data.

## 11. Results
The dashboard reports aggregates from the supplied synthetic dataset. Numerical outputs are reproducible because the sample generator uses a fixed random seed. These results demonstrate software functionality only and should not be interpreted as measured BMTC performance.

## 12. Limitations
The demonstration dataset is synthetic; route/stop coordinate associations are illustrative; the map is not a live vehicle tracker; no unique-passenger deduplication is performed; delays are generated rather than measured; and Hadoop cluster execution depends on local cluster configuration.

## 13. Future enhancements
Integrate licensed current BMTC/GTFS and verified operational data; add real-time vehicle positions where officially available; process larger datasets in a multi-node Hadoop cluster; add date/route filters; compare planned versus observed arrivals where both exist; add metro integration and accessibility indicators.

## 14. Conclusion
The project demonstrates how MapReduce can transform transportation observations into useful aggregates and how a web dashboard can make the results understandable. A clear separation between real source data and synthetic demonstration values supports responsible interpretation.

## References and data sources
1. OpenCity, “Bengaluru Bus Stops and Routes,” https://data.opencity.in/dataset/bengaluru-bus-stops-and-routes
2. TUMI Datahub, “GTFS: Bengaluru,” https://hub.tumidata.org/dataset/gtfs-bengaluru
3. OpenCity, BMTC organization datasets, https://data.opencity.in/dataset/?organization=bengaluru-metropolitan-transport-corporation
4. Apache Hadoop, “Hadoop Streaming,” https://hadoop.apache.org/docs/stable/hadoop-streaming/HadoopStreaming.html
5. Apache Hadoop, “MapReduce Tutorial,” https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html
6. OpenStreetMap contributors, https://www.openstreetmap.org/copyright

## Reproducibility statement
Run `python scripts/generate_sample_data.py`, `python scripts/run_local_mapreduce.py`, then `python app.py`. Record the Python/Hadoop versions and date of any real dataset download in the final submission.
