import sys
from collections import deque

def ford_fulkerson(G, s, t, c, after_pass = None):              # {{{1
  """Ford-Fulkerson algorithm."""
  if isinstance(c, dict): c_, c = c, lambda u, v: c_[u][v]
  V, E  = G; ET = transpose(G)[1]; f = {}
  neighbors, rneighbors = lambda u: E[u], lambda u: ET[u]
  for u in V:   # build residual graph with combined forward & reverse
    f[u] = {}   # edges; thus we need neighbors, rneighbors & cap
    for v in E[u]: f[u][v] = dict(capacity = c(u,v), flow = 0)
  cap   = lambda u, v, rev: f[u][v]["capacity"] - f[u][v]["flow"] \
                            if not rev else f[v][u]["flow"]
  path  = find_augmenting_path(s, t, neighbors, rneighbors, cap)
  while path != None:
    b = min( cap(*x) for x in path )
    for u,v,rev in path: (f[v][u] if rev else f[u][v])["flow"] += b
    if after_pass: after_pass(path, b, f)
    path = find_augmenting_path(s, t, neighbors, rneighbors, cap)
  return f
                                                                # }}}1

def find_augmenting_path(s, t, neighbors, rneighbors, cap):     # {{{1
  """Find a (shortest) augmenting path using BFS."""
  seen, q = set([s]), deque([(s,[])])
  def process(u, v, rev):
    if cap(u, v, rev) > 0 and v not in seen:
      path_ = path + [(u,v,rev)]; seen.add(v); q.append((v,path_))
      return path_ if v == t else None
  if s == t: return []
  while q:
    u, path = q.popleft()
    for v in neighbors(u):
      path_ = process(u, v, False)
      if path_ != None: return path_
    for v in rneighbors(u):
      path_ = process(u, v, True)
      if path_ != None: return path_
  return None
                                                                # }}}1

def transpose(G):
  """Transpose graph."""
  V, E = G; ET = {}
  for u in V: ET[u] = []
  for u, vs in E.items():
    for v in vs: ET[v].append(u)
  return (V, ET)

sys.stdin.readline()
s2q = [ int(x)-1 for x in sys.stdin.readline().split() ]
qsz = list(map(int, sys.stdin.readline().split()))

c   = dict(s = {}, t = {}); s, t = "st"
V   = list("st")

for i, (d, *data) in enumerate( map(int, line.split())
                                for line in sys.stdin ):
  w = "{}_w".format(i); c[w] = { t:d }
  V += [w]
  for j, (a, q) in enumerate(zip(data, s2q)):
    u, v = "{}_q{}".format(i, q), "{}_q{}_".format(i, q)
    c[s].setdefault(u, 0); c[s][u] += a
    c[u] = { v: qsz[q] }; c[v] = { w: min(qsz[q], d) }
    if i > 0:
      v_ = "{}_q{}_".format(i-1, q); c[v_][u] = qsz[q]
    V += [u, v]

# from pprint import pprint; pprint(c)

E = dict( (k,sorted(v)) for k,v in c.items() )
G = (V,E)
f = ford_fulkerson(G, s, t, c)

for fsu in f[s].values():
  if fsu["flow"] != fsu["capacity"]:
    print("impossible"); break
else:
  print("possible")
