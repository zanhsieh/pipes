#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import json
import datetime
from urllib import parse, request

key = os.getenv("ENTITIES_KEY")


def analyze(text, entity_type):
    query = parse.urlencode({"text": text, "lang": "en"}, encoding="utf-8", errors="replace")
    params = query.encode("utf-8", "replace")
    req = request.Request("http://api.syllabs.com/v0/entities", params)
    req.add_header("API-Key", key)
    r = request.urlopen(req)
    resp = r.read()
    data = json.loads(resp.decode("utf-8", "replace"))
    entities = data["response"]["entities"]
    return entities.get(entity_type, [])


def display(entities):
    entities.sort(key=lambda ent: int(ent["count"]), reverse=True)
    for entity in entities:
        print("%s: %s" % (entity["text"], entity["count"]))


def main():
    start_time = datetime.datetime.now()
    texts = ""
    for line in sys.stdin:
        texts += line

    entities = analyze(texts, "Person")

    display(entities)
    elsapsed_time = datetime.datetime.now() - start_time
    # print(elsapsed_time)


if __name__ == '__main__':
    main()
