import os
from tornado.options import define, options

path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ROOT = path(ROOT, 'logaggregator/templates')

define('TEMPLATE_ROOT', default = TEMPLATE_ROOT, type = str, help = 'template root path')
define('port', default=8888, help='run on the given port', type=int)
define('debug', default=False, help='debug mode')
options.parse_command_line()


settings = dict()
settings['debug'] = True

