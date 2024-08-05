import requests

import numpy as np
import pandas as pd
from tqdm.auto import tqdm


def rest_api_get_request(wd_qid: str, term: str = ""):
    api_endpoint = "https://www.wikidata.org/w/rest.php/wikibase/v0"
    request_string = api_endpoint + "/entities/items/" + f"{wd_qid}"
    if term != "":
        request_string += f"/{term}"

    request = requests.get(request_string)

    return request.json()


birth_pid = "P569"
death_pid = "P570"

df_birth_mismatches = pd.read_csv("output_moma_birth.csv")
df_death_mismatches = pd.read_csv("output_moma_death.csv")

birth_qids = list(df_birth_mismatches["item_id"])
death_qids = list(df_death_mismatches["item_id"])

birth_wd_values = list(df_birth_mismatches["wikidata_value"])
death_wd_values = list(df_death_mismatches["wikidata_value"])

birth_statement_guids = []
for i in tqdm(range(len(birth_qids)), desc="Birth GUIDs found", unit="qids"):
    rest_api_response = rest_api_get_request(wd_qid=birth_qids[i], term="statements")[
        birth_pid
    ]

    for s in rest_api_response:
        s_wd_value = s["value"]["content"]["time"].replace("+", "")
        if s_wd_value == birth_wd_values[i]:
            birth_statement_guids.append(s["id"].upper())
            break

    if len(birth_statement_guids) != i + 1:
        # No matching GUID was found.
        birth_statement_guids.append(np.nan)

death_statement_guids = []
for i in tqdm(range(len(death_qids)), desc="Death GUIDs found", unit="qids"):
    rest_api_response = rest_api_get_request(wd_qid=death_qids[i], term="statements")[
        death_pid
    ]

    for s in rest_api_response:
        s_wd_value = s["value"]["content"]["time"].replace("+", "")
        if s_wd_value == death_wd_values[i]:
            death_statement_guids.append(s["id"].upper())
            break

    if len(death_statement_guids) != i + 1:
        # No matching GUID was found.
        death_statement_guids.append(np.nan)

df_birth_mismatches["statement_guid"] = birth_statement_guids
df_death_mismatches["statement_guid"] = death_statement_guids

df_birth_mismatches.loc[
    df_birth_mismatches["statement_guid"].isnull(), "wikidata_value"
] = np.nan
df_death_mismatches.loc[
    df_death_mismatches["statement_guid"].isnull(), "wikidata_value"
] = np.nan

df_birth_mismatches.to_csv(
    "output_moma_birth_upload.csv",
    sep=",",
    encoding="utf-8",
    index=False,
    header=True,
)

df_death_mismatches.to_csv(
    "output_moma_death_upload.csv",
    sep=",",
    encoding="utf-8",
    index=False,
    header=True,
)
