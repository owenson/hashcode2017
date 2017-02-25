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

# output:
# ncache servers
# cservid video1 video2 etc
