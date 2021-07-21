import os
import pandas as pd
import json
import glob
import datetime


input_file = "Location History.json"

contents = []
json_dir_name = os.getcwd()

json_pattern = os.path.join(json_dir_name, "*.json")
file_list = glob.glob(json_pattern)
print(file_list)

# Flatten the nested data

with open(input_file, "r") as f:
    data = json.loads(f.read())

df = pd.json_normalize(data, record_path=["locations"])


df["dateTime"] = pd.to_datetime(df["timestampMs"], unit="ms")
# convert lat and long formats.
df["latitude"] = df["latitudeE7"] / float(1e7)
df["longitude"] = df["longitudeE7"] / float(1e7)

# print(df.tail())
# print(df.info())

# Previous 14 days days data only.
df1 = df[df.dateTime > datetime.datetime.now() - pd.to_timedelta("14day")]

df1 = df1[
    [
        "dateTime",
        "longitude",
        "latitude",
        "source",
        "accuracy",
        "velocity",
        "platformType",
    ]
]

# print(df1.head())

df1.to_csv("output.csv", index=False)


location_data = df1[df1.accuracy < 1000]

print(location_data)

print(
    "Earliest observed date: {}".format(
        min(location_data["dateTime"]).strftime("%m-%d-%Y")
    )
)
print(
    "Latest observed date: {}".format(
        max(location_data["dateTime"]).strftime("%m-%d-%Y")
    )
)

earliest_obs = min(location_data["dateTime"]).strftime("%m-%d-%Y")
latest_obs = max(location_data["dateTime"]).strftime("%m-%d-%Y")
