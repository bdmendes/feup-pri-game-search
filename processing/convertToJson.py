import ast
import csv
import json
import sys
import os.path

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def parse_date(date):
    def ok_date(d):
        return len(d) == 10 and d[4] == "-" and d[7] == "-" \
            and d[:4].isdigit() and d[5:7].isdigit() and d[8:].isdigit()

    date = date.split(" ")
    try:
        if len(date) == 3:
            year = date[2].zfill(4)
            month = str(months.index(date[0]) + 1).zfill(2)
            day = date[1].zfill(2)
            date = f"{year}-{month}-{day}"
            if not ok_date(date):
                raise Exception("Invalid date")
            return date
        else:
            year = date[1].zfill(4)
            month = str(months.index(date[0]) + 1).zfill(2)
            date = f"{year}-{month}-01"
            if not ok_date(date):
                raise Exception("Invalid date")
            return date
    except:
        return None


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
                    if "Date" in i or "date" in i:
                        n_row[i] = parse_date(j)
                    else:
                        n_row[i] = j.strip()
                if i not in n_row or n_row[i] == None:
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
