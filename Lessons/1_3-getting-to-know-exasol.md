# Connecting to Exasol

When you start the cluster with `exasol start`, the output will display all the connection details you need. If the cluster is already running, you can retrieve the same information at any time with:

```bash
exasol info
```

The connection credentials (passwords) are stored in the `secrets.json` file inside your deployment directory.

> **Important:** The EC2 instances do not have static IPs configured. This means the server address will change every time you stop and start the cluster. Always check the latest connection details via `exasol start` or `exasol info` after a restart.

## Graphical SQL Client (DbVisualizer)

1. Download and install [DbVisualizer](https://www.dbvis.com/)
2. Create a new database connection and choose **Exasol** as the driver
3. Enter the connection details from the `exasol start` output:
   - **Server:** the EC2 hostname (e.g., `ec2-x-x-x-x.eu-central-1.compute.amazonaws.com`)
   - **Port:** `8563`
   - **UserId:** `sys`
   - **Certificate Fingerprint:** as shown in the output
   - **Password:** stored in `deployment/secrets.json`

**Reference:** [DbVisualizer Setup for Exasol](https://docs.exasol.com/db/latest/connect_exasol/sql_clients/db_visualizer.htm)

## Administration UI

Exasol comes with a web-based administration interface hosted on the cluster:

1. Open the URL shown in the `exasol start` output (e.g., `https://ec2-x-x-x-x.eu-central-1.compute.amazonaws.com:8443`)
2. Accept the certificate if necessary
3. Login with username `admin` and the password from `deployment/secrets.json`

## CLI Connection

Connect directly from the terminal:

```bash
exasol connect
```

## SSH Connection

For direct access to the cluster node:

```bash
exasol diag shell
```

Or alternatively using SSH with the key from your deployment directory:

```bash
ssh -i deployment/node_access.pem ubuntu@<ec2-hostname> -p 22
```

## Creating a Schema and Table

Once connected via DbVisualizer, create a new schema and table for the Yellow Cab dataset:

1. Open a new SQL Commander tab in DbVisualizer
2. Create the schema:

   ```sql
   CREATE SCHEMA yellow_cab;
   ```

3. Create the table:

   ```sql
   CREATE TABLE yellow_cab.yellow_taxi_trips (
       VendorID            INT,
       tpep_pickup_datetime  TIMESTAMP,
       tpep_dropoff_datetime TIMESTAMP,
       passenger_count     INT,
       trip_distance       DOUBLE,
       RatecodeID          INT,
       store_and_fwd_flag  VARCHAR(1),
       PULocationID        INT,
       DOLocationID        INT,
       payment_type        INT,
       fare_amount         DOUBLE,
       extra               DOUBLE,
       mta_tax             DOUBLE,
       tip_amount          DOUBLE,
       tolls_amount        DOUBLE,
       improvement_surcharge DOUBLE,
       total_amount        DOUBLE,
       congestion_surcharge DOUBLE,
       airport_fee         DOUBLE,
       cbd_congestion_fee  DOUBLE
   );
   ```

## Importing Data from S3

Import the Yellow Cab parquet dataset from S3 into the table:

```sql
IMPORT INTO yellow_taxi_trips
  FROM PARQUET AT 'https://exasol-personal-data.s3.eu-central-1.amazonaws.com/'
  FILE 'yellow_cab_combined.parquet';
```

This imports approximately 48.7 million rows (~1 GB) from a single parquet file. On a single-node r6i.xlarge instance, the import takes about 35 seconds.

![Import example output](../Script_Images/1_3/import_example_output.png)
