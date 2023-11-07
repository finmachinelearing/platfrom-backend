import json


def dumps(d):
    return json.dumps(d, ensure_ascii=False)
