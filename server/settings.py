from tornado.options import define, options

define('port', default=8888, help='run on the given port', type=int)
define('debug', default=False, help='debug mode')
options.parse_command_line()


settings = dict()
settings['debug'] = True

