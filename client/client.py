import json
import logging
import time
import os
import gevent
import grequests


def send_data(service, data):
    urls = ['http://localhost:8888/test/']
    params = {'data': data, 'service': service}
    rs = (grequests.post(u, data=params) for u in urls)
    req = gevent.spawn(grequests.map, rs)
    gevent.joinall([req])


def get_logs(service):
    file_path = service.get('file')
    service_name = service.get('name')
    print "got service", service_name
    f_obj = open(file_path, 'r')
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
            r = gevent.spawn(send_data,service_name, line)
            gevent.joinall([r])


def main():
    try:
        print "in main"
        config = json.load(open('config.json', 'r'))
        client = config.get('client_name')
        client_ip = config.get('client_ip')
        print "got config file"
        req = []
        for service in config.get('services', []):
            req.append(gevent.spawn(get_logs, service))

        gevent.joinall(req)

    except IOError as e:
        logging.error(e)


if __name__ == '__main__':
    # send_data('s')
    gevent.joinall([
        gevent.spawn(main)
    ])


