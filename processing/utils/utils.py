import json
import csv
import ast


def group_bool_columns(df, cols_name, new_col_name, index) -> None:
    new_category_data = []

    for i in range(df.shape[0]):
        new_category_data.append(
            [j[index:] for j, k in df.iloc[i][cols_name].items() if k == True])

    df.drop(columns=cols_name, inplace=True)
    df[new_col_name] = new_category_data


def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            nRow = {}
            for i, j in row.items():
                try:
                    nRow[i] = ast.literal_eval(str(j))
                except:
                    if j == " ":
                        nRow[i] = ""
                    else:
                        nRow[i] = j

            jsonArray.append(nRow)

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)
