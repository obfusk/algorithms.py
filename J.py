import sys
from collections import deque

def dinic(c, s, t):                                             # {{{1
  """Dinic's algorithm."""
  f = {} # residual/level graph w/ "reverse" edges
  for u, cu in c.items():
    fu = f[u] = {}
    for v, cuv in cu.items(): fu[v] = dict(cap = cuv, flo = 0)
  for u, cu in c.items():
    for v in cu: f.setdefault(v, {})\
                  .setdefault(u, dict(cap = 0, flo = 0))
  L = dinic_levels(f, s, t)
  while L.get(t, None) is not None:
    dinic_blocking_flow(L, f, s, t); L = dinic_levels(f, s, t)
  return f
                                                                # }}}1

def dinic_levels(f, s, t):                                      # {{{1
  L, q = { s:0 }, deque([(s,0)])
  while q:
    u, n = q.popleft()
    for v, fuv in f[u].items():
      if fuv["cap"] - fuv["flo"] > 0 and not v in L:
        L[v] = n+1; q.append((v,n+1))
        if v == t: return L
  return L
                                                                # }}}1

def dinic_blocking_flow(L, f, s, t):                            # {{{1
  seen = set()
  def dfs(u, flo):
    if u == s: return flo
    rem = flo
    for v in f[u]:
      c = f[v][u]["cap"] - f[v][u]["flo"]; m = min(rem, c)
      if c > 0 and v not in seen and L.get(v, -2) == L[u]-1:
        flo_ = dfs(v, m)
        if flo_ < m: seen.add(v)
        f[v][u]["flo"] += flo_; f[u][v]["flo"] -= flo_; rem -= flo_
        if rem == 0: return flo
    return flo - rem
  dfs(t, sum( fsu["cap"] for fsu in f[s].values() ))
                                                                # }}}1

sys.stdin.readline()
s2q = [ int(x)-1 for x in sys.stdin.readline().split() ]
qsz = list(map(int, sys.stdin.readline().split()))

c   = dict(s = {}, t = {}); s, t = "st"

for i, (d, *data) in enumerate( map(int, line.split())
                                for line in sys.stdin ):
  w = "{}_w".format(i); c[w] = { t:d }
  for a, q in zip(data, s2q):
    u, v = "{}_q{}".format(i, q), "{}_q{}_".format(i, q)
    c[s].setdefault(u, 0); c[s][u] += a
    c[u] = { v: qsz[q] }; c[v] = { w: min(qsz[q], d) }
    if i > 0:
      v_ = "{}_q{}_".format(i-1, q); c[v_][u] = qsz[q]

f = dinic(c, s, t)

for fsu in f[s].values():
  if fsu["flo"] != fsu["cap"]:
    print("impossible"); break
else:
  print("possible")
