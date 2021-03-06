import gevent
import grequests
import json
import logging
import os
from itertools import count
from gevent.queue import Queue, Empty, Full
from requests.exceptions import ConnectionError

# creating a global queue to add all the tasks
tasks = Queue()


class Worker(object):
    """
    Worker which will pop task from queue and complete it
    """
    _count = count(0)

    def __init__(self):
        # setting url of the server where logs will be shipped
        self.urls = [os.getenv('SERVER_IP', 'http://127.0.0.1:8888/logs/')]
        self.count = self._count.next()  # counts of number of worker

    def start(self):
        """
        starts poping task from queue and complete it
        :return:
        """
        print "worker %d running " % self.count
        try:
            while True:
                print "got task from worker %d" % self.count
                task = tasks.get()
                rs = (grequests.post(u, data=task) for u in self.urls)
                grequests.map(rs)
        except ConnectionError:
            tasks.put(task)
        except Empty:
            logging.error("Queue is empty")


def get_logs(service, client, client_ip):
    """
    listen to log file for each new entries and add them to queue
    :param service: name of the service
    :param client: client name
    :param client_ip: client ip
    :return:
    """
    file_path = service.get('file')
    service_name = service.get('name')
    print "got service", service_name

    try:
        f_obj = open(file_path, 'r')
        st_results = os.stat(file_path)
        st_size = st_results[6]
        f_obj.seek(st_size)

        while 1:
            where = f_obj.tell()  # get current file position
            line = f_obj.readline()  # read file from current position
            if not line:
                # if no entry is found check again after 1 sec
                gevent.sleep(1)
                f_obj.seek(where)
            else:
                # Got new line in log file, adding it to queue
                t = {
                    'data': line,
                    'service': service['name'],
                    'client': client,
                    'client_ip': client_ip
                }
                print "adding task to queue"
                tasks.put(t, block=False)

    except IOError as e:
        logging.error("log file not found")
        logging.error(e)

    except Full:
        logging.error("Queue is full, Out of memory")


def main():
    """
    parse the config file and get list of services
    :return: None
    """
    try:
        config = json.load(open('config.json', 'r'))
        client = config.get('client_name')
        client_ip = config.get('client_ip')

        req = []
        # getting all services from config file
        for service in config.get('services', []):
            req.append(gevent.spawn(get_logs, service, client, client_ip))
        gevent.joinall(req)

    except IOError as e:
        logging.error("Config file not found")
        logging.error(e)


if __name__ == '__main__':
    # initializing two workers
    w1 = Worker()
    w2 = Worker()
    # spawning all tasks
    gevent.joinall([
        gevent.spawn(main),
        gevent.spawn(w1.start),
        gevent.spawn(w2.start)
    ])


