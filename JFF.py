import sys
from collections import deque

def ford_fulkerson(c, s, t):                                    # {{{1
  """Ford-Fulkerson algorithm."""
  f = {} # residual/level graph w/ "reverse" edges
  for u, cu in c.items():
    fu = f[u] = {}
    for v, cuv in cu.items(): fu[v] = dict(cap = cuv, flo = 0)
  for u, cu in c.items():
    for v in cu: f.setdefault(v, {})\
                  .setdefault(u, dict(cap = 0, flo = 0))
  path = find_augmenting_path(f, s, t)
  while path is not None:
    b = min( f[u][v]["cap"] - f[u][v]["flo"] for u,v in path )
    for u,v in path:
      f[u][v]["flo"] += b; f[v][u]["flo"] -= b
    path = find_augmenting_path(f, s, t)
  return f
                                                                # }}}1

def find_augmenting_path(f, s, t):                              # {{{1
  """Find a (shortest) augmenting path using BFS."""
  seen, q = set([s]), deque([(s,[])])
  if s == t: return []
  while q:
    u, path = q.popleft()
    for v in f[u]:
      if f[u][v]["cap"] - f[u][v]["flo"] > 0 and v not in seen:
        path_ = path + [(u,v)]; seen.add(v); q.append((v,path_))
        if v == t: return path_
  return None
                                                                # }}}1

sys.stdin.readline()
s2q = [ int(x)-1 for x in sys.stdin.readline().split() ]
qsz = list(map(int, sys.stdin.readline().split()))

c   = dict(s = {}, t = {}); s, t = "st"

for i, (d, *data) in enumerate( map(int, line.split())
                                for line in sys.stdin ):
  w = "{}_w".format(i); c[w] = { t:d }
  for j, (a, q) in enumerate(zip(data, s2q)):
    u, v = "{}_q{}".format(i, q), "{}_q{}_".format(i, q)
    c[s].setdefault(u, 0); c[s][u] += a
    c[u] = { v: qsz[q] }; c[v] = { w: min(qsz[q], d) }
    if i > 0:
      v_ = "{}_q{}_".format(i-1, q); c[v_][u] = qsz[q]

# from pprint import pprint; pprint(c)

f = ford_fulkerson(c, s, t)

for fsu in f[s].values():
  if fsu["flo"] != fsu["cap"]:
    print("impossible"); break
else:
  print("possible")
