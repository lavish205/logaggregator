import time
import os
import grequests


def send_data(data):
    urls = ['http://localhost:8888/test/']
    params = {'data': data}
    rs = (grequests.post(u, data=params) for u in urls)
    grequests.map(rs)


def main():

    # Set the file path and open the file
    file_path = '/var/log/redis/redis-server.log'
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
            send_data(line)  # already has newline
            # print line
if __name__ == '__main__':
    # send_data('s')
    main()

