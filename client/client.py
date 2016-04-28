
import json
import logging
import time
import os
import gevent
import grequests
import requests
from requests.exceptions import ConnectionError
from gevent.queue import Queue, Empty

tasks = Queue()


def exception_handler(req, exc):
    print req
    print exc


def worker1():
    try:
        print "worker running"
        urls = ['http://localhost:8888/test/']
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
    file_path = service.get('file')
    service_name = service.get('name')
    print "got service", service_name

    try:
        f_obj = open(file_path, 'r')

    except IOError as e:
        logging.error(e)

    st_results = os.stat(file_path)
    st_size = st_results[6]
    f_obj.seek(st_size)

    while 1:
        where = f_obj.tell()
        line = f_obj.readline()
        if not line:
            gevent.sleep(1)
            f_obj.seek(where)
        else:
            t = {
                'data': line,
                'service': service['name'],
                'client': client,
                'client_ip': client_ip
            }
            print "adding task to queue"
            tasks.put(t)


def main():
    try:
        config = json.load(open('config.json', 'r'))
        client = config.get('client_name')
        client_ip = config.get('client_ip')

        req = []
        for service in config.get('services', []):
            req.append(gevent.spawn(get_logs, service, client, client_ip))
        gevent.joinall(req)

    except IOError as e:
        logging.error(e)


if __name__ == '__main__':
    gevent.joinall([
        gevent.spawn(main),
        gevent.spawn(worker1),
        gevent.spawn(worker2)
    ])


