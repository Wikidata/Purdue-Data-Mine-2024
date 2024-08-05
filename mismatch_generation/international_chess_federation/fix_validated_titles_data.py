import numpy as np
import pandas as pd

df_mismatches = pd.read_csv("validated_titles_data.csv")

df_mismatches["external_value"].replace(np.nan, "No title", inplace=True)
df_mismatches["external_value"].replace("FM", "FIDE Master", inplace=True)
df_mismatches["external_value"].replace("WFM", "Woman FIDE Master", inplace=True)
df_mismatches["external_value"].replace("WIM", "Woman Intl. Master", inplace=True)
df_mismatches["external_value"].replace("WGM", "Woman Grandmaster", inplace=True)
df_mismatches["external_value"].replace("IM", "Intl. Master", inplace=True)
df_mismatches["external_value"].replace("GM", "Grandmaster", inplace=True)
df_mismatches["external_value"].replace(
    "WH", "Woman Honorary Grandmaster", inplace=True
)

df_mismatches.to_csv(
    "validated_titles_data_upload.csv",
    sep=",",
    encoding="utf-8",
    index=False,
    header=True,
)
