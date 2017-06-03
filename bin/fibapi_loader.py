#!/usr/bin/python
from fib import app
from fib.conf import CONF

app.app.run(debug=True, port=CONF['listen_port'])
