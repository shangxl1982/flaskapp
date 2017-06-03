from nameko.rpc import rpc, RpcProxy
from sqlalchemy import *
import memcache
import json
from fib.msg_template import ret_msg_template
from configobj import ConfigObj
from fib.fib_p import fib_p

config_f = "/etc/fib/fibsvc.conf"

class fib(object):
    name = "fib"
    mail = RpcProxy('fib')

    def __init__(self):
        self.mc = None
        self.db_engine = None
        self.db_conn = None
        try:
            config = ConfigObj(config_f)
        except Exception as e:
            LOG.warn("Can not read config file. No mc or db available.")
            return
        last_calc_rst = None
        try :
            self.db_engine = create_engine(config['db_host'], echo, module)
            self.db_conn = db_engine.connect()
            last_calc_rst = db_conn.execute("select * from fib_rst_table where rec_id == 0")
        except Exception as e:
            LOG.warn("Can not connect database, will not loading fib data")
            self.db_engine = None
            self.db_conn = None
        try :
            self.mc = memcache.Client(config['mc_hosts'],debug=0)
            if self.mc.get('fib_prefix_maxstep_rst'):
                return
            elif ( last_calc_rst ):
                self.mc.set ('fib_prefix_maxstep_rst', '%s'%last_calc_rst['fib_rst'])
            else:
                tmp = {'maxsteps': 2, 'rst_array':[0,1]}
                self.mc.set('fib_prefix_maxstep_rst', '%s' % json.dumps(tmp))
        except Exception as e:
            LOG.warn("Can not connect memcache, will not loading fib data")
            self.mc = None
        return
    @rpc
    def fib(self, nstep):
        msg = ret_msg_template
        if self.mc:
            mc_rst = json.loads(self.mc.get('fib_prefix_maxstep_rst'))
            if nstep <= mc_rst['maxsteps']:
                msg['result'] = str(mc_rst['rst_array'][0:nstep])
            else:
                # call the python backend to calculate
                ret,tmp_a = fib_p(mc_rst['rst_array'][-2], mc_rst['rst_array'][-1], nstep - mc_rst['maxsteps'])
                if ret == 0:
                    mc_rst['rst_array'] += tmp_a
                # memcached will serialize the get/set op, so the only concern is we may invalid
                # a value set by other caller which may have a better fib arrary. use get and set to
                # minimize the side effect here. To imp a lock here is not necessary.
                mc_rst = json.loads(self.mc.get('fib_prefix_maxstep_rst'))
                if mc_rst['maxsteps'] < nstep:
                    mc_rst['maxsteps'] = nstep
                    self.mc.set('fib_prefix_maxstep_rst',json.dumps(mc_rst))
                    # update the database either
                    if self.db_conn:
                        self.db_conn.execute("update fib_rst_table set fib_rst = \'%s\' where rec_id == 0 "
                                             %json.dumps(mc_rst))
                msg['result'] = mc_rst['rst_array']
        else:
            # ok no mc available
            ret,tmp_a = fib_p(0, 1, nstep-2)
            if ret == 0:
                msg['result'] = tmp_a
        return msg
