__author__ = 'lavish'
from tornado import gen
from tornado.web import RequestHandler
from utils import writeObjToResponse, es_index, es
import psutil


class LogsHandler(RequestHandler):
    """
    Logs handler which will index logs and get the required logs
    """
    @gen.coroutine
    def get(self, *args, **kwargs):
        service = self.get_query_argument('service')
        # es.search(index="logs", )

    @gen.coroutine
    def post(self, *args, **kwargs):
        data = {
            'log': self.get_argument('data', None),
            'service': self.get_argument('service', None),
            'client': self.get_argument('client', None),
            'client_ip': self.get_argument('client_ip', None)
        }
        print data
        es_index(data)


class StatsHandler(RequestHandler):
    """

    """
    def get(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        response = {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent
        }