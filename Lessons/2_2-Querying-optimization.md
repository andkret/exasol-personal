# Query Optimization

## Setting Up the TPC-H Dataset

To explore query optimization we will use the industry-standard TPC-H benchmark dataset at 100 GB scale. Rather than downloading a pre-built dataset (which would be slow and inefficient), we generate it ourselves from the TPC-H source code.

### Step 1: Download the TPC-H Source Code

1. Go to the [TPC-H Specification page](https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp)
2. Fill in the required information to request the download
3. You will receive an email with a download link

> **Note:** The download link is only valid for a short period (less than 24 hours). Make sure to download the source code as soon as you receive the email.

### Step 2: Compile and Generate the Dataset

Log into the AWS EC2 instance via the AWS Console (go to EC2 > Instances > Connect), then install the required build tools and generate the raw `.tbl` data files:

```bash
sudo apt update
sudo apt install build-essential -y
cd tpch-kit/dbgen
./dbgen -s 10
ls -lh *.tbl
df -h
```

### Step 3: Convert .tbl Files to Parquet

Install Python and the required libraries, then create the conversion script:

```bash
sudo apt install python3 python3-pip python3-venv -y
python3 -m venv tpch-env
source tpch-env/bin/activate
pip install duckdb pandas pyarrow
```

Create a file called `convert_to_parquet.py` with the following content. This script reads each `.tbl` file, converts it to Parquet, and for the `lineitem` table additionally adds two columns: `quarter_rand` (a random quarter 1–4) and `hotspot_key` (a skewed key used to simulate bad data distribution — 95% of rows get value 1):

```python
import duckdb
import os

con = duckdb.connect()

tables = [
    "region",
    "nation",
    "part",
    "supplier",
    "partsupp",
    "customer",
    "orders",
    "lineitem"
]

for table in tables:
    print(f"Processing {table}...")

    con.execute(f"DROP TABLE IF EXISTS {table};")

    con.execute(f"""
        CREATE TABLE {table} AS
        SELECT *
        FROM read_csv_auto(
            '{table}.tbl',
            delim='|',
            header=False,
            ignore_errors=True,
            null_padding=True
        );
    """)

    row_count = con.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
    print(f"Rows loaded: {row_count}")

    os.makedirs(f"parquet/{table}", exist_ok=True)

    if table == "lineitem":
        con.execute(f"""
            COPY (
                SELECT
                    *,
                    1 + (abs(hash(column00, column03)) % 4) AS quarter_rand,
                    CASE
                        WHEN abs(hash(column00, column03, column01)) % 100 < 95 THEN 1
                        ELSE 2
                    END AS hotspot_key
                FROM {table}
            )
            TO 'parquet/{table}'
            (
                FORMAT PARQUET,
                PER_THREAD_OUTPUT TRUE,
                FILE_SIZE_BYTES '512MB',
                ROW_GROUP_SIZE 1000000
            );
        """)
    else:
        con.execute(f"""
            COPY {table}
            TO 'parquet/{table}'
            (
                FORMAT PARQUET,
                PER_THREAD_OUTPUT TRUE,
                FILE_SIZE_BYTES '512MB',
                ROW_GROUP_SIZE 1000000
            );
        """)

    con.execute(f"DROP TABLE {table};")

print("Done.")
```

Run the script:

```bash
python3 convert_to_parquet.py
```

### Step 4: Upload Parquet Files to S3

Install the AWS CLI, configure it with your IAM user credentials, and upload the lineitem parquet files:

```bash
sudo apt install awscli -y
aws configure
```

```bash
aws s3 cp parquet/lineitem \
  s3://your-bucket/lineitems/ \
  --recursive
```

Clean up the generated files from the instance to free up disk space:

```bash
rm -rf parquet
rm -f *.tbl
```

---

## Cluster Scaling — Import Performance Comparison

Using the 120 million row lineitem dataset, we can clearly see the performance benefit of adding more nodes to the cluster.

**Single-node cluster:**

![Import on single node cluster](../Script_Images/2_2/Import-single-node-cluster.png)

**4-node cluster:**

![Import on 4-node cluster](../Script_Images/2_2/Import-4-node-cluser.png)

The results show a significant reduction in import time when scaling from 1 to 4 nodes. Exasol distributes the workload across all nodes in parallel, so adding nodes directly translates into faster data ingestion.

---

## Distribution Key Demo

To demonstrate how distribution keys affect query performance, we set up a 4-node cluster and compare a poorly distributed table against a well distributed one.

### Step 1: Create a 4-Node Cluster

Stop the current single-node cluster and create a new 4-node deployment:

```bash
exasol stop
cd ..
mkdir 4-node-cluster
cd 4-node-cluster
exasol install aws --cluster-size 4
```

Log back into DbVisualizer using the connection details shown after the install completes.

### Step 2: Create the Badly Distributed Table

This table uses `HOTSPOT_KEY` as the distribution key. Since 95% of rows have `HOTSPOT_KEY = 1`, almost all data ends up on a single node — creating a severe imbalance:

```sql
CREATE OR REPLACE TABLE LINEITEM_BAD_DIST (
    L_ORDERKEY      DECIMAL(18,0),
    L_PARTKEY       DECIMAL(18,0),
    L_SUPPKEY       DECIMAL(18,0),
    L_LINENUMBER    DECIMAL(18,0),
    L_QUANTITY      DOUBLE PRECISION,
    L_EXTENDEDPRICE DOUBLE PRECISION,
    L_DISCOUNT      DOUBLE PRECISION,
    L_TAX           DOUBLE PRECISION,
    L_RETURNFLAG    VARCHAR(1),
    L_LINESTATUS    VARCHAR(1),
    L_SHIPDATE      DATE,
    L_COMMITDATE    DATE,
    L_RECEIPTDATE   DATE,
    L_SHIPINSTRUCT  VARCHAR(25),
    L_SHIPMODE      VARCHAR(10),
    L_COMMENT       VARCHAR(44),
    QUARTER_RAND    DECIMAL(1,0),
    HOTSPOT_KEY     DECIMAL(1,0)
);

ALTER TABLE LINEITEM_BAD_DIST DISTRIBUTE BY HOTSPOT_KEY;
```

Import the data:

```sql
IMPORT INTO LINEITEM_BAD_DIST
FROM PARQUET AT 'https://exasol-personal-data.s3.eu-central-1.amazonaws.com/'
FILE 'lineitems/data_0.parquet'
FILE 'lineitems/data_1.parquet'
FILE 'lineitems/data_2.parquet'
FILE 'lineitems/data_3.parquet'
FILE 'lineitems/data_4.parquet'
FILE 'lineitems/data_5.parquet'
FILE 'lineitems/data_6.parquet'
FILE 'lineitems/data_7.parquet'
FILE 'lineitems/data_8.parquet'
FILE 'lineitems/data_9.parquet';
```

Check the data distribution across nodes — you should see a severe imbalance:

```sql
SELECT
    IPROC() AS NODE_ID,
    COUNT(*) AS ROWS_ON_NODE
FROM LINEITEM_BAD_DIST
GROUP BY IPROC()
ORDER BY IPROC();
```

Run a simple count and a heavy aggregation query to measure performance:

```sql
SELECT COUNT(*)
FROM LINEITEM_BAD_DIST
WHERE HOTSPOT_KEY = 1;
```

```sql
SELECT
    L_PARTKEY,
    L_SUPPKEY,
    L_SHIPMODE,
    L_RETURNFLAG,
    SUM(L_EXTENDEDPRICE) AS REVENUE,
    SUM(L_QUANTITY) AS QTY,
    AVG(L_DISCOUNT) AS AVG_DISCOUNT,
    AVG(L_TAX) AS AVG_TAX
FROM LINEITEM_GOOD_DIST
WHERE QUARTER_RAND = 1
GROUP BY
    L_PARTKEY,
    L_SUPPKEY,
    L_SHIPMODE,
    L_RETURNFLAG
LIMIT 100;
```

### Step 3: Create the Well Distributed Table

This table uses `L_ORDERKEY` as the distribution key. Since order keys are unique and evenly spread, rows are distributed uniformly across all nodes:

```sql
CREATE OR REPLACE TABLE LINEITEM_GOOD_DIST (
    L_ORDERKEY      DECIMAL(18,0),
    L_PARTKEY       DECIMAL(18,0),
    L_SUPPKEY       DECIMAL(18,0),
    L_LINENUMBER    DECIMAL(18,0),
    L_QUANTITY      DOUBLE PRECISION,
    L_EXTENDEDPRICE DOUBLE PRECISION,
    L_DISCOUNT      DOUBLE PRECISION,
    L_TAX           DOUBLE PRECISION,
    L_RETURNFLAG    VARCHAR(1),
    L_LINESTATUS    VARCHAR(1),
    L_SHIPDATE      DATE,
    L_COMMITDATE    DATE,
    L_RECEIPTDATE   DATE,
    L_SHIPINSTRUCT  VARCHAR(25),
    L_SHIPMODE      VARCHAR(10),
    L_COMMENT       VARCHAR(44),
    QUARTER_RAND    DECIMAL(1,0),
    HOTSPOT_KEY     DECIMAL(1,0)
);

ALTER TABLE LINEITEM_GOOD_DIST DISTRIBUTE BY L_ORDERKEY;
```

Import the data:

```sql
IMPORT INTO LINEITEM_GOOD_DIST
FROM PARQUET AT 'https://exasol-personal-data.s3.eu-central-1.amazonaws.com/'
FILE 'lineitems/data_0.parquet'
FILE 'lineitems/data_1.parquet'
FILE 'lineitems/data_2.parquet'
FILE 'lineitems/data_3.parquet'
FILE 'lineitems/data_4.parquet'
FILE 'lineitems/data_5.parquet'
FILE 'lineitems/data_6.parquet'
FILE 'lineitems/data_7.parquet'
FILE 'lineitems/data_8.parquet'
FILE 'lineitems/data_9.parquet';
```

Check the distribution — rows should be spread evenly this time:

```sql
SELECT
    IPROC() AS NODE_ID,
    COUNT(*) AS ROWS_ON_NODE
FROM LINEITEM_GOOD_DIST
GROUP BY IPROC()
ORDER BY IPROC();
```

Run the same heavy query and compare the execution time against the badly distributed table:

```sql
SELECT
    L_PARTKEY,
    L_SUPPKEY,
    L_SHIPMODE,
    L_RETURNFLAG,
    SUM(L_EXTENDEDPRICE) AS REVENUE,
    SUM(L_QUANTITY) AS QTY,
    AVG(L_DISCOUNT) AS AVG_DISCOUNT,
    AVG(L_TAX) AS AVG_TAX
FROM LINEITEM_GOOD_DIST
WHERE QUARTER_RAND = 1
GROUP BY
    L_PARTKEY,
    L_SUPPKEY,
    L_SHIPMODE,
    L_RETURNFLAG
LIMIT 100;
```


## Query Writing Best Practices

Having the right keys set up is only half the story — how you write your queries also directly affects performance.

**Avoid:**

- **ORDER BY in views and subqueries** — only sort in the outermost final SELECT. Sorting inside subqueries forces materialisation and kills parallelism
- **UNION instead of UNION ALL** — UNION removes duplicates which requires an extra pass over the data. Use UNION ALL unless you explicitly need deduplication
- **Joining columns of different data types** — e.g. joining an INT to a VARCHAR triggers implicit type conversion and prevents efficient local joins
- **Oversized data types** — avoid VARCHAR(2000000) or DECIMAL(32,x) when much smaller types are sufficient. Oversized types hurt compression and memory usage
- **Distributing on WHERE clause columns** — this disables MPP for filtered queries and forces global joins

**Do:**

- **Distribute large tables on join columns** — both tables distributed on the same join column means the join happens locally on each node with no network traffic
- **Use exact, compact data types** — smaller types compress better and process faster
- **Use DECIMAL over DOUBLE for financial data** — DOUBLE is approximate; DECIMAL is exact
- **Filter on partition key columns in WHERE clauses** — this allows Exasol to skip entire partitions and scan only the relevant data

**Reference:** [Exasol Performance Best Practices](https://docs.exasol.com/db/latest/performance/best_practices.htm)
