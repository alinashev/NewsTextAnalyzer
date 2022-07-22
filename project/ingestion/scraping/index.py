import json
import uuid

from configurator import IngestionConfigurator
from scraper import Scraper
from loader import Loader


def lambda_handler(event, context):
    try:
        event = event['Records'][0]['body']
        event = json.loads(event)
    except KeyError:
        print("Message empty")
        return

    conf = IngestionConfigurator(event['source'], 'aNews')

    scraper: Scraper = Scraper(event['url'],
                               conf.get_xpath().get(event['source']))

    loader: Loader = Loader(conf.get_table_name(),
                            conf.get_date())

    loader.put(uuid.uuid4().hex, event['category'],
               event['source'], scraper.scrape())

    return {
        'statusCode': 200
    }
