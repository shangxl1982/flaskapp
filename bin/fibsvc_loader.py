#!/usr/bin/python

from commands import getstatusoutput
from fib.conf import CONF
status,r = getstatusoutput('nameko run %s --broker %s'%('fib.fib_svc', CONF['amqp_host']))
if status != 0:
    print(r)
exit(status)
