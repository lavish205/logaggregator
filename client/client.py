
import json
import logging
import os
import gevent
import grequests
from requests.exceptions import ConnectionError
from gevent.queue import Queue, Empty

tasks = Queue()


def worker1():
    """
    Worker which will pop task from queue and complete it
    :return: None
    """
    try:
        print "worker running"
        urls = ['http://localhost:8888/logs/']
        while True:
            print "getting task from queue worker 1"
            task = tasks.get()
            
            rs = (grequests.post(u, data=task) for u in urls)
            grequests.map(rs)

    except Empty:
        print "empty"
        pass
    except ConnectionError:
        tasks.put(task)


def worker2():
    """
    Worker which will pop task from queue and complete it
    :return: None
    """
    try:
        print "worker running"
        urls = ['http://localhost:8888/test/']
        while True:
            print "getting task from queue worker 2"
            task = tasks.get()

            rs = (grequests.post(u, data=task) for u in urls)
            grequests.map(rs)

    except Empty:
        print "empty"
        pass
    except ConnectionError:
        tasks.put(task)


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
                # add task to queue
                t = {
                    'data': line,
                    'service': service['name'],
                    'client': client,
                    'client_ip': client_ip
                }
                print "adding task to queue"
                tasks.put(t)

    except IOError as e:
        logging.error("log file not found")
        logging.error(e)


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
        for service in config.get('services', []):
            req.append(gevent.spawn(get_logs, service, client, client_ip))
        gevent.joinall(req)

    except IOError as e:
        logging.error("Config file not found")
        logging.error(e)


if __name__ == '__main__':
    gevent.joinall([
        gevent.spawn(main),
        gevent.spawn(worker1),
        gevent.spawn(worker2)
    ])


