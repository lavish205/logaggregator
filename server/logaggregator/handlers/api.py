__author__ = 'lavish'
import logging
from tornado.gen import coroutine
from tornado.web import RequestHandler
from utils import writeObjToResponse, es_index, es


class LogsHandler(RequestHandler):
    """
    Test handler
    """
    @coroutine
    def get(self, *args, **kwargs):
        es.search(index="logs", )

    @coroutine
    def post(self, *args, **kwargs):
        data = {
            'log': self.get_argument('data', None),
            'service': self.get_argument('service', None),
            'client': self.get_argument('client', None),
            'client_ip': self.get_argument('client_ip', None)
        }
        print data
        # es_index(data)
        self.finish()
