import sys
import pandas as pd
import os.path


def main():
    arg = os.path.dirname(__file__) + '/' + sys.argv[1]

    data = pd.read_csv(arg)

    data.drop(columns=['QueryID', 'QueryName', 'AchievementHighlightedCount', 'PCReqsHaveMin', 'PCReqsHaveRec', 'LinuxReqsHaveMin', 'LinuxReqsHaveRec', 'MacReqsHaveMin', 'MacReqsHaveRec', 'LegalNotice', 'SupportEmail', 'SupportURL',
              'PriceCurrency', 'AboutText', 'Background', 'ShortDescrip', 'DRMNotice', 'ExtUserAcctNotice', 'LegalNotice', 'ScreenshotCount', 'MovieCount', 'PackageCount', 'SteamSpyOwnersVariance', 'SteamSpyPlayersVariance', 'Reviews'], inplace=True)

    data.rename(
        columns={'DetailedDescrip': 'PromotionalDescription'}, inplace=True)

    data.to_csv(arg, index=False)


if __name__ == "__main__":
    main()
    print("Dropped useless columns")
