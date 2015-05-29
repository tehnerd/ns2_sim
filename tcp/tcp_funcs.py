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
    ts_size = 1.0/resolution
    print(ts_size)
    qlen = list()
    drlist = list()
    timelist = list()
    curlen = 0
    curdr = 0
    with open(fname) as fd:
        for line in fd:
            line = line.split()
            if line[0] == "r" or line[2] != "0":
                continue
            t = float(line[1])
            if t > ts_start+ts_size:
                qlen.append(curlen)
                drlist.append(curdr)
                curdr = 0
                timelist.append(ts_start+ts_size)
                zero_timeframes = (t-(ts_start + ts_size))//ts_size
                while zero_timeframes != 0:
                    zero_timeframes -= 1
                    qlen.append(curlen)
                    drlist.append(curdr)
                    ts_start += ts_size
                    timelist.append(ts_start+ts_size)
                ts_start+=ts_size
            if line[0] == "+":
                curlen+=1
            if line[0] == "-" or line[0] == "d":
                curlen-=1
            if line[0] == "d":
                curdr += 1
    return timelist,qlen,drlist
