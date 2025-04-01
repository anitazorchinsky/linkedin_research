import os
import pandas as pd


files_list = []
ignore_files = ["all_vacancy.xlsx","skills.xlsx", "skills1.xlsx", "test.xlsx"]
for file in os.listdir():
    if file.endswith(".xlsx") and file not in ignore_files:
        files_list.append(pd.read_excel(file))

concat = pd.concat(files_list)
concat.to_excel("tes.xlsx", index=False)
