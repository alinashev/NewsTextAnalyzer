import json

from Executor import Executor
from QueueWriter import QueueWriter


def lambda_handler(event, context):
    sources: list = ["bbc", "dailycaller", "americanbankingnews"]

    for s in sources:
        for i in Executor.execute(s):
            QueueWriter.write('a-news', json.dumps({
                "url": i["url"],
                "category": i["category"],
                "source": s
            }))

    return {
        'statuscode': 200
    }
