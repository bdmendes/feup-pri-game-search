import sys
import pandas as pd

def main():
    arg = sys.argv[1]

    data = pd.read_csv(arg)

    data.drop(columns=['QueryID','QueryName', 'AchievementHighlightedCount', 'PCReqsHaveMin', 'PCReqsHaveRec', 'LinuxReqsHaveMin', 'LinuxReqsHaveRec', 'MacReqsHaveMin', 'MacReqsHaveRec', 'LegalNotice', 'SupportEmail', 'SupportURL', 'PriceCurrency', 'AboutText', 'Background', 'ShortDescrip', 'DRMNotice', 'ExtUserAcctNotice', 'LegalNotice', 'ScreenshotCount', 'MovieCount', 'PackageCount', 'SteamSpyOwnersVariance', 'SteamSpyPlayersVariance', 'Reviews'], inplace=True)

    data.to_csv(arg, index=False)
