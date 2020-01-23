#!/usr/bin/env python3

import pandas as pd
import unidecode
import requests
import glob
import json

df = pd.read_csv("textiles_only.csv")
df = df.drop_duplicates(subset="Statement ID")
df = df.where(df.notnull(), None)

countries = json.load(open("countries.geojson"))["features"]

results = {}

for i, row in df.iterrows():
    statement = glob.glob(f"text_statements/from_pdf/{row['Company ID']}-*-{row['Statement ID']}.txt")
    if statement:
        result = row.to_dict()
        mentioned_countries = []
        with open(statement[0]) as f:
            statement = f.read()
        for country in countries:
            country_name = country["properties"]["name"]
            if country_name.lower() in statement.lower():
                mentioned_countries.append(country_name)
        result["Mentioned Countries"] = mentioned_countries
        results[result["Statement ID"]] = result

with open("mentioned_countries.json", "w") as f:
    json.dump(results, f, indent=4)