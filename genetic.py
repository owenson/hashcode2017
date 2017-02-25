from models import *
from score import score
import random


#sort requests by number, highest first
sortedRequests = sorted(requests, key=lambda x:x.nreq, reverse=True)

for r in sortedRequests:
    endpoints[r.epid].addRequests(r)

smallestVideo = min(videoSizes)
#assign videos to al caches until fulsl
_score=0
best = 0
while _score < 448000:
    for c in caches:
        c.clear()
        while c.hasSpace(smallestVideo):
            vid = random.randint(0,len(videoSizes)-1)
            if c.hasSpace(vid):
                c.addVideo(vid)

    _score = score(endpoints)
    best = max(_score,best)
    sys.stderr.write("Score: %d (best: %d)\n" % (_score,best))

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
