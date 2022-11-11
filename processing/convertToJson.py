import ast
import csv
import json
import sys
import os.path

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def parse_date(date):
    date = date.split(" ")
    year = date[2].zfill(4)
    month = str(months.index(date[0]) + 1).zfill(2)
    day = date[1].zfill(2)
    return f"{year}-{month}-{day}"


def csv_to_json(csv_file_path, json_file_path):
    json_arr = []

    with open(csv_file_path, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)
        for row in csv_reader:
            n_row = {}
            for i, j in row.items():
                try:
                    n_row[i] = ast.literal_eval(str(j))
                except:
                    try:
                        n_row[i] = parse_date(j)
                    except:
                        n_row[i] = j.strip()
                if n_row[i] == None:
                    n_row[i] = ""

            json_arr.append(n_row)

    with open(json_file_path, 'w', encoding='utf-8') as jsonf:
        json_str = json.dumps(json_arr, indent=4)
        jsonf.write(json_str)


def main():
    csv_file_path = os.path.dirname(__file__) + '/' + sys.argv[1]
    json_file_path = csv_file_path.replace(".csv", ".json")
    csv_to_json(csv_file_path, json_file_path)


if __name__ == "__main__":
    main()
    print("Converted to json")
