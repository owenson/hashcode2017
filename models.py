import sys
import operator

videoSizes = []
endpoints = []
requests = []
cacheServer = []
caches = []

####begin models#####
class Cache:
    def __init__(self, id, capacity):
        self.capacity = capacity
        self.maxCapacity = capacity
        self.id = id
        self.videos = []
        self.requestsSavings = [] #tuple (r, saving)

    def clear(self):
        self.videos = []
        self.requestSavings = []
        self.capacity = self.maxCapacity

    def finalise(self):
        self.requestsSavings = sorted(self.requestsSavings, key=operator.itemgetter(1), reverse=True)

    def addRequestSavings(self, request, saving):
        self.requestsSavings.append((request,saving))

    def addVideo(self, vid):
        global videoSizes
        if self.capacity < videoSizes[vid]:
            print "ERROR CACHE RUN OUT OF CAPACITY"
            sys.exit(1)
        self.capacity -= videoSizes[vid]
        self.videos.append(vid)

    def hasSpace(self, vid):
        global videoSizes
        if self.capacity >= videoSizes[vid]:
            return True
        return False

    def hasVideo(self,vid):
        return vid in self.videos

class Endpoint:
    def __init__(self, id):
        self.id = id
        self.dataCenterLatency = 0
        self.endpointLatencyToCacheServer = {}   #key is cache id
        self.cachesByLatency = []
        self.requests = []

    def finalise(self):
        self.cachesByLatency = sorted(self.endpointLatencyToCacheServer.items(), key=operator.itemgetter(1))

    def addCacheServer(self, cache, latency):
        self.endpointLatencyToCacheServer[cache] = latency

    def addVideoToNearestCache(self, vid):
        for (cache, latency) in self.cachesByLatency:
            if cache.hasSpace(vid) and not cache.hasVideo(vid):
                cache.addVideo(vid)
                return True
        return False

    def addRequests(self,r):
        self.requests.append(r)

class Request:
    def __init__(self, vid, epid, nreq):
        self.vid = vid
        self.epid = epid
        self.nreq = nreq
        self.serviced = False

#begin parsing
f = open(sys.argv[1], "r")
(nVideos, nEndpoints, nRequests, nCaches, cacheCapacity) = map(int,f.readline().split(" "))
videoSizes = map(int, f.readline().split(" "))

#initialise cache servers with same capacity
for i in range(nCaches):
    c = Cache(i, cacheCapacity)
    caches.append(c)

#read endpoints from file
for i in range(nEndpoints):
    ep = Endpoint(i)
    (dcLatency, nCachesToThis) = map(int,f.readline().split(" "))
    ep.dataCenterLatency = dcLatency
    for k in range(nCachesToThis):
        (cid, clat) = map(int, f.readline().split(" "))
        ep.addCacheServer(caches[cid], clat)
    endpoints.append(ep)

for i in range(nRequests):
    (vid, epid, nreq) = map(int,f.readline().split(" "))
    r = Request(vid, epid, nreq)
    requests.append(r)

#sorting of some internal data in models
for e in endpoints:
    e.finalise()

for c in caches:
    c.finalise()
##### END PARSING
