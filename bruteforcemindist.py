#!/usr/bin/env python2

"""Brute force calculation of the minimum distance to assume being attacked using only the number of peers and the HTL.

This currently ignores that in a real network there will only be a fixed number of locations equal to the size of the network.
"""

import random
import numpy as np
import pylab as pl
import math

def dist(loc1, loc2):
    dist1 = abs(loc1 - loc2)
    dist2 = (loc1 + loc2)%1
    return min(dist1, dist2)

def random_dist(npeers, target, nodes=None):
    if nodes is None:
        return min([dist(random.random(), target) for i in range(npeers)])
    else:
        
        return min([dist(i, target) for i in np.random.choice(nodes, (npeers,))])

def oneroute(npeers, target, HTL=10, nodes=None):
    best = random_dist(npeers, target)
    maybebetter = random_dist(npeers, target, nodes=nodes)
    for i in range(HTL-1):
        if maybebetter > best:
           break
        best = maybebetter
        maybebetter = random_dist(npeers, target)
    return best

def trial(npeers, ntries, nodes=None):
  target = random.random()
  best = oneroute(npeers, target)
  maybebetter = oneroute(npeers, target, nodes=nodes)
  for i in range(ntries):
    maybebetter = oneroute(npeers, target, nodes=nodes)
    if maybebetter < best:
      best = maybebetter
  return best

npeers = 6
size = 1000
nodes = None # pl.random_sample(size)
samples_per_try = 5000
maxtries = 4
tries = []
best_by_tries = []
twostd_per_tries = {}
for ntries in range(int(math.log(maxtries, 2))):
    t = []
    for i in range(samples_per_try):
        tries.append(2**ntries)
        t.append(trial(npeers, int(2**ntries), nodes=nodes))
    best_by_tries.extend(t)
    twostd_per_tries[2**ntries] = t
pl.plot(tries, best_by_tries, "+")
print sorted(zip(twostd_per_tries.keys(), [2 * pl.std(t) for t in twostd_per_tries.values()], [pl.median(t) + 2 * pl.std(t) for t in twostd_per_tries.values()], [pl.mean(t) + 2 * pl.std(t) for t in twostd_per_tries.values()]))
pl.plot(twostd_per_tries.keys(), [2 * pl.std(t) for t in twostd_per_tries.values()], "o", label="2s")
pl.plot(twostd_per_tries.keys(), [sorted(t)[int(0.95*len(t))] for t in twostd_per_tries.values()], "d", label="95%")
pl.plot(twostd_per_tries.keys(), [pl.median(t) for t in twostd_per_tries.values()], "h", label="median")
pl.plot(twostd_per_tries.keys(), [pl.mean(t) for t in twostd_per_tries.values()], "H", label="mean")
pl.xscale('log')
pl.legend()
pl.grid()
pl.show()
