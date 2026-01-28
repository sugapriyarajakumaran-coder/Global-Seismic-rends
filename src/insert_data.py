import pandas as pd
from mysql_connection import engine

df = pd.read_csv(
    "clean_earthquakes.csv",
    parse_dates=["time", "updated"]
)

print("CSV loaded:", df.shape)

df.to_sql(
    name="earthquakes", 
    con=engine,
    if_exists="append",
    index=False,
    chunksize=1000
)

print("Data inserted into MySQL successfully")
