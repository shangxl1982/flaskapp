from configobj import ConfigObj

config_f = "/etc/fib/fibsvc.conf"

CONF = None

try:
    CONF = ConfigObj(config_f)
except Exception as e:
    # LOG.warn("Can not read config file. No mc or db available.")
    print("Can not read config file. No mc or db available.")
