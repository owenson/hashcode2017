from models import *
from score import score
import random

#sort requests by number, highest first
sortedRequests = sorted(requests, key=lambda x:x.nreq, reverse=True)

#GOAL
#For each cache, if we store video X here, what are the savings, Order at each cache by most savings first
#then assign

sys.stderr.write( "calculating savings\n")
for r in sortedRequests:
    ep = endpoints[r.epid]
    ep.addRequests(r)
    for (c, cachePing) in ep.endpointLatencyToCacheServer.items():
        dataCenterPing = ep.dataCenterLatency
        saving = (dataCenterPing - cachePing)*r.nreq #saving if assigned here
        c.addRequestSavings(r, saving)

for c in caches:
    c.finalise()

sys.stderr.write( "doing assignments\n")
actioned = True
while actioned:
    actioned = False
    bestSaving = 0
    bestRequest = False
    bestCache = False
    for c in caches:
        if len(c.requestsSavings) > 0:
            req = c.requestsSavings[0][0]
            saving = c.requestsSavings[0][1]

            while req.serviced:
                c.requestsSavings.pop(0)
                if len(c.requestsSavings) == 0:
                    continue
                req = c.requestsSavings[0][0]
                saving = c.requestsSavings[0][1]

            if c.hasVideo(req.vid):
                req.serviced = True
                c.requestsSavings.pop(0)
                continue

            if c.hasSpace(req.vid) and req.serviced==False:
                if saving > bestSaving:
                    bestSaving = saving
                    bestRequest = req
                    bestCache = c
                #c.addVideo(req.vid)
                #req.serviced = True
                #c.requestsSavings.pop(0)
    if bestRequest:
        bestCache.addVideo(bestRequest.vid)
        bestRequest.serviced = True
        actioned = True

sys.stderr.write("Score: %d\n" % score(endpoints))

# produce the output
print nCaches
for c in caches:
    print c.id,
    for vid in c.videos:
        print vid,
    print

# output:
# ncache servers
# cservid video1 video2 etc
