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

# TODO: optimise sup, dem?
def dinic_blocking_flow(L, f, s, t):                            # {{{1
  st, sup, dem = [(s,None,False)], {}, {}
  sup[s] = dem[t] = sum( fsu["cap"] for fsu in f[s].values() )
  while st:
    u, w, b = st.pop()
    if not b:
      if u == t:
        dem[u] = min(sup[w], f[w][u]["cap"] - f[w][u]["flo"])
        sup[w] -= dem[u]
      else:
        st.append((u,w,True))
        if w: sup[u] = min(sup[w], f[w][u]["cap"] - f[w][u]["flo"])
        for v in f[u]:
          if L.get(v, -1) > L[u]: st.append((v,u,False))
    else:
      dem[u] = 0
      for v, fuv in f[u].items():
        if L.get(v, -1) > L[u]:
          fuv["flo"] += dem[v]; f[v][u]["flo"] -= dem[v]
          dem[u] += dem[v]; dem[v] = 0
      if w: sup[w] -= dem[u]
                                                                # }}}1

sys.stdin.readline()
ss  = [ int(x)-1 for x in sys.stdin.readline().split() ]
qq  = list(map(int, sys.stdin.readline().split()))
c   = dict(s = {}, t = {}); s, t = "st"

for i, (d, *data) in enumerate( map(int, line.split())
                                for line in sys.stdin ):
  w = "{}_w".format(i); c[w] = { t:d }
  for j, (a, q) in enumerate(zip(data, ss)):
    u = "{}_s{}_q{}".format(i, j, q)
    v = "{}_q{}"    .format(i,    q)
    c[s][u] = a; c[u] = { v: qq[q] }; c[v] = { w: min(qq[q], d) }
    if i > 0:
      v_ = "{}_q{}".format(i-1, q); c[v_][u] = qq[q]

# from pprint import pprint
# pprint(c)

f = dinic(c, s, t)

for fsu in f[s].values():
  if fsu["flo"] != fsu["cap"]:
    print("impossible"); break
else:
  print("possible")
