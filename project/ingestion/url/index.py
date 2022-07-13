import json

from extractor import Extractor
from queuewriter import QueueWriter


def lambda_handler(event, context):
    sources = event["Source"]

    for s in sources:
        extractor: Extractor = Extractor(s)
        extractor.extract()
        for i in extractor.get_news():
            QueueWriter.write('a-news', json.dumps({
                "url": i["url"],
                "category": i["category"],
                "source": s
            }))

    return {
        'statuscode': 200
    }
