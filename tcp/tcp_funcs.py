import pylab
def parse_cwnd(fname):
    fd = open(fname)
    x = list()
    y = list()
    for line in fd:
        line = line.split()
        if len(line) >= 2:
            x.append(float(line[0]))
            y.append(float(line[1].strip("\n")))
    fd.close()
    return x,y


def parse_cwnd_many(fname):
    with open(fname) as fd:
        window_dict = dict()
        for line in fd:
            line = line.split()
            if len(line) >= 4:
                name = (line[2],line[3])
                if name in window_dict:
                    window_dict[name]["t"].append(float(line[0]))
                    window_dict[name]["val"].append(float(line[1]))
                else:
                    window_dict[name] = dict()
                    window_dict[name]["t"] = list()
                    window_dict[name]["val"] = list()
                    window_dict[name]["t"].append(float(line[0]))
                    window_dict[name]["val"].append(float(line[1]))
        return window_dict




def parse_bw_2nodes(fname,resolution):
    #starting point of time slice and slice's size
    ts_start= 0.0
    ts_size = 1.0/resolution
    print(ts_size)
    bwlist = list()
    timelist = list()
    prlist = list()
    curbw = 0
    curpr = 0
    with open(fname) as fd:
        for line in fd:
            line = line.split()
            if line[0] == "r":
                t = float(line[1])
                if t > ts_start+ts_size:
                    bwlist.append((curbw/ts_size)*8)
                    prlist.append(curpr/ts_size)
                    timelist.append(ts_start+ts_size)
                    curbw = 0
                    curpr = 0
                    zero_timeframes = (t-(ts_start + ts_size))//ts_size
                    while zero_timeframes != 0:
                        zero_timeframes -= 1
                        bwlist.append((curbw/ts_size)*8)
                        prlist.append(curpr/ts_size)
                        ts_start += ts_size
                        timelist.append(ts_start+ts_size)
                    ts_start+=ts_size
                curbw+=int(line[5])
                curpr+=1
    return timelist,bwlist,prlist


def parse_qlen_2nodes(fname,resolution):
    #starting point of time slice and slice's size
    ts_start= 0.0
    #queue delay dict
    qdd = {}
    ts_size = 1.0/resolution
    print(ts_size)
    qlen = []
    qdelay = []
    drlist = []
    timelist = []
    curlen = 0
    curdr = 0
    curqdelay_list = []
    curdelay = 0.0
    with open(fname) as fd:
        for line in fd:
            line = line.split()
            if line[0] == "r" or line[2] != "0":
                continue
            t = float(line[1])
            if t > ts_start+ts_size:
                for k in curqdelay_list:
                    curdelay += k
                # avg delay; 1000000 because resolution is in msec
                curdelay = curdelay / len(curqdelay_list)* 1000000
                if curlen < 0:
                    curlen = 0
                qlen.append(curlen)
                drlist.append(curdr)
                qdelay.append(curdelay)
                curdr = 0
                timelist.append(ts_start+ts_size)
                zero_timeframes = (t-(ts_start + ts_size))//ts_size
                while zero_timeframes != 0:
                    zero_timeframes -= 1
                    qlen.append(curlen)
                    qdelay.append(curdelay)
                    drlist.append(curdr)
                    ts_start += ts_size
                    timelist.append(ts_start+ts_size)
                ts_start+=ts_size
                curdelay = 0
            if line[0] == "+":
                qdd[line[11]] = float(line[1])
                curlen+=1
            if line[0] == "-":
                curlen-=1
                curqdelay_list.append(float(line[1])-qdd[line[11]])
                del(qdd[line[11]])
            if line[0] == "d":
                curlen-=1
                curdr += 1
    return timelist,qlen,drlist,qdelay

def plot2(n, draw_delay = False):
    pylab.ion()
    x,y,z = parse_bw_2nodes("out.ns",n)
    t,q,d,qd = parse_qlen_2nodes("out.ns",n)
    a,b = parse_cwnd("n0w.ns")
    pylab.subplot(411)
    pylab.plot(t,q)
    # queue delay
    if draw_delay:
        pylab.plot(t,qd)
    pylab.subplot(412)
    pylab.plot(t,d)
    pylab.subplot(413)
    pylab.plot(x,y)
    pylab.subplot(414)
    pylab.plot(a,b)
    pylab.draw()

def plot2_log(n):
    pylab.ion()
    x,y,z = parse_bw_2nodes("out.ns",n)
    t,q,d,qd = parse_qlen_2nodes("out.ns",n)
    a,b = parse_cwnd("n0w.ns")
    pylab.subplot(411).set_yscale("log")
    pylab.plot(t,q)
    pylab.plot(t,qd)
    pylab.subplot(412)
    pylab.plot(t,d)
    pylab.subplot(413)
    pylab.plot(x,y)
    pylab.subplot(414)
    pylab.plot(a,b)
    pylab.draw()
