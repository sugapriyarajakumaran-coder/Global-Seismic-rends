import calendar
import pandas as pd
import requests
from datetime import datetime

base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

all_records = []

start_year = datetime.now().year -5
end_year = datetime.now().year
min_magnitude = 3
current_month = datetime.now().month

for year in range(start_year, end_year + 1):
    for month in range(1,13):
        if year == end_year and month >current_month:
            break
        start_day = datetime(year,month,1) 
        last_day = calendar.monthrange(year,month)[1] 
        end_day = datetime(year,month,last_day)

        start_time = start_day.strftime("%Y-%m-%d")
        
        end_time = end_day.strftime("%Y-%m-%d")

        params = {
            "format":"geojson",
            "starttime" : start_time,
            "endtime" : end_time,
            "minmagnitude" : min_magnitude,
            "orderby":"time-asc"
        }

        response=requests.get(base_url,params = params)

        if response.status_code != 200:
            print(f"Failed for {year}-{month} : response.status_code")
            continue
        data = response.json()
        features = data.get("features", [])

        for event in features:
            pro = event["properties"]
            geo = event["geometry"]
            coord = geo.get("coordinates")
            record = {
                "id" : event["id"],
                "time" : datetime.fromtimestamp(pro.get("time",0)/1000),
                "updated": datetime.fromtimestamp(pro.get("updated", 0) / 1000),
                "latitude" : coord[1],
                "longitude" : coord[0],
                "depth_km" : coord[2],
                "mag" : pro.get("mag"),
                "magType": pro.get("magType"),
                "place": pro.get("place"),
                "status": pro.get("status"),
                "tsunami": pro.get("tsunami"),
                "sig": pro.get("sig"),
                "net": pro.get("net"),
                "nst": pro.get("nst"),
                "dmin": pro.get("dmin"),
                "rms": pro.get("rms"),
                "gap": pro.get("gap"),
                "magError": pro.get("magError"),
                "depthError": pro.get("depthError"),
                "magNst": pro.get("magNst"),
                "locationSource": pro.get("locationSource"),
                "magSource": pro.get("magSource"),
                "types": pro.get("types"),
                "ids": pro.get("ids"),
                "sources": pro.get("sources"),
                "type": pro.get("type"),
                "alert": pro.get("alert")
            }
            all_records.append(record)

df = pd.DataFrame(all_records)  


df["Country"] = (df["place"].str.extract(r",\s*([^,]+)$", expand = False).fillna(df["place"]))

if "alert" in df.columns:
    df["alert"] = df["alert"].astype("string").str.lower()

string_columns = ["magType", "status", "type", "net", "sources", "types"] 
for column in string_columns:
    if column in df.columns:
        df[column] = df[column].astype("string").str.lower().str.strip()
num_columns = ["mag", "depth_km", "nst", "dmin", "rms", "gap", "magError", 
               "depthError", "magNst", "sig"]
for column in num_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column] , errors="coerce")

count_columns = ["nst", "magNst", "sig"]
df[count_columns] = df[count_columns].fillna(0)

for column in ["mag", "depth_km", "dmin", "rms", "gap", "magError", "depthError"]:
    if column in df.columns:
        df[column] = df[column].fillna(df[column].median())  

#Year, month, day, day_of_week from time 
df["years"] = df["time"].dt.year
df["month"]  = df["time"].dt.month 
df["day"] = df["time"].dt.day
df["day_of_week"] = df["time"].dt.day_name()

print(df.columns)
df["depth_flag"] = df["depth_km"].apply(lambda x : "shallow" if x<70 else "deep")
df["destructive_flag"] = df["mag"].apply(lambda x : "destructive" if x>=6.0 else "strong")

print("shape : ", df.shape)

print(df.dtypes)
df.to_csv("clean_earthquakes.csv", index=False)
