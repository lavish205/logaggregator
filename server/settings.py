from tornado.options import define, options

define('port', default=8888, help='run on the given port', type=int)
define('debug', default=False, help='debug mode')
options.parse_command_line()


settings = {}

settings['debug'] = True
settings['cookie_secret'] = "your-cookie-secret"
settings['xsrf_cookies'] = False

