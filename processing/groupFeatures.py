import sys
import pandas as pd
from utils.utils import group_bool_columns
import os


def main():
    arg = os.path.dirname(__file__) + '/' + sys.argv[1]

    data = pd.read_csv(arg)

    new_feature_column = 'Features'
    feature_columns = ['CategoryInAppPurchase', 'CategoryIncludeSrcSDK',
                       'CategoryIncludeLevelEditor', 'CategoryVRSupport']
    group_bool_columns(data, feature_columns, new_feature_column, 8)

    data.to_csv(arg, index=False)


if __name__ == "__main__":
    main()
    print("Grouped features")
