from models import *


#sort requests by number, highest first
sortedRequests = sorted(requests, key=lambda x:x.nreq, reverse=True)

#assign videos to al caches until full
for c in caches:
    for r in sortedRequests:
        if c.hasSpace(r.vid):
            c.addVideo(r.vid)

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
