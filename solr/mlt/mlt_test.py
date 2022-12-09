import requests
import sys

QUERY_TEXT = sys.argv[1]

QUERY = f"http://localhost:8983/solr/games_tuned/select?bf=sum(sum(mul(0.5%2CMetacritic)%2Cmul(10%2Clog(SteamSpyPlayersEstimate)))%2Cmul(15%2Clog(RecommendationCount)))&defType=edismax&indent=true&q.op=OR&q=ResponseName%3A%22{QUERY_TEXT}%22~2%5E4%2C%0APromotionalDescription%3A%22{QUERY_TEXT}%22~2%2C%0AWikiData%3A%22{QUERY_TEXT}%22~2%5E3"
print(QUERY)

results = requests.get(QUERY).json()['response']['docs']

titles = [i["ResponseName"] for i in results]
print(titles)
if len(titles) == 0:
    print("No data")
    exit(0)

i = 0
while i < 1 or i > len(titles): i = int(input(f"Choose which title do you want to search more about (1-{len(titles)}):"))

title_chosen = titles[i - 1]

print(title_chosen)

MLT_QUERY = f"http://localhost:8983/solr/games_tuned/mlt?defType=edismax&indent=true&q.op=OR&q={title_chosen}&df=ResponseName&mlt.fl=PromotionalDescription,ResponseName"
results = requests.get(MLT_QUERY).json()['response']['docs']
titles = [i["ResponseName"] for i in results]

print(titles)