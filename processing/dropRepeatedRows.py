import sys
import pandas as pd
import os.path


def main():
    arg = os.path.dirname(__file__) + '/' + sys.argv[1]

    data = pd.read_csv(arg)

    data.drop_duplicates(subset='ResponseID',
                         inplace=True)

    data.to_csv(arg, index=False)


if __name__ == "__main__":
    main()
    print("Dropped repeated rows")
