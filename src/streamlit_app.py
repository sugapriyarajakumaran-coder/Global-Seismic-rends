import streamlit as st
import pandas as pd
from mysql_connection import engine

st.title("Global Seismic Trends Dashboard")
st.subheader("Interactive analysis of global earthquake patterns using MySQL & Streamlit")

question = st.selectbox(
    "Choose an analysis question:",
    [
        "--Select a question--",
        "Top 10 strongest earthquakes",
        "Top 10 deepest earthquakes",
        "Shallow earthquakes < 50 km and mag > 7.5",
        "Average magnitude per magnitude type (magType)",
        "Year with most earthquakes",
        "Month with highest number of earthquakes",
        "Day of week with most earthquakes",
        "Count of earthquakes per hour of day",
        "Most active reporting network (net)",

        "Count of reviewed vs automatic earthquakes (status)",
        "Count by earthquake type (type)",
        "Number of earthquakes by data type (types)",
        "Events with high station coverage (nst > threshold)",
        "Number of tsunamis triggered per year",
        "Count earthquakes by alert levels (red, orange, etc.)",

  	    "Find the top 5 countries with the highest average magnitude of earthquakes in the past 10 years",             	
  	    "Find countries that have experienced both shallow and deep earthquakes within the same month",
  	    "Compute the year-over-year growth rate in the total number of earthquakes globally",
   	    "List the 3 most seismically active regions by combining both frequency and average magnitude",

        "For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator",
        "Identify countries having the highest ratio of shallow to deep earthquakes",
        "Find the average magnitude difference between earthquakes with tsunami alerts and those without",
        "Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins)",
         
        "Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km)"

    ]
)
if question == "--Select a question--":
    st.info("Please select an analysis question from the dropdown.")
    st.stop()

if question == "Top 10 strongest earthquakes":
    query = """
    SELECT * FROM earthquakes ORDER BY mag DESC LIMIT 10;
    """
    df = pd.read_sql(query, engine)
    st.dataframe(df)

elif question == "Top 10 deepest earthquakes":
    query = """
    SELECT * FROM earthquakes ORDER BY depth_km DESC LIMIT 10;
    """
    df = pd.read_sql(query, engine)
    st.dataframe(df)
elif question == "Shallow earthquakes < 50 km and mag > 7.5":
    query = """ SELECT * FROM earthquakes WHERE depth_km < 50 AND mag > 7.5; """   
    df = pd.read_sql(query, engine)
    st.dataframe(df)

elif question == "Average magnitude per magnitude type (magType)":    
    query ="""SELECT magType, AVG(mag) AS avg_mag FROM earthquakes 
    GROUP BY magType ORDER BY avg_mag DESC;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)

elif question == "Year with most earthquakes":   
    query ="""SELECT years, COUNT(*) AS quake_count FROM earthquakes GROUP BY years
    ORDER BY quake_count DESC LIMIT 1;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)    

elif question == "Month with highest number of earthquakes":
    query = """SELECT month, COUNT(*) AS quake_count FROM earthquakes GROUP BY month
    ORDER BY quake_count DESC LIMIT 1;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)

elif question == "Day of week with most earthquakes":
    query = """SELECT day_of_week, COUNT(*) AS quake_count FROM earthquakes GROUP BY day_of_week
    ORDER BY quake_count DESC;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)    

elif question == "Count of earthquakes per hour of day":
    query = """SELECT HOUR(time) AS hour, COUNT(*) AS quake_count FROM earthquakes GROUP BY hour
ORDER BY hour;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df) 

elif question == "Most active reporting network (net)":
    query = """SELECT net, COUNT(*) AS reports FROM earthquakes GROUP BY net ORDER BY reports DESC
LIMIT 1;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)  

elif question == "Count of reviewed vs automatic earthquakes (status)":
    query = """select status, count(*) from earthquakes group by status;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)  

elif question == "Count by earthquake type (type)":
    query = """select type, count(*) as status_count from earthquakes group by type;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)   

elif question == "Number of earthquakes by data type (types)":
    query = """select types, count(*) as status_count from earthquakes group by types;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)  

elif question == "Events with high station coverage (nst > threshold)":
    query = """SELECT *FROM earthquakes WHERE nst > 50;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df) 

elif question == "Count earthquakes by alert levels (red, orange, etc.)":
    query = """select alert, count(*) as alert_count from earthquakes group by alert;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)   

elif question == "Find the top 5 countries with the highest average magnitude of earthquakes in the past 10 years":
    query = """SELECT country, AVG(mag) AS avg_mag FROM earthquakes 
    WHERE years >= (SELECT MIN(years) FROM earthquakes) 
    GROUP BY country ORDER BY avg_mag DESC LIMIT 5;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)   

elif question == "Find countries that have experienced both shallow and deep earthquakes within the same month":
    query = """SELECT DISTINCT country, years, month FROM earthquakes
WHERE (country, years, month) IN (SELECT country, years, month FROM earthquakes WHERE depth_km < 70)
AND (country, years, month) IN (SELECT country, years, month FROM earthquakes WHERE depth_km > 300);"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)   

elif question == "Compute the year-over-year growth rate in the total number of earthquakes globally":
    query = """SELECT years, total, total - LAG(total) OVER (ORDER BY years) AS year_difference
FROM ( SELECT years, COUNT(*) AS total FROM earthquakes GROUP BY years) t;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)    

elif question == "List the 3 most seismically active regions by combining both frequency and average magnitude":
    query = """SELECT country, COUNT(*) AS frequency, AVG(mag) AS avg_mag,COUNT(*) * AVG(mag) AS activity_score
FROM earthquakes GROUP BY country ORDER BY activity_score DESC LIMIT 3;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)  
                

elif question == "For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator":
    query = """SELECT country, AVG(depth_km) AS avg_depth FROM earthquakes WHERE latitude BETWEEN -5 AND 5 GROUP BY country;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)

elif question == "Identify countries having the highest ratio of shallow to deep earthquakes":
    query = """SELECT country,SUM(CASE WHEN depth_flag = 'Shallow' THEN 1 ELSE 0 END) /NULLIF(SUM(CASE WHEN depth_flag = 'Deep' THEN 1 ELSE 0 END), 0) AS ratio
FROM earthquakes GROUP BY country ORDER BY ratio DESC;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)

elif question == "Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins)":
    query = """SELECT * FROM earthquakes ORDER BY (rms + gap) DESC LIMIT 10;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)

elif question == "Find the average magnitude difference between earthquakes with tsunami alerts and those without":
    query = """SELECT 
    (SELECT AVG(mag) FROM earthquakes WHERE tsunami = 1) -
    (SELECT AVG(mag) FROM earthquakes WHERE tsunami = 0) AS mag_diff;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)    

elif question == "Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km)":
    query = """SELECT country, COUNT(*) AS deep_quakes FROM earthquakes
WHERE depth_km > 300 GROUP BY country;"""
    df = pd.read_sql(query, engine)
    st.dataframe(df)
