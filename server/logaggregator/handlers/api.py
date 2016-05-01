__author__ = 'lavish'
from tornado import gen
from tornado.web import RequestHandler
from tornado.options import options
from tornado.template import Loader, Template
from .utils import writeObjToResponse, es_index, es
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