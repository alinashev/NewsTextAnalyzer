import json
import os
import uuid

from configurator import IngestionConfigurator
from news import News
from streamloader import Stream
from scraper import Scraper
from dynamoloader import Dynamo


def lambda_handler(event, context):
    try:
        event = event['Records'][0]['body']
        event = json.loads(event)
    except KeyError:
        print("Message empty")
        return

    conf: IngestionConfigurator = IngestionConfigurator(
        event['source'],
        os.environ['DYNAMODB_TABLE_NAME'],
        os.environ['STREAM_NAME']
    )

    scraper: Scraper = Scraper(
        event['url'], conf.get_xpath().get(event['source'])
    )

    news: dict = News(
        uuid.uuid4().hex, conf.get_date(),
        event['category'], event['source'],
        scraper.scrape()
    ).__dict__

    Dynamo(conf.get_table_name(), conf.get_date()).put(news)
    Stream(conf.get_stream_name(), conf.get_date()).put(news)

    return {
        'statusCode': 200
    }
