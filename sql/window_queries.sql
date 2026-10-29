-- Week 1, Task 3: 3 window queries (rank, running total, top-N per group)
USE nyc_taxi;

-- W1 (rank): rank pickup zones by number of trips
WITH zone_trips AS (
    SELECT z.Zone, z.Borough, COUNT(*) AS trips
    FROM taxi_trips t
    JOIN taxi_zones z ON t.PULocationID = z.LocationID
    GROUP BY z.Zone, z.Borough
)
SELECT Zone, Borough, trips,
       RANK() OVER (ORDER BY trips DESC) AS trip_rank
FROM zone_trips
ORDER BY trip_rank
LIMIT 20;

-- W2 (running total): cumulative revenue by day
WITH daily AS (
    SELECT DATE(tpep_pickup_datetime) AS d, SUM(total_amount) AS revenue
    FROM taxi_trips
    WHERE tpep_pickup_datetime >= '2024-01-01' AND tpep_pickup_datetime < '2024-02-01'
    GROUP BY DATE(tpep_pickup_datetime)
)
SELECT d, ROUND(revenue, 2) AS revenue,
       ROUND(SUM(revenue) OVER (ORDER BY d), 2) AS running_total
FROM daily
ORDER BY d;

-- W3 (top-N per group): top 3 pickup zones in each borough
WITH zone_trips AS (
    SELECT z.Borough, z.Zone, COUNT(*) AS trips
    FROM taxi_trips t
    JOIN taxi_zones z ON t.PULocationID = z.LocationID
    GROUP BY z.Borough, z.Zone
),
ranked AS (
    SELECT Borough, Zone, trips,
           ROW_NUMBER() OVER (PARTITION BY Borough ORDER BY trips DESC) AS rn
    FROM zone_trips
)
SELECT Borough, Zone, trips, rn
FROM ranked
WHERE rn <= 3
ORDER BY Borough, rn;
