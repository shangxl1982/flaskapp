import unittest
import requests
import json
from nameko.standalone.rpc import ClusterRpcProxy
from fib.conf import CONF

class test_fib_api(unittest.TestCase):
    def setUp(self):
        self.uri = 'http://localhost:%s/fib'%str(CONF['listen_port'])

    def test_api(self):
        # normal
        r = requests.post(self.uri, json.dumps({'nstep':10}), headers={"Content-Type": "application/json"})
        self.assertTrue(r.json()['errcode'] == 200)
        # invalid input 1
        r = requests.post(self.uri, json.dumps({'nstep1': 10}), headers={"Content-Type": "application/json"})
        self.assertTrue(r.json()['errcode'] == 400)
        # invalid input 2
        r = requests.post(self.uri, json.dumps({'nstep': 0 }), headers={"Content-Type": "application/json"})
        self.assertTrue(r.json()['errcode'] == 400)
        # invalid input 3
        r = requests.post(self.uri, json.dumps({'nstep': -1 }), headers={"Content-Type": "application/json"})
        self.assertTrue(r.json()['errcode'] == 400)

    def test_backend(self):
        with ClusterRpcProxy({'AMQP_URI': CONF['amqp_host']}) as rpc:
            msg = rpc.fib.fib(50)
            rst = [0.0, 1.0, 1.0, 2.0, 3.0, 5.0, 8.0, 13.0, 21.0, 34.0, 55.0, 89.0, 144.0, 233.0, 377.0,
                   610.0, 987.0, 1597.0, 2584.0, 4181.0, 6765.0, 10946.0, 17711.0, 28657.0, 46368.0, 75025.0,
                   121393.0, 196418.0, 317811.0, 514229.0, 832040.0, 1346269.0, 2178309.0, 3524578.0,
                   5702887.0, 9227465.0, 14930352.0, 24157817.0, 39088169.0, 63245986.0, 102334155.0,
                   165580141.0, 267914296.0, 433494437.0, 701408733.0, 1134903170.0, 1836311903.0,
                   2971215073.0, 4807526976.0, 7778742049.0]
            self.assertTrue(msg['errcode'] == 200)
            self.assertTrue(cmp(str(rst), str(msg['result'])) == 0)


if __name__ == '__main__':
   unittest.main()
