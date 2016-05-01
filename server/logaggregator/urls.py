from handlers.api import *

url_patterns = [
    (r'/logs/', LogsHandler),
    (r'/stats/', StatsHandler),
]
