import sys
from more_itertools import first
import pandas as pd
import os.path
import aiohttp
import asyncio
import en_core_web_lg
nlp = en_core_web_lg.load()

#Limit API calls so it does not die
sem = asyncio.Semaphore(1000)

async def get_wiki_data(response_name: str, extra_info: bool = True):
    async with sem:
        endpoint = 'http://en.wikipedia.org/w/api.php'
        try:
            description = ""
            session = aiohttp.ClientSession()
            async with session.get(endpoint, params={'format': 'json', 'action': 'query', 'prop': 'extracts|categories',
                                                    'exlimit': 'max', 'explaintext': '', 'exintro': '', 'titles': response_name.replace(' ', '_')}) as response:
                pages = (await response.json())['query']['pages']
                first_page = next(iter(pages.values()))

                if 'categories' in first_page:
                    for category in first_page['categories']:
                        if 'disambiguation' in category['title']:
                            raise Exception('Disambiguation page')

                description = first_page['extract']
                if description == '' or description == ' ':
                    raise Exception('No description found')
            await session.close()

            if extra_info:
                nlp_processed = nlp(description)
                entities = list(set([X.text for X in nlp_processed.ents if X.label_ ==
                                'GPE' or X.label_ == 'ORG' or X.label_ == 'PERSON']))

                entityData = ' '.join([i for i in await asyncio.gather(*[get_wiki_data(i, extra_info=False) for i in entities if i.capitalize() != response_name.capitalize()]) if i != 'None'])

                if entityData == '':
                    entityData = 'None'

                return (description.replace('\n', ' '), entityData.replace('\n', ' '))
            return description.replace('\n', ' ')
        except Exception as e:
            if str(e) == 'Server disconnected':
                print(e)
            await session.close()
            if extra_info:
                return ('None', 'None')
            else:
                return 'None'


async def main():
    arg = os.path.dirname(__file__) + '/' + sys.argv[1]

    data = pd.read_csv(arg)

    #print(await get_wiki_data("Counter-Strike"))
    wikidata = await asyncio.gather(*[get_wiki_data(i) for i in data['ResponseName']])

    gameWikiData = [i for i, _ in wikidata]
    entityWikiData = [j for _, j in wikidata]

    data["WikiData"] = gameWikiData
    data["EntityWikiData"] = entityWikiData

    data.to_csv(arg, index=False)


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
    print("Got wiki data")
