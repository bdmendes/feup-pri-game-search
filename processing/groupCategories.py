import sys
import pandas as pd
from utils.utils import group_bool_columns

def main():
    arg = sys.argv[1]

    data = pd.read_csv(arg)

    new_category_column = 'Categories'
    category_columns = ['CategorySinglePlayer', 'CategoryMultiplayer', 'CategoryCoop', 'CategoryMMO']
    group_bool_columns(data, category_columns, new_category_column, 8)

    data.to_csv(arg, index=False)
