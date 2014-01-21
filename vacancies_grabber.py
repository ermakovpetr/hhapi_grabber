# -*- coding: utf-8 -*-
import json
import urllib2
import pymongo

start_vacancy_id = 9777248
prefix_url = 'https://api.hh.ru/vacancies/'
client = pymongo.MongoClient('localhost', 27017)
db = client['hh']
collection = db['vacancies']


def get_vacancy(v_id):
    response = urllib2.urlopen(prefix_url + str(v_id))
    the_page = response.read()
    vacancy = json.loads(the_page)
    return vacancy

query_result = collection.aggregate([{"$group": {"_id": 0, "minVacanciesId": {"$min": "$id"}}}])
if query_result["ok"] == 1:
    start_vacancy_id = int(query_result["result"][0]["minVacanciesId"]) - 1

for vacancy_id in range(start_vacancy_id, 0, -1):
    try:
        print vacancy_id
        collection.insert(get_vacancy(vacancy_id))
    except urllib2.HTTPError:
        print 'HTTPError ' + str(vacancy_id)
        collection.insert({"id": str(vacancy_id), "error": True})
