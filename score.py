import sys

def score(endpoints):
    totalReqs = 0
    score = 0
    for ep in endpoints:
        for r in ep.requests:
            totalReqs += r.nreq
            for (cache,latency) in ep.cachesByLatency:
                if cache.hasVideo(r.vid):
                    score += (ep.dataCenterLatency - latency)*r.nreq
                    break

    return int(score*1000.0/totalReqs)

#if you want to use on the command line
if __name__ == "__main__":
    if len(sys.argv)!=3:
        print "python score.py problemFile solutionfile"
        sys.exit(1)
    print "Calculating score - note little validation is done on your input file so beware"
#reads in problem file and generates the classes
    from models import *

    for r in requests:
        endpoints[r.epid].addRequests(r)

#read in solution file ready for the score() function
    f = open(sys.argv[2], "r")
    f.readline() # skip count
    for _l in f.readlines():
        l = map(int,_l.split(" "))
        for vid in l[1:]:
            caches[l[0]].addVideo(vid)
    print "SCORE: ",score(endpoints)




# output:
# ncache servers
# cservid video1 video2 etc
