#!/usr/bin/python3
# encoding: utf-8

# ...

                                                                # {{{1
r"""
Ford-Fulkerson algorithm                                        # {{{2
------------------------

>>> # {{{ {{{ {{{ {{{ fix vim folds
>>> import pprint
>>> c = dict(s = dict(u = 15, v = 5, x = 12),
...          u = dict(x = 8, v = 10),
...          v = dict(z = 8),
...          x = dict(y = 5, t = 5),
...          y = dict(t = 15),
...          z = dict(t = 10),
...          t = dict())
>>> s, t = "st"
>>> # TODO: (deterministic!) examples of after_pass
>>> # def after_pass(path, b, f):
>>> #   print("b =", b, "path =", path); pprint.pprint(f)
>>> f = ford_fulkerson(c, s, t)
>>> max_flow(f, s)
18
>>> cut_a, cut_b = min_cut(f, s)
>>> sorted(cut_a), sorted(cut_b)
(['s', 'u', 'v', 'x'], ['t', 'y', 'z'])

                                                                # }}}2

Dinic's algorithm                                               # {{{2
-----------------

>>> # ... (continues from Ford-Fulkerson example)
>>> # {{{ {{{ {{{ fix vim folds
>>> from pprint import pprint
>>> def after_pass(f, L): pprint(dict(f = f, L = L))
>>> f = dinic(c, s, t, after_pass = after_pass)
{'L': {'s': 0, 't': 3, 'u': 1, 'v': 1, 'x': 1, 'y': 2, 'z': 2},
 'f': {'s': {'u': {'cap': 15, 'flo': 0},
             'v': {'cap': 5, 'flo': 0},
             'x': {'cap': 12, 'flo': 5}},
       't': {'x': {'cap': 0, 'flo': -5},
             'y': {'cap': 0, 'flo': 0},
             'z': {'cap': 0, 'flo': 0}},
       'u': {'s': {'cap': 0, 'flo': 0},
             'v': {'cap': 10, 'flo': 0},
             'x': {'cap': 8, 'flo': 0}},
       'v': {'s': {'cap': 0, 'flo': 0},
             'u': {'cap': 0, 'flo': 0},
             'z': {'cap': 8, 'flo': 0}},
       'x': {'s': {'cap': 0, 'flo': -5},
             't': {'cap': 5, 'flo': 5},
             'u': {'cap': 0, 'flo': 0},
             'y': {'cap': 5, 'flo': 0}},
       'y': {'t': {'cap': 15, 'flo': 0}, 'x': {'cap': 0, 'flo': 0}},
       'z': {'t': {'cap': 10, 'flo': 0}, 'v': {'cap': 0, 'flo': 0}}}}
{'L': {'s': 0, 't': 4, 'u': 1, 'v': 2, 'x': 1, 'z': 3},
 'f': {'s': {'u': {'cap': 15, 'flo': 0},
             'v': {'cap': 5, 'flo': 5},
             'x': {'cap': 12, 'flo': 10}},
       't': {'x': {'cap': 0, 'flo': -5},
             'y': {'cap': 0, 'flo': -5},
             'z': {'cap': 0, 'flo': -5}},
       'u': {'s': {'cap': 0, 'flo': 0},
             'v': {'cap': 10, 'flo': 0},
             'x': {'cap': 8, 'flo': 0}},
       'v': {'s': {'cap': 0, 'flo': -5},
             'u': {'cap': 0, 'flo': 0},
             'z': {'cap': 8, 'flo': 5}},
       'x': {'s': {'cap': 0, 'flo': -10},
             't': {'cap': 5, 'flo': 5},
             'u': {'cap': 0, 'flo': 0},
             'y': {'cap': 5, 'flo': 5}},
       'y': {'t': {'cap': 15, 'flo': 5}, 'x': {'cap': 0, 'flo': -5}},
       'z': {'t': {'cap': 10, 'flo': 5}, 'v': {'cap': 0, 'flo': -5}}}}
{'L': {'s': 0, 'u': 1, 'v': 2, 'x': 1},
 'f': {'s': {'u': {'cap': 15, 'flo': 3},
             'v': {'cap': 5, 'flo': 5},
             'x': {'cap': 12, 'flo': 10}},
       't': {'x': {'cap': 0, 'flo': -5},
             'y': {'cap': 0, 'flo': -5},
             'z': {'cap': 0, 'flo': -8}},
       'u': {'s': {'cap': 0, 'flo': -3},
             'v': {'cap': 10, 'flo': 3},
             'x': {'cap': 8, 'flo': 0}},
       'v': {'s': {'cap': 0, 'flo': -5},
             'u': {'cap': 0, 'flo': -3},
             'z': {'cap': 8, 'flo': 8}},
       'x': {'s': {'cap': 0, 'flo': -10},
             't': {'cap': 5, 'flo': 5},
             'u': {'cap': 0, 'flo': 0},
             'y': {'cap': 5, 'flo': 5}},
       'y': {'t': {'cap': 15, 'flo': 5}, 'x': {'cap': 0, 'flo': -5}},
       'z': {'t': {'cap': 10, 'flo': 8}, 'v': {'cap': 0, 'flo': -8}}}}
>>> max_flow(f, s)
18

>>> s, t = "st"
>>> c = { 's': { '1': 10, '2': 10 },
...       '1': { '2': 2, '3': 4, '4': 8 },
...       '2': { '4': 9 },
...       '3': { 't': 10 },
...       '4': { '3': 6, 't': 10 },
...       't': {} }
>>> f = dinic(c, s, t)
>>> # TODO: (deterministic!) examples of after_pass
>>> max_flow(f, s)
19

>>> f = ford_fulkerson(c, s, t)
>>> max_flow(f, s)
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
# NB: assumes c.keys() == V
def ford_fulkerson(c, s, t, after_pass = None):                 # {{{1
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
    if after_pass: after_pass(path, b, f)
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

def min_cut(f, s):                                              # {{{1
  """Find minimum cut using post-Ford-Fulkerson residual graph."""
  cut_a, q = set([s]), deque([s])
  while q:
    u = q.popleft()
    for v in f[u]:
      if f[u][v]["cap"] - f[u][v]["flo"] > 0 and v not in cut_a:
        cut_a.add(v); q.append(v)
  return cut_a, set(f) - cut_a
                                                                # }}}1

# === Dinic's algorithm ===

def max_flow(f, s):
  return sum( fsu["flo"] for fsu in f[s].values() )

# NB: assumes c.keys() == V
def dinic(c, s, t, after_pass = None):                          # {{{1
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
    if after_pass: after_pass(f, L)
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
