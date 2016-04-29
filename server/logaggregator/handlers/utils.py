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
from tornado.options import options

es = Elasticsearch()


@coroutine
def es_index(data):
    index = "logs"
    doc_type = data.get('service')
    es.index(index=index, doc_type=doc_type, body=data)


@coroutine
def fetch_from_datastore(apiurl='', url_params={}, headers={}, body={}, datastore='', is_json=False, method='GET'):
    response = None

    if not len(apiurl):
        raise Return(response)
    try:
        start_time = int(round(time.time() * 1000))

        url = url_concat(apiurl, url_params)

        if is_json:
            body = json.dumps(body)
        else:
            body = urlencode(body)

        client = AsyncHTTPClient()

        if method == "GET":
            response_data = yield client.fetch(url, method=method, headers=headers, raise_error=False)
        else:
            response_data = yield client.fetch(url, method=method, headers=headers, body=body, raise_error=False)
        assert response_data and response_data.code in [200, 201, 202, 204]

        response = {
            'headers': response_data.headers,
            'body': json.loads(response_data.body) if response_data.body else None,
            'status': response_data.code
        }
        end_time = int(round(time.time() * 1000))
        logging.info(url+': Time Taken :'+str(end_time - start_time))
    except AssertionError:
        error = json.loads(response_data.body) if response_data.body else response_data.body

        response = {
            'method': method,
            'status_code': response_data.code,
            'error': error,
            'data_store': datastore,
            'url': url
        }
        logging.error(response)
    finally:

        raise Return(response)


def writeObjToResponse(self, object, return_type='json', status=200, headers=None):
    if return_type == 'json':
        if object is not None:
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(object))
        self.set_status(status)
    elif return_type == 'json_gzip':
        zbuf = StringIO()
        zfile = GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
        zfile.write(json.dumps(object))
        zfile.close()

        compressed_content = zbuf.getvalue()
        zbuf.close()

        self.set_header('Content-Type', 'application/json')
        self.set_header('Content-Encoding', 'gzip')
        self.set_header('Content-Length', str(len(compressed_content)))
        self.write(compressed_content)
        self.set_status(status)

    if headers is None:
        self.add_header('Cache-Control', 'no-cache, no-store, must-revalidate')
    else:
        for name, value in headers.items():
            self.add_header(name, value)
