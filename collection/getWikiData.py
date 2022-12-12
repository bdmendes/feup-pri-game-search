import sys
import pandas as pd
import os.path
import aiohttp
import asyncio

async def get_wiki_data(response_name):
    endpoint = 'http://en.wikipedia.org/w/api.php'
    session = aiohttp.ClientSession()
    try:
        description = ""
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
        return description.replace("\n", " ")
    except:
        await session.close()
        return 'None'


async def main():
    arg = os.path.dirname(__file__) + '/' + sys.argv[1]

    data = pd.read_csv(arg)

    data['WikiData'] = await asyncio.gather(*[get_wiki_data(i) for i in data['ResponseName']])

    data.to_csv(arg, index=False)


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
    print("Got wiki data")
