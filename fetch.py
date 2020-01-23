#!/usr/bin/env python3

import pandas as pd
import unidecode
import requests
import glob

df = pd.read_csv("textiles_only.csv")
df = df.drop_duplicates(subset="Statement ID")

strip = ".&()/'+,"

def ext_detect(s):
    if "pdf" in s:
        return ".pdf"
    elif "jpeg" in s:
        return ".jpg"
    elif "png" in s:
        return ".png"
    return ".html"

for i, row in df.iterrows():
    safe_company_name = unidecode.unidecode(row["Company"].lower()).strip().replace(" ", "-")
    for c in strip:
        safe_company_name = safe_company_name.replace(c, "")
    safe_company_name = safe_company_name.replace("--", "-")
    output_filename = f'statements/{row["Company ID"]}-{safe_company_name}-{row["Statement ID"]}'
    if not glob.glob(output_filename + ".*"):
        snapshot_url = f'https://www.modernslaveryregistry.org/companies/{row["Company ID"]}-{safe_company_name}/statements/{row["Statement ID"]}/snapshot'
        print(snapshot_url)
        r = requests.get(snapshot_url, allow_redirects=True)
        ext = ext_detect(r.headers["Content-Type"])
        with open(output_filename + ext, "wb") as f:
            f.write(r.content)
    output_filename += "-2020"
    if not glob.glob(output_filename + ".*"):
        try:
            print(row["URL"])
            r = requests.get(row["URL"], allow_redirects=True, verify=False, timeout=5)
            r.raise_for_status()
            ext = ext_detect(r.headers["Content-Type"])
            with open(output_filename + ext, "wb") as f:
                f.write(r.content)
        except:
            continue