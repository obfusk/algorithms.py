#!/usr/bin/python

# --                                                            ; {{{1
#
# File        : algorithms.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2016-10-12
#
# Copyright   : Copyright (C) 2016  Felix C. Stegerman
# Version     : v0.0.1
# License     : GPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""
Python (2+3) implementations of standard algorithms

Examples
========

A* Search                                                       # {{{2
---------

>>> A, B      = "L", "F"
>>> h         = lambda node: EX_STRAIGT_LINES_TO_F[node]
>>> siblings  = lambda node: sorted(EX_DISTANCES[node].items())
>>> a_star(A, B, h, siblings, verbose = True)
L 152
  -> M 231
  -> T 295
M 231
  -> D 347
  -> L 292
L 292
  -> M 371
  -> T 435
T 295
  -> A 435
  -> L 374
D 347
  -> C 456
  -> M 381
M 371
  -> D 487
  -> L 432
L 374
  -> M 453
  -> T 517
M 381
  -> D 497
  -> L 442
L 432
  -> M 511
  -> T 575
A 435
  -> S 456
  -> T 531
  -> Z 491
T 435
  -> A 575
  -> L 514
L 442
  -> M 521
  -> T 585
M 453
  -> D 569
  -> L 514
C 456
  -> D 587
  -> P 483
  -> R 489
S 456
  -> A 715
  -> F 468
  -> O 711
  -> R 527
('F', 468)

                                                                # }}}2

...


Links
=====

https://en.wikipedia.org/wiki/A*_search_algorithm
...
"""
                                                                # }}}1

from __future__ import print_function

import argparse, heapq, sys

if sys.version_info.major == 2:                                 # {{{1
  pass
else:
  xrange  = range
                                                                # }}}1

__version__       = "0.0.1"


def main(*args):                                                # {{{1
  p = argument_parser(); n = p.parse_args(args)
  import doctest
  doctest.testmod(verbose = n.verbose)
  return 0
                                                                # }}}1

def argument_parser():                                          # {{{1
  p = argparse.ArgumentParser(description = "cryptanalysis")
  p.add_argument("--version", action = "version",
                 version = "%(prog)s {}".format(__version__))
  p.add_argument("--verbose", "-v", action = "store_true",
                 help = "run tests verbosely")
  return p
                                                                # }}}1

# === A* Search ===

def a_star(A, B, h, siblings, verbose = False):                 # {{{1
  """A* search."""
  frontier = []; heapq.heappush(frontier, (0+h(A),0,A))
  while frontier:
    f_of_node, cost, node = heapq.heappop(frontier)
    if node == B: return (node, cost)
    if verbose: print(node, f_of_node)
    for sibling, cost_from_node in siblings(node):
      s_cost = cost + cost_from_node; f_of_s = s_cost + h(sibling)
      if verbose: print("  ->", sibling, f_of_s)
      heapq.heappush(frontier, (f_of_s,s_cost,sibling))
  return None
                                                                # }}}1

EX_STRAIGT_LINES_TO_F = dict(
  A = 206, B = 176, C = 191, D = 202, E = 306, F = 0, G = 204,
  H = 287, I = 171, L = 152, M = 161, N = 150, O = 191, P = 80,
  R = 78, S = 87, T = 184, U = 182, V = 170, Z = 187
)

EX_DISTANCES = dict(                                            # {{{1
  O = dict(Z = 71, S = 151),
  Z = dict(O = 71, A = 75),
  S = dict(O = 151, A = 140, F = 99, R = 80),
  A = dict(Z = 75, S = 140, T = 118),
  F = dict(S = 99, B = 211),
  R = dict(S = 80, P = 97, C = 146),
  T = dict(A = 118, L = 111),
  B = dict(F = 211, P = 101, U = 85, G = 90),
  P = dict(R = 97, B = 101, C = 138),
  C = dict(R = 146, P = 138, D = 120),
  L = dict(T = 111, M = 70),
  M = dict(L = 70, D = 75),
  U = dict(B = 85, H = 98, V = 142),
  G = dict(B = 90),
  D = dict(C = 120, M = 75),
  H = dict(U = 98, E = 86),
  V = dict(U = 142, I = 92),
  E = dict(H = 86),
  I = dict(V = 92, N = 87),
  N = dict(I = 87),
)                                                               # }}}1

# === END ===

if __name__ == "__main__":
  sys.exit(main(*sys.argv[1:]))

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
