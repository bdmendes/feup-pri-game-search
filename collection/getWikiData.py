import sys
import pandas as pd
import os.path
import requests
from tqdm import tqdm


def get_wiki_data(response_name):
    endpoint = 'http://en.wikipedia.org/w/api.php'
    try:
        response = requests.get(endpoint, params={'format': 'json', 'action': 'query', 'prop': 'extracts|categories',
                                'exlimit': 'max', 'explaintext': '', 'exintro': '', 'titles': response_name.replace(' ', '_')})
        pages = response.json()['query']['pages']
        first_page = next(iter(pages.values()))

        if 'categories' in first_page:
            for category in first_page['categories']:
                if 'disambiguation' in category['title']:
                    raise Exception('Disambiguation page')

        description = first_page['extract']
        if description == '' or description == ' ':
            raise Exception('No description found')

        return description
    except:
        return 'None'


def main():
    arg = os.path.dirname(__file__) + '/' + sys.argv[1]

    data = pd.read_csv(arg)

    tqdm.pandas()  # Create new `pandas` methods which use `tqdm` progress

    data['WikiData'] = data['ResponseName'].progress_apply(get_wiki_data)

    data.to_csv(arg, index=False)


if __name__ == "__main__":
    main()
    print("Got wiki data")
