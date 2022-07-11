from Executor import Executor


def lambda_handler(event, context):
    sources: list = ["bbc", "americanbankingnews", "dailycaller"]
    tasks: list = list()

    for s in sources:
        for i in Executor.execute(s):
            tasks.append({
                "url": i["url"],
                "category": i["category"],
                "source": s
            })

    return {
        'statuscode': 200
    }
