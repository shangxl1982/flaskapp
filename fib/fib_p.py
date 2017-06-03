from commands import getstatusoutput

def fib_p(value_1, value_2, nsteps):
    tmp_array = None
    cmdline = "fib_c %l %l %l"%(value_1, value_2, nsteps)
    status,r = getstatusoutput(cmdline)
    if status == 0:
        tmp_array = [v.strip() for v in r.split(",") if v]
    return status,tmp_array