import os, json
import pandas as pd
import numpy as np
from pathlib import Path


def dataFormater(fields):
    data_list = list()
    for i, field in enumerate(fields):
        data_list.append({
            "model": "main.lecture",
            "pk": i + 1,
            "fields": field
        })
    return data_list


cwd = Path('.')
dir_name = "data"
file_name = "lecture.csv"
full_path = cwd / dir_name / file_name

data = pd.read_csv(full_path, encoding="utf-8")
data.reset_index()
data = data.fillna("")
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(data.head())

data = data.to_dict(orient="records")
data = dataFormater(data)
# json_data = json.dumps(data)

write_file_path = cwd / Path("data/initial_data.json")

with open(write_file_path, 'w', encoding='UTF-8') as f:
    json.dump(data, f, ensure_ascii=False)
