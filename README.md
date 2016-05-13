# logaggregator
Ships logs from clients to centeralized server.

### Project Setup
============================
#### Installing Requirements
```shell
$ git clone git@github.com:lavish205/logaggregator.git
$ cd logaggregator
$ pip install -r requirements.txt
```
#### Client Side
* Edit `config.json` and add all the service and log file path that should be shipped to server
Ex:
```json
{
  "client_name": "<client name to distinguish among different server>",
  "client_ip": "<ip of the client>",
  "services":[
    {
      "name": "<service name>",
      "file": "<path to log file>"
    }
  ]

}
```
* Set Enviornment variable "SERVER_IP" as http://_server_ip_:8888/logs/
* Run `client.py`
> $ python client.py

#### Server Side
* Setup ElasticSearch

  > $ curl -L -O https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.2.0/elasticsearch-2.2.0.tar.gz

* Run ElasticSearch

  > $ elasticsearch/bin/elasticsearch -d # running as daemon

* Run `app.py`

  > $ python app.py

### Endpoints
========================
#### 1. Real Time log streaming:
  > /logs/

  **Query Params**:
    * _service_: filter logs according to given service value
    * _query_: filter logs through given text

#### 2. System Statistics Information (CPU, Mem, etc):
  > /stats/


Access panel at : [http://127.0.0.1:8888/](http://127.0.0.1:8888/)
