import json

from extractor import Extractor
from queuewriter import QueueWriter


def lambda_handler(event, context):
    source = event['Source']

    extractor: Extractor = Extractor(source)
    extractor.extract()
    for i in extractor.get_news():
        QueueWriter.write('a-news', json.dumps({
            "url": i["url"],
            "category": i["category"],
            "source": source
        }))

    return {
        'statuscode': 200
    }
