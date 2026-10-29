-- Week 1, Task 2: 10 queries using filters, joins, GROUP BY and CTEs
-- Tables: taxi_trips (yellow taxi trips), taxi_zones (LocationID, Borough, Zone, service_zone)
USE nyc_taxi;

-- Q1 (filter): long, expensive trips in January 2024
SELECT tpep_pickup_datetime, trip_distance, fare_amount, total_amount
FROM taxi_trips
WHERE tpep_pickup_datetime >= '2024-01-01' AND tpep_pickup_datetime < '2024-02-01'
  AND trip_distance > 10 AND fare_amount > 50
ORDER BY fare_amount DESC
LIMIT 20;

-- Q2 (join): trips with pickup zone and borough
SELECT t.tpep_pickup_datetime, z.Borough, z.Zone, t.total_amount
FROM taxi_trips t
JOIN taxi_zones z ON t.PULocationID = z.LocationID
LIMIT 20;

-- Q3 (join + group by): trips and average fare per pickup borough
SELECT z.Borough, COUNT(*) AS trips, ROUND(AVG(t.fare_amount), 2) AS avg_fare
FROM taxi_trips t
JOIN taxi_zones z ON t.PULocationID = z.LocationID
GROUP BY z.Borough
ORDER BY trips DESC;

-- Q4 (group by + having): revenue by payment type (1=Card, 2=Cash, 3=No charge, 4=Dispute)
SELECT payment_type, COUNT(*) AS trips, ROUND(SUM(total_amount), 2) AS revenue
FROM taxi_trips
GROUP BY payment_type
HAVING COUNT(*) > 1000
ORDER BY revenue DESC;

-- Q5 (group by): demand by hour of day
SELECT HOUR(tpep_pickup_datetime) AS pickup_hour, COUNT(*) AS trips
FROM taxi_trips
GROUP BY pickup_hour
ORDER BY pickup_hour;

-- Q6 (double join): top 10 pickup -> dropoff routes
SELECT pz.Zone AS pickup_zone, dz.Zone AS dropoff_zone, COUNT(*) AS trips
FROM taxi_trips t
JOIN taxi_zones pz ON t.PULocationID = pz.LocationID
JOIN taxi_zones dz ON t.DOLocationID = dz.LocationID
GROUP BY pz.Zone, dz.Zone
ORDER BY trips DESC
LIMIT 10;

-- Q7 (CTE): days where revenue was above the monthly daily average
WITH daily AS (
    SELECT DATE(tpep_pickup_datetime) AS d, SUM(total_amount) AS revenue
    FROM taxi_trips
    WHERE tpep_pickup_datetime >= '2024-01-01' AND tpep_pickup_datetime < '2024-02-01'
    GROUP BY DATE(tpep_pickup_datetime)
)
SELECT d, ROUND(revenue, 2) AS revenue
FROM daily
WHERE revenue > (SELECT AVG(revenue) FROM daily)
ORDER BY revenue DESC;

-- Q8 (CTE + join): average tip percentage by borough (card payments only)
WITH card_trips AS (
    SELECT PULocationID, tip_amount, fare_amount
    FROM taxi_trips
    WHERE payment_type = 1 AND fare_amount > 0
)
SELECT z.Borough, ROUND(AVG(c.tip_amount / c.fare_amount) * 100, 1) AS avg_tip_pct
FROM card_trips c
JOIN taxi_zones z ON c.PULocationID = z.LocationID
GROUP BY z.Borough
ORDER BY avg_tip_pct DESC;

-- Q9 (filter + group by): average distance and passengers by weekday
SELECT DAYNAME(tpep_pickup_datetime) AS weekday,
       ROUND(AVG(trip_distance), 2) AS avg_distance,
       ROUND(AVG(passenger_count), 2) AS avg_passengers
FROM taxi_trips
WHERE trip_distance > 0
GROUP BY weekday, DAYOFWEEK(tpep_pickup_datetime)
ORDER BY DAYOFWEEK(tpep_pickup_datetime);

-- Q10 (CTE + join): airport-related trips and their average fare
WITH airport_zones AS (
    SELECT LocationID, Zone FROM taxi_zones WHERE Zone LIKE '%Airport%'
)
SELECT a.Zone AS airport, COUNT(*) AS pickups, ROUND(AVG(t.total_amount), 2) AS avg_total
FROM taxi_trips t
JOIN airport_zones a ON t.PULocationID = a.LocationID
GROUP BY a.Zone
ORDER BY pickups DESC;
