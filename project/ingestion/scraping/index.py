import json

from Configurator import Configurator
from Executor import Executor


def lambda_handler(event, context):
    try:
        event = event['Records'][0]['body']
        event = json.loads(event)
    except KeyError:
        print("Message empty")
        return

    conf = Configurator(event['source'], 'testTable')
    Executor.execute(event['url'],
                     event['category'],
                     event['source'],
                     **conf.get_param())

    return {
        'statusCode': 200
    }
