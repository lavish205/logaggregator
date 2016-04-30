__author__ = 'lavish'
from handlers.api import *

url_patterns = [
    (r'/logs/', LogsHandler),
    (r'/stats/', LogsHandler),
]
