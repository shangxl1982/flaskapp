from commands import getstatusoutput

def fib_p(value_1, value_2, nsteps):
    tmp_array = None
    cmdline = "fib_c %ld %ld %ld"%(value_1, value_2, nsteps)
    status,r = getstatusoutput(cmdline)
    if status == 0:
        tmp_array = [float(v.strip()) for v in r.split(",") if v.strip()]
    return status,tmp_array
