from models import *
import random


#sort requests by number, highest first
sortedRequests = sorted(requests, key=lambda x:x.nreq, reverse=True)

for r in sortedRequests:
    endpoints[r.epid].addRequests(r)

#for each endpoint, add most popular videos to nearest cache
for e in endpoints:
    for r in e.requests:
        e.addVideoToNearestCache(r.vid)

# produce the output file
print nCaches
for c in caches:
    print c.id,
    for vid in c.videos:
        print vid,
    print

# output:
# ncache servers
# cservid video1 video2 etc
