
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
            # print tasks
            print "getting task from queue worker 1"
            task = tasks.get()
            # print task
            rs = requests.post(urls[0], task)
            if not rs.status_code == 200:
                tasks.put(task)
            # rs = (grequests.post(u, data=task) for u in urls)
            # req = gevent.spawn(grequests.map, rs)
            # gevent.joinall([req])
            print task
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
            # print tasks
            print "getting task from queue worker 2"
            task = tasks.get()
            # print task
            rs = requests.post(urls[0], task)
            if not rs.status_code == 200:
                tasks.put(task)
            # rs = (grequests.post(u, data=task) for u in urls)
            # req = gevent.spawn(grequests.map, rs)
            # gevent.joinall([req])
            print task
    except Empty:
        print "empty"
        pass
    except ConnectionError:
        tasks.put(task)


def send_data(data, service, client, ip):
    print "sending"
    urls = ['http://localhost:8888/test/']
    params = {
        'data': data,
        'service': service,
        'client': client,
        'client_ip': ip
    }
    rs = (grequests.post(u, data=params) for u in urls)
    req = gevent.spawn(grequests.map, rs)
    gevent.joinall([req])


def get_logs(service, client, client_ip):
    file_path = service.get('file')
    service_name = service.get('name')
    print "got service", service_name

    try:
        f_obj = open(file_path, 'r')

    except IOError as e:
        logging.error(e)

    # Find the size of the file and move to the end
    st_results = os.stat(file_path)
    st_size = st_results[6]
    f_obj.seek(st_size)

    while 1:
        where = f_obj.tell()
        line = f_obj.readline()
        if not line:
            time.sleep(1)
            f_obj.seek(where)
        else:
            t = {
                'data': line,
                'service': service['name'],
                'client': client,
                'client_ip': client_ip
            }
            print "adding task to queuw"
            tasks.put(t)
            # r = gevent.spawn(send_data, line, service_name, client, client_ip)
            # gevent.joinall([r])


def main():
    try:
        config = json.load(open('config.json', 'r'))
        client = config.get('client_name')
        client_ip = config.get('client_ip')
        # print "got config file"

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


