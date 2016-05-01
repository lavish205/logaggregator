from __future__ import absolute_import
import json
import time
import logging
from elasticsearch import Elasticsearch
from StringIO import StringIO
from gzip import GzipFile
from urllib import urlencode
from tornado.gen import coroutine, Return
from tornado.httpclient import AsyncHTTPClient
from tornado.httputil import url_concat

es = Elasticsearch()
INDEX = "logs"


@coroutine
def es_index(data):
    """
    index provided data to elasticsearch
    :param data: data to be indexed
    :return: None
    """
    doc_type = data.get('service')
    es.index(index=INDEX, doc_type=doc_type, body=data)


def search_log(doc_type, query):
    """
    search requested logs from elasticsearch
    :param doc_type: service
    :param query: search query
    :return: filtered logs
    """
    if query:
        body = {
            "from": 0,
            "size": 50,
            "sort": [
               {
                  "created_at": {
                     "order": "desc"
                  }
               }
            ],
            "query": {
                "term": {
                    "_all": "the"
                }
            }
        }
    else:
        body = {
            "from": 0,
            "size": 50,
            "sort": [
               {
                  "created_at": {
                     "order": "desc"
                  }
               }
            ]
        }
    if doc_type:
        print "condition 1 true"
        res = es.search(index="logs", doc_type=str(doc_type).strip(), body=body)
    else:
        res = es.search(index="logs", body=body)

    data = []
    if not res.get('timed_out'):
        for item in res["hits"]["hits"]:
            data.append({
                'client_ip': item['_source'].get('client_ip'),
                'client': item['_source'].get('client'),
                'log': item['_source'].get('log'),
                'service': item['_source'].get('service'),
            })
    response = {"data": data}
    return response


def writeObjToResponse(self, object, status=200, headers=None):
    """
    write response in json format to client
    :param self:
    :param object: response as a json object
    :param status: status code
    :param headers: headers to be included
    :return: response
    """
    if object is not None:
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(object))
    self.set_status(status)

    if headers is None:
        self.add_header('Cache-Control', 'no-cache, no-store, must-revalidate')
    else:
        for name, value in headers.items():
            self.add_header(name, value)
