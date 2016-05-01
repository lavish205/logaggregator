from __future__ import absolute_import
import datetime
from tornado import gen
from tornado.escape import json_encode
from tornado.options import options
from tornado.template import Loader, Template
from tornado.web import RequestHandler
import psutil
from .utils import writeObjToResponse, es_index, search_log


class LogsHandler(RequestHandler):
    """
    Logs handler which will index logs and get the required logs
    """
    @gen.coroutine
    def get(self, *args, **kwargs):
        doc_type = self.get_query_argument('service', None)

        query = self.get_query_argument('query', None)
        context = search_log(doc_type, query)
        templateRoot = options.TEMPLATE_ROOT
        loader = Loader(templateRoot)
        templateName = 'logs.html'
        response = loader.load(templateName).generate(**context)
        writeObjToResponse(self, object=context, status=200)
        self.finish()

    @gen.coroutine
    def post(self, *args, **kwargs):
        data = {
            'log': self.get_argument('data', None),
            'service': self.get_argument('service', None),
            'client': self.get_argument('client', None),
            'client_ip': self.get_argument('client_ip', None),
            'created_at': datetime.datetime.now()
        }
        print data
        if self.get_argument('data', None):
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
        context = {
            'cpu': {
                'user': psutil.cpu_times_percent().user,
                'system': psutil.cpu_times_percent().system,
                'idle': psutil.cpu_times_percent().idle,
                'iowait': psutil.cpu_times_percent().iowait,
                'usage': psutil.cpu_percent()
            },
            'memory': {
                'percent': psutil.virtual_memory().percent,
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'used': psutil.virtual_memory().used,
                'free': psutil.virtual_memory().free,
                'cached': psutil.virtual_memory().cached
            }
        }
        templateRoot = options.TEMPLATE_ROOT
        loader = Loader(templateRoot)
        templateName = 'stats.html'
        response = loader.load(templateName).generate(**context)
        self.write(response)
        self.finish()
