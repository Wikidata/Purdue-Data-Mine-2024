import pandas as pd

df_mismatches = pd.read_csv("find_a_grave_mismatches.csv")

df_mismatches["statement_guid"] = (
    df_mismatches["statement_guid"]
    .str.replace("http://www.wikidata.org/entity/statement/", "")
    .str.upper()
)

df_mismatches.to_csv(
    "find_a_grave_mismatches_upload.csv",
    sep=",",
    encoding="utf-8",
    index=False,
    header=True,
)
