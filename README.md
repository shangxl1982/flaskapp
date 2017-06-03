# flaskapp
## How to build
### check requirements. this project needs:
OS:
Centos 7.x

Python:
SQLAlchemy>=0.9.0
flask>=0.1.0
flasgger
nameko
python-memcached
python-pbr
python-setuptools

Services:
mariadb
memcached
rabbitmq(using docker. "docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management")

### clone this project and:

cd flaskapp && make
Rpms will be in target directory.

## Installation: 

yum install fib-1.x.x-1.x_x86_64.rpm

## Check services: 

systemctl status fib-api
systemctl status fib-svc

## Test suite:

    $python
    >>> from fib import test”
    >>> unittest.main()”

## Configurations:

in /etc/fib/fibsvc.conf:
db_host = mysql://fib:fib@127.0.0.1:3389/fib
mc_hosts = 127.0.0.1:11211
amqp_host = amqp://guest:guest@localhost
listen_port = 8080

## Local access & api test:

http://localhost:8080/apidocs -> default -> post
