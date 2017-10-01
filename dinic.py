#!/usr/bin/python3
# encoding: utf-8

# ...

                                                                # {{{1
r"""
Ford-Fulkerson algorithm                                        # {{{2
------------------------

>>> # {{{ {{{ {{{ {{{ fix vim folds
>>> import pprint
>>> V = "suvxyzt"
>>> c = dict(s = dict(u = 15, v = 5, x = 12),
...          u = dict(x = 8, v = 10),
...          v = dict(z = 8),
...          x = dict(y = 5, t = 5),
...          y = dict(t = 15),
...          z = dict(t = 10),
...          t = dict())
>>> E = dict( (k,sorted(v.keys())) for k,v in c.items() )
>>> G = (V,E); s, t = "st"
>>> def after_pass(path, b, f):
...   print("b =", b, "path =", path); pprint.pprint(f)
>>> f, max_flow, min_cut = ford_fulkerson(G, s, t, c, after_pass = after_pass)
b = 5 path = [('s', 'x', False), ('x', 't', False)]
{'s': {'u': {'capacity': 15, 'flow': 0},
       'v': {'capacity': 5, 'flow': 0},
       'x': {'capacity': 12, 'flow': 5}},
 't': {},
 'u': {'v': {'capacity': 10, 'flow': 0}, 'x': {'capacity': 8, 'flow': 0}},
 'v': {'z': {'capacity': 8, 'flow': 0}},
 'x': {'t': {'capacity': 5, 'flow': 5}, 'y': {'capacity': 5, 'flow': 0}},
 'y': {'t': {'capacity': 15, 'flow': 0}},
 'z': {'t': {'capacity': 10, 'flow': 0}}}
b = 5 path = [('s', 'v', False), ('v', 'z', False), ('z', 't', False)]
{'s': {'u': {'capacity': 15, 'flow': 0},
       'v': {'capacity': 5, 'flow': 5},
       'x': {'capacity': 12, 'flow': 5}},
 't': {},
 'u': {'v': {'capacity': 10, 'flow': 0}, 'x': {'capacity': 8, 'flow': 0}},
 'v': {'z': {'capacity': 8, 'flow': 5}},
 'x': {'t': {'capacity': 5, 'flow': 5}, 'y': {'capacity': 5, 'flow': 0}},
 'y': {'t': {'capacity': 15, 'flow': 0}},
 'z': {'t': {'capacity': 10, 'flow': 5}}}
b = 5 path = [('s', 'x', False), ('x', 'y', False), ('y', 't', False)]
{'s': {'u': {'capacity': 15, 'flow': 0},
       'v': {'capacity': 5, 'flow': 5},
       'x': {'capacity': 12, 'flow': 10}},
 't': {},
 'u': {'v': {'capacity': 10, 'flow': 0}, 'x': {'capacity': 8, 'flow': 0}},
 'v': {'z': {'capacity': 8, 'flow': 5}},
 'x': {'t': {'capacity': 5, 'flow': 5}, 'y': {'capacity': 5, 'flow': 5}},
 'y': {'t': {'capacity': 15, 'flow': 5}},
 'z': {'t': {'capacity': 10, 'flow': 5}}}
b = 3 path = [('s', 'u', False), ('u', 'v', False), ('v', 'z', False), ('z', 't', False)]
{'s': {'u': {'capacity': 15, 'flow': 3},
       'v': {'capacity': 5, 'flow': 5},
       'x': {'capacity': 12, 'flow': 10}},
 't': {},
 'u': {'v': {'capacity': 10, 'flow': 3}, 'x': {'capacity': 8, 'flow': 0}},
 'v': {'z': {'capacity': 8, 'flow': 8}},
 'x': {'t': {'capacity': 5, 'flow': 5}, 'y': {'capacity': 5, 'flow': 5}},
 'y': {'t': {'capacity': 15, 'flow': 5}},
 'z': {'t': {'capacity': 10, 'flow': 8}}}
>>> max_flow
18
>>> cut_a, cut_b = min_cut
>>> sorted(cut_a), sorted(cut_b)
(['s', 'u', 'v', 'x'], ['t', 'y', 'z'])

                                                                # }}}2

Dinic's algorithm                                               # {{{2
-----------------

>>> from pprint import pprint
>>> V = "s1234t"
>>> c = { 's': { '1': 10, '2': 10 },
...       '1': { '2': 2, '3': 4, '4': 8 },
...       '2': { '4': 9 },
...       '3': { 't': 10 },
...       '4': { '3': 6, 't': 10 },
...       't': {} }
>>> E = dict( (k,sorted(v.keys())) for k,v in c.items() )
>>> G = (V,E); s, t = "st"
>>> def after_pass(f, L): pprint(dict(f = f, L = L))
>>> f, max_flow = dinic(G, s, t, c, after_pass = after_pass)
TODO
>>> max_flow
19

                                                                # }}}2
"""
                                                                # }}}1

import argparse, sys
from collections import deque

__version__ = "0.0.1"

def main(*args):                                                # {{{1
  p = _argument_parser(); n = p.parse_args(args)
  import doctest
  failures, tests = doctest.testmod(verbose = n.verbose)
  return 0 if failures == 0 else 1
                                                                # }}}1

# TODO
def _argument_parser():                                         # {{{1
  p = argparse.ArgumentParser(description = "...")
  p.add_argument("--version", action = "version",
                 version = "%(prog)s {}".format(__version__))
  p.add_argument("--verbose", "-v", action = "store_true",
                 help = "run tests verbosely")
  return p
                                                                # }}}1

# === Ford-Fulkerson algorithm ===

# TODO: confirm the algorithm actually works correctly
# TODO: inline
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
  max_flow = sum( f[s][u]["flow"] for u in neighbors(s) )
  return f, max_flow, min_cut(V, f, s, neighbors, rneighbors, cap)
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

def min_cut(V, f, s, neighbors, rneighbors, cap):               # {{{1
  """Find minimum cut using post-Ford-Fulkerson residual graph."""
  cut_a, q = set([s]), deque([s])
  def process(u, v, rev):
    if cap(u, v, rev) > 0 and v not in cut_a:
      cut_a.add(v); q.append(v)
  while q:
    u = q.popleft()
    for v in  neighbors(u): process(u, v, False)
    for v in rneighbors(u): process(u, v, True)
  return cut_a, set(V) - cut_a
                                                                # }}}1

# === Dinic's algorithm ===

def dinic(G, s, t, c, after_pass = None):                       # {{{1
  """Dinic's algorithm."""
  V, E = G; f = {} # residual/level graph w/ "reverse" edges
  for u in V:
    f[u] = {}
    for v in E[u]: f[u][v] = dict(cap = c[u][v], flo = 0)
  for u in V:
    for v in E[u]: f.setdefault(v, {})\
                    .setdefault(u, dict(cap = 0, flo = 0))
  L = dinic_levels(f, s)
  while L.get(t, None) is not None:
    dinic_blocking_flow(L, f, s, t); L = dinic_levels(f, s)
    if after_pass: after_pass(f, L)
  return f, sum( f[s][u]["flo"] for u in f[s].keys() )
                                                                # }}}1

def dinic_levels(f, s):                                         # {{{1
  L, seen, q = { s:0 }, set(), deque([(s,0)])
  while q:
    u, n = q.popleft()
    if u in seen: continue
    seen.add(u); L[u] = n
    for v in f[u].keys():
      if f[u][v]["cap"] - f[u][v]["flo"] > 0: q.append((v,n+1))
  return L
                                                                # }}}1

def dinic_blocking_flow(L, f, s, t):                            # {{{1
  st, sup, dem = [(s,None,False)], {}, {}
  sup[s] = dem[t] = sum( f[s][u]["cap"] for u in f[s].keys() )
  while st:
    u, w, b = st.pop()
    if not b:
      if u == t:
        dem[u] = min(sup[w], f[w][u]["cap"] - f[w][u]["flo"])
        sup[w] -= dem[u]
      else:
        st.append((u,w,True))
        if w: sup[u] = min(sup[w], f[w][u]["cap"] - f[w][u]["flo"])
        for v in f[u].keys():
          if L.get(v, -1) > L[u]: st.append((v,u,False))
    else:
      dem[u] = 0
      for v in f[u].keys():
        if L.get(v, -1) > L[u]:
          f[u][v]["flo"] += dem[v]; f[v][u]["flo"] -= dem[v]
          dem[u] += dem[v]; dem[v] = 0
      if w: sup[w] -= dem[u]
                                                                # }}}1

# === Miscellaneous graph algorithms ===

def transpose(G):
  """Transpose graph."""
  V, E = G; ET = {}
  for u in V: ET[u] = []
  for u, vs in E.items():
    for v in vs: ET[v].append(u)
  return (V, ET)

# === END ===

if __name__ == "__main__":
  sys.exit(main(*sys.argv[1:]))

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
