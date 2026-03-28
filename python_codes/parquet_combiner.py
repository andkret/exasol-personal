import duckdb

duckdb.sql("""
    COPY (SELECT * FROM read_parquet('yellow_cab/*.parquet'))
    TO 'yellow_cab_combined.parquet' (FORMAT PARQUET)
""")

print("Combined all parquet files from 'yellow_cab/' into 'yellow_cab_combined.parquet'")
