import sys
import pandas as pd
from utils.utils import group_bool_columns
import os


def main():
    arg = os.path.dirname(__file__) + '/' + sys.argv[1]

    data = pd.read_csv(arg)

    new_platform_column = 'Platforms'
    platform_columns = ['PlatformWindows', 'PlatformLinux', 'PlatformMac']
    group_bool_columns(data, platform_columns, new_platform_column, 8)

    data.to_csv(arg, index=False)


if __name__ == "__main__":
    main()
    print("Grouped platforms")
