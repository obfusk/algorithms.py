#!/usr/bin/python
# encoding: utf-8

# --                                                            ; {{{1
#
# File        : algorithms.py
# Maintainer  : Felix C. Stegerman <flx@obfusk.net>
# Date        : 2016-10-20
#
# Copyright   : Copyright (C) 2016  Felix C. Stegerman
# Version     : v0.0.3
# License     : GPLv3+
#
# --                                                            ; }}}1

                                                                # {{{1
r"""
Python (2+3) implementations of standard algorithms

Examples
========

Depth-first search (DFS)                                        # {{{2
------------------------

>>> V = "ABCDEFGH"
>>> E = dict(A = "BF", B = "CE", C = "D", D = "BH", E = "DG", \
...          F = "EG", G = "F" , H = "G")
>>> G = (V,E); classify = {}
>>> def at_edge(u, v, colour):
...   classify[(u,v)] = dict(W = "tree", G = "back", B = "")[colour]
>>> p, ts, d, f = dfs(G, at_edge = at_edge)
>>> for k, v in sorted(p.items()): print(k, v)
A None
B A
C B
D C
E F
F G
G H
H D
>>> ts
[['A', 'B', 'C', 'D', 'H', 'G', 'F', 'E']]
>>> for e, c in sorted(classify.items()):
...   u, v = e
...   print(u, "->", v, c if c != "" else ("forward" if d[u] < d[v]
...                                                  else "cross"))
A -> B tree
A -> F forward
B -> C tree
B -> E forward
C -> D tree
D -> B back
D -> H tree
E -> D back
E -> G back
F -> E tree
F -> G back
G -> F tree
H -> G tree

                                                                # }}}2

Topological sort and longest path                               # {{{2
---------------------------------

>>> V = "ABCDEFG"
>>> E = dict(A = "BCE", B = "C", C = "D", D = "", E = "", \
...          F = "G"  , G = "")
>>> G = (V,E)
>>> topological_sort(G)
deque(['F', 'G', 'A', 'E', 'B', 'C', 'D'])
>>> longest_path(G)
3

>>> V = "ABCDEFG"
>>> E = dict(A = "BCE", B = "C", C = "D", D = "", E = "", \
...          F = "G"  , G = "")
>>> G = (V,E)
>>> topological_sort2(G)
['F', 'G', 'A', 'E', 'B', 'C', 'D']

                                                                # }}}2

Strongly connected components                                   # {{{2
-----------------------------

>>> V = "ABCDEFGH"
>>> E = dict(A = "B", B = "CEF", C = "DG", D = "CH", E = "AF",
...          F = "G", G = "FH" , H = "H")
>>> G = (V,E)
>>> SCC_V, SCC_E = strongly_connected_components(G)
>>> SCC_V
['ABE', 'CD', 'FG', 'H']
>>> for k, v in sorted(SCC_E.items()): print("%-3s" % k, sorted(v))
ABE ['CD', 'FG']
CD  ['FG', 'H']
FG  ['H']
H   []

                                                                # }}}2

Dijkstra's algorithm                                            # {{{2
--------------------

>>> V = "ABCDEFGH"
>>> w = dict(A = dict(B =  5, E =  4),
...          B = dict(A =  5, C =  6, E =  3, F = 14, G = 10),
...          C = dict(B =  6, D =  1, G =  9, H = 17),
...          D = dict(C =  1, H = 12),
...          E = dict(A =  4, B =  3, F = 11),
...          F = dict(B = 14, E = 11, G =  7),
...          G = dict(B = 10, F =  7, H = 15),
...          H = dict(C = 17, D = 12, G = 15))
>>> E = dict( (k,v.keys()) for k,v in w.items() )
>>> G = (V,E); s = 'A'
>>> def at_dequeue(u, q, d):
...   print(u, q, sorted(d.items(), key = lambda x: x[0]))
>>> d, p = dijkstra(G, s, w, at_dequeue = at_dequeue)
A [] [('A', 0), ('B', None), ('C', None), ('D', None), ('E', None), ('F', None), ('G', None), ('H', None)]
E [(5, 'B')] [('A', 0), ('B', 5), ('C', None), ('D', None), ('E', 4), ('F', None), ('G', None), ('H', None)]
B [(15, 'F')] [('A', 0), ('B', 5), ('C', None), ('D', None), ('E', 4), ('F', 15), ('G', None), ('H', None)]
C [(15, 'F'), (15, 'G')] [('A', 0), ('B', 5), ('C', 11), ('D', None), ('E', 4), ('F', 15), ('G', 15), ('H', None)]
D [(15, 'F'), (15, 'G'), (28, 'H')] [('A', 0), ('B', 5), ('C', 11), ('D', 12), ('E', 4), ('F', 15), ('G', 15), ('H', 28)]
F [(15, 'G'), (24, 'H'), (28, 'H')] [('A', 0), ('B', 5), ('C', 11), ('D', 12), ('E', 4), ('F', 15), ('G', 15), ('H', 24)]
G [(24, 'H'), (28, 'H')] [('A', 0), ('B', 5), ('C', 11), ('D', 12), ('E', 4), ('F', 15), ('G', 15), ('H', 24)]
H [(28, 'H')] [('A', 0), ('B', 5), ('C', 11), ('D', 12), ('E', 4), ('F', 15), ('G', 15), ('H', 24)]
>>> sorted(d.items())
[('A', 0), ('B', 5), ('C', 11), ('D', 12), ('E', 4), ('F', 15), ('G', 15), ('H', 24)]
>>> sorted(p.items())
[('A', None), ('B', 'A'), ('C', 'B'), ('D', 'C'), ('E', 'A'), ('F', 'E'), ('G', 'B'), ('H', 'D')]

                                                                # }}}2

Bellman-Ford algorithm                                          # {{{2
----------------------

>>> V = "txyzs"
>>> w = dict(s = dict(t = 6, y = 7),
...          t = dict(x = 5, y = 8, z = -4),
...          x = dict(t = -2),
...          y = dict(x = -3, z = 9),
...          z = dict(s = 2, x = 7))
>>> E = dict( (k,sorted(v.keys(), key = lambda x: V.index(x)))
...           for k,v in w.items() )
>>> G = (V,E); s = 'z'
>>> def after_pass(d, p):
...   print("d =", sorted(d.items()))
...   print("p =", sorted(p.items()))
>>> d, p = bellman_ford(G, s, w, after_pass = after_pass)
d = [('s', 2), ('t', 8), ('x', 7), ('y', 9), ('z', 0)]
p = [('s', 'z'), ('t', 's'), ('x', 'z'), ('y', 's'), ('z', None)]
d = [('s', 2), ('t', 5), ('x', 6), ('y', 9), ('z', 0)]
p = [('s', 'z'), ('t', 'x'), ('x', 'y'), ('y', 's'), ('z', None)]
d = [('s', 2), ('t', 4), ('x', 6), ('y', 9), ('z', 0)]
p = [('s', 'z'), ('t', 'x'), ('x', 'y'), ('y', 's'), ('z', None)]
d = [('s', 2), ('t', 4), ('x', 6), ('y', 9), ('z', 0)]
p = [('s', 'z'), ('t', 'x'), ('x', 'y'), ('y', 's'), ('z', None)]

                                                                # }}}2

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

Universal sink (celebrity problem)                              # {{{2
----------------------------------

>>> V = "ABC"
>>> E = [[0,1,1],[0,0,0],[0,1,0]]
>>> G = (V,E)
>>> V[universal_sink(G)]
'B'
>>> V = "ABCD"
>>> E = [[0,1,1,0],[0,0,0,1],[0,1,0,0],[0,0,1,0]]
>>> G = (V,E)
>>> universal_sink(G) is None
True

                                                                # }}}2

Miscellaneous graph algorithms                                  # {{{2
------------------------------

...
                                                                # }}}2

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

MiniMax w/ Alpha-Beta Pruning                                   # {{{2
-----------------------------

>>> import pprint
>>> L4 = [0.5,1,0.5,0,0,0.5,1,0,0.5,0,0.5,0,1,1,0.5,1,0,0,1,0.5,1,0,0.5,0.5]
>>> L3 = [dict(value = None, children = L4[:3]),
...       1,
...       dict(value = None, children = L4[3:6]),
...       dict(value = None, children = L4[6:9]),
...       0,
...       dict(value = None, children = L4[9:12]),
...       dict(value = None, children = L4[12:15]),
...       dict(value = None, children = L4[15:18]),
...       0.5,
...       dict(value = None, children = L4[18:21]),
...       0.5,
...       dict(value = None, children = L4[21:])]
>>> L2 = [dict(value = None, children = L3[:4]),
...       0,
...       dict(value = None, children = L3[4:5]),
...       dict(value = None, children = L3[5:8]),
...       dict(value = None, children = L3[8:9]),
...       dict(value = None, children = L3[9:])]
>>> L1 = [dict(value = None, children = L2[:3]),
...       dict(value = None, children = L2[3:])]
>>> T   = dict(value = None, children = L1)
>>> minimax_alphabeta(T, 0, 1, start_max = False, verbose = True)
minimax(0, 1)
  minimax(0, 1)
    minimax(0, 1)
      minimax(0, 1)
        minimax(0, 1)
        | leaf (value = 0.5)
      | alpha = 0.5 beta = 1
        minimax(0.5, 1)
        | leaf (value = 1)
      | alpha = 1 beta = 1
      | pruning; value = 1
    | alpha = 0 beta = 1
      minimax(0, 1)
      | leaf (value = 1)
    | alpha = 0 beta = 1
      minimax(0, 1)
        minimax(0, 1)
        | leaf (value = 0)
      | alpha = 0 beta = 1
        minimax(0, 1)
        | leaf (value = 0)
      | alpha = 0 beta = 1
        minimax(0, 1)
        | leaf (value = 0.5)
      | alpha = 0.5 beta = 1
      | value = 0.5
    | alpha = 0 beta = 0.5
      minimax(0, 0.5)
        minimax(0, 0.5)
        | leaf (value = 1)
      | alpha = 1 beta = 0.5
      | pruning; value = 0.5
    | alpha = 0 beta = 0.5
    | value = 0.5
  | alpha = 0.5 beta = 1
    minimax(0.5, 1)
    | leaf (value = 0)
  | alpha = 0.5 beta = 1
    minimax(0.5, 1)
      minimax(0.5, 1)
      | leaf (value = 0)
    | alpha = 0.5 beta = 0
    | pruning; value = 0.5
  | alpha = 0.5 beta = 1
  | value = 0.5
| alpha = 0 beta = 0.5
  minimax(0, 0.5)
    minimax(0, 0.5)
      minimax(0, 0.5)
        minimax(0, 0.5)
        | leaf (value = 0)
      | alpha = 0 beta = 0.5
        minimax(0, 0.5)
        | leaf (value = 0.5)
      | alpha = 0.5 beta = 0.5
      | pruning; value = 0.5
    | alpha = 0 beta = 0.5
      minimax(0, 0.5)
        minimax(0, 0.5)
        | leaf (value = 1)
      | alpha = 1 beta = 0.5
      | pruning; value = 0.5
    | alpha = 0 beta = 0.5
      minimax(0, 0.5)
        minimax(0, 0.5)
        | leaf (value = 1)
      | alpha = 1 beta = 0.5
      | pruning; value = 0.5
    | alpha = 0 beta = 0.5
    | value = 0.5
  | alpha = 0.5 beta = 0.5
  | pruning; value = 0.5
| alpha = 0 beta = 0.5
| value = 0.5
0.5
>>> pprint.pprint(T)
{'children': [{'children': [{'children': [{'children': [0.5, 1, 0.5],
                                           'value': 1},
                                          1,
                                          {'children': [0, 0, 0.5],
                                           'value': 0.5},
                                          {'children': [1, 0, 0.5],
                                           'value': 0.5}],
                             'value': 0.5},
                            0,
                            {'children': [0], 'value': 0.5}],
               'value': 0.5},
              {'children': [{'children': [{'children': [0, 0.5, 0],
                                           'value': 0.5},
                                          {'children': [1, 1, 0.5],
                                           'value': 0.5},
                                          {'children': [1, 0, 0],
                                           'value': 0.5}],
                             'value': 0.5},
                            {'children': [0.5], 'value': None},
                            {'children': [{'children': [1, 0.5, 1],
                                           'value': None},
                                          0.5,
                                          {'children': [0, 0.5, 0.5],
                                           'value': None}],
                             'value': None}],
               'value': 0.5}],
 'value': 0.5}

                                                                # }}}2

d-ary heap                                                      # {{{2
----------

>>> A = [24,21,23,22,36,29,30,34,28,27]
>>> heapsort(2, A)
>>> A
[21, 22, 23, 24, 27, 28, 29, 30, 34, 36]

>>> A = [24,21,23,22,36,29,30,34,28,27]
>>> heapsort(3, A)
>>> A
[21, 22, 23, 24, 27, 28, 29, 30, 34, 36]

>>> import random
>>> ok = 0
>>> for d in xrange(2, 100):
...   A = random.sample(xrange(1000), 200)
...   B = sorted(A)
...   heapsort(d, A)
...   if A == B: ok += 1
>>> ok
98

>>> d, A = 3, [24,21,23,22,36,29,30,34,28,27]
>>> build_maxheap(d, A)
>>> A
[36, 30, 34, 22, 21, 29, 24, 23, 28, 27]
>>> heap_extract_max(d, A)
36
>>> A
[34, 30, 28, 22, 21, 29, 24, 23, 27]
>>> heap_extract_max(d, A)
34
>>> A
[30, 29, 28, 22, 21, 27, 24, 23]
>>> heap_insert(d, A, 42)
>>> A
[42, 29, 30, 22, 21, 27, 24, 23, 28]
>>> heap_insert(d, A, 7)
>>> A
[42, 29, 30, 22, 21, 27, 24, 23, 28, 7]
>>> heap_increase_key(d, A, 4, 99)
>>> A
[99, 42, 30, 22, 29, 27, 24, 23, 28, 7]

                                                                # }}}2

Extended Euclidean algorithm                                    # {{{2
----------------------------

>>> a, b                = 240, 46
>>> gcd, bezout, quots  = egcd(a, b, verbose = True)
q=           r=       240 s=         1 t=         0
q=           r=        46 s=         0 t=         1
q=         5 r=        10 s=         1 t=        -5
q=         4 r=         6 s=        -4 t=        21
q=         1 r=         4 s=         5 t=       -26
q=         1 r=         2 s=        -9 t=        47
q=         2 r=         0 s=        23 t=      -120
>>> gcd
2
>>> bezout
(-9, 47)
>>> quots
(-120, 23)
>>> gcd == a*bezout[0] + b*bezout[1]
True
>>> a == gcd*abs(quots[0])
True
>>> b == gcd*abs(quots[1])
True

                                                                # }}}2

Lazy List                                                       # {{{2
---------

>>> list(llist(xrange(0, 10, 2)))
[0, 2, 4, 6, 8]
>>> list(llist( n*n for n in itertools.count(0) )[:10])
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> list(llist([0], rec = lambda xs: ( x+1 for x in xs ))[:10])
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> list(fibs[:10])
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
>>> list(fibs[:10:2])
[0, 1, 3, 8, 21]

                                                                # }}}2

Prime Numbers (Sieve of Eratosthenes)                           # {{{2
-------------------------------------

>>> list(itertools.islice(mprimes(), 20))
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
>>> list(lprimes[:20])
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]

>>> list(primes_up_to(100))
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

>>> list(prime_factors(1))
[]
>>> list(prime_factors(11))
[11]
>>> list(prime_factors(100))
[2, 2, 5, 5]
>>> list(prime_factors(982139867123097))
[3, 162629, 2013047831]

>>> divisors(1)
[1]
>>> divisors(60)
[1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60]
>>> divisors(100)
[1, 2, 4, 5, 10, 20, 25, 50, 100]
>>> divisors(2013047831)
[1, 2013047831]


>>> import math
>>> def naive_divisors(n):
...   def f():
...     for d in xrange(1, int(math.sqrt(n))+2):
...       if n % d == 0:
...         yield d; yield n // d
...   return sorted(set(f()))

>>> import random
>>> ok = 0
>>> for n in xrange(10000):
...   if divisors(n) == naive_divisors(n): ok += 1
>>> ok
10000

On my machine, fastest to slowest is:
  python 2.7  : naive, memoised, llist, non-memoised erastothenes
  python 3.5  : memoised, naive, llist, non-memoised erastothenes
  pypy        : memoised, llist, naive, non-memoised erastothenes
And pypy is significantly faster (~10x for naive, memoised and llist).

>>> import timeit
>>> ndivs = naive_divisors
>>> edivs = lambda x: divisors(x, lambda n: prime_factors(n, erastothenes()))
>>> mdivs = lambda x: divisors(x, lambda n: prime_factors(n, mprimes()))
>>> ldivs = lambda x: divisors(x, lambda n: prime_factors(n, lprimes))
>>> n = timeit.timeit(lambda: ndivs(2013047831), number = 100)
>>> e = timeit.timeit(lambda: edivs(2013047831), number = 100)
>>> m = timeit.timeit(lambda: mdivs(2013047831), number = 100)
>>> l = timeit.timeit(lambda: ldivs(2013047831), number = 100)
>>> n < m < l < e or m < n < l < e or m < l < n < e
True

Everything seems to be thread-safe:

>>> import time
>>> sieve   = _make_prime_sieve() # new data!
>>> a, b, c = [], [], []
>>> def f(x):
...   for p in primes_up_to(100000, sieve()):
...     x.append(p); time.sleep(0.0001)
>>> t1 = threading.Thread(target = f, args = (a,))
>>> t2 = threading.Thread(target = f, args = (b,))
>>> t3 = threading.Thread(target = f, args = (c,))
>>> t1.start(); t2.start(); t3.start()
>>> t1.join() ; t2.join() ; t3.join()
>>> len(a)
9592
>>> a == list(primes_up_to(100000)) and a == b and b == c
True

>>> primes  = llist(erastothenes()) # new data!
>>> a, b, c = [], [], []
>>> def f(x):
...   for p in primes_up_to(100000, primes):
...     x.append(p); time.sleep(0.0001)
>>> t1 = threading.Thread(target = f, args = (a,))
>>> t2 = threading.Thread(target = f, args = (b,))
>>> t3 = threading.Thread(target = f, args = (c,))
>>> t1.start(); t2.start(); t3.start()
>>> t1.join() ; t2.join() ; t3.join()
>>> len(a)
9592
>>> a == list(primes_up_to(100000)) and a == b and b == c
True

                                                                # }}}2


Links
=====

https://en.wikipedia.org/wiki/A*_search_algorithm
https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm
https://en.wikipedia.org/wiki/D-ary_heap
https://en.wikipedia.org/wiki/Depth-first_search
https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm
https://en.wikipedia.org/wiki/Heapsort
https://en.wikipedia.org/wiki/Minimax
https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
https://en.wikipedia.org/wiki/Strongly_connected_component
https://en.wikipedia.org/wiki/Topological_sorting
"""
                                                                # }}}1

from __future__ import print_function

import argparse, functools, itertools, heapq, operator, sys, threading
from collections import deque

if sys.version_info.major == 2:                                 # {{{1
  izip    = itertools.izip
else:
  izip    = zip
  xrange  = range
  reduce  = functools.reduce
                                                                # }}}1

__version__       = "0.0.3"


def main(*args):                                                # {{{1
  p = _argument_parser(); n = p.parse_args(args)
  import doctest
  failures, tests = doctest.testmod(verbose = n.verbose)
  return 0 if failures == 0 else 1
                                                                # }}}1

def _argument_parser():                                         # {{{1
  p = argparse.ArgumentParser(description = "cryptanalysis")
  p.add_argument("--version", action = "version",
                 version = "%(prog)s {}".format(__version__))
  p.add_argument("--verbose", "-v", action = "store_true",
                 help = "run tests verbosely")
  return p
                                                                # }}}1

# === Depth-first search (DFS) ===

def dfs(G, neighbors  = None, at_discover = None,               # {{{1
           at_edge    = None, at_finish   = None):
  """Perform DFS on a graph."""
  V, E = G; colour, p, d, f = {}, {}, {}, {}; ts = []
  _ = type("",(),{})(); _.time = 0
  if neighbors is None: neighbors = lambda u: E[u]
  def visit(u, t):
    t.append(u)
    if at_discover: at_discover(u)
    colour[u] = 'G'; _.time += 1; d[u] = _.time
    for v in neighbors(u):
      if at_edge: at_edge(u, v, colour[v])
      if colour[v] == 'W':
        p[v] = u; visit(v, t)   # recursive!
    colour[u] = 'B'; _.time += 1; f[u] = _.time
    if at_finish: at_finish(u)
  for u in V:
    colour[u], p[u] = 'W', None
  for u in V:
    if colour[u] == 'W':
      t = []; visit(u, t); ts.append(t)
  return p, ts, d, f
                                                                # }}}1

# === Topological sort and longest path ===

def topological_sort(G):
  """Perform topological sort on a directed acyclic graph (DAG)."""
  vs = deque()
  def at_finish(u): vs.appendleft(u)
  dfs(G, at_finish = at_finish)
  return vs

def topological_sort2(G):                                       # {{{1
  """Perform topological sort on a directed acyclic graph (DAG)."""
  V, E  = G; vs = []
  ET_l  = dict( (k,len(v)) for k, v in transpose(G)[1].items() )
  s     = [ u for u in V if ET_l[u] == 0 ]
  while s:
    u = s.pop(); vs.append(u)
    for v in E[u]:
      ET_l[v] -= 1  # remove edge
      if ET_l[v] == 0: s.append(v)
  return vs
                                                                # }}}1

def longest_path(G):
  """Find the length of the longest path in a DAG."""
  V, E = G; lens = {}; ET = transpose(G)[1]; V_ = topological_sort(G)
  for u in V_:
    vs      = [ lens[v] for v in ET[u] ]
    lens[u] = max( vs ) + 1 if vs else 0
  return max(lens.values())

# === Strongly connected components ===

def strongly_connected_components(G):                           # {{{1
  """Find the strongly connected componens of a graph."""
  V, E    = G; ET = transpose(G)[1]; V_ = deque()
  dfs(G, at_finish = lambda u: V_.appendleft(u)); ts = dfs((V_,ET))[1]
  ts_     = [ tuple(sorted(set(t))) for t in ts ]
  if all( isinstance(x, str) and len(x) == 1 for x in V ):
    ts_   = [ "".join(t) for t in ts_ ]
  comp    = dict( (u,t) for t in ts_ for u in t )
  SCC_E   = dict( (t,list(set([ comp[v] for u in t for v in E[u]
                                        if comp[v] != t ])))
                  for t in ts_ )
  return (ts_, SCC_E)
                                                                # }}}1

# === Dijkstra's algorithm ===

def dijkstra(G, s, w, neighbors = None, at_dequeue = None):     # {{{1
  """Dijkstra's algorithm."""
  if neighbors is None: neighbors = lambda u: E[u]
  if isinstance(w, dict): w_, w = w, lambda u, v: w_[u][v]
  V, E  = G; d = { s: 0 }; p = { s: None }; S = set()
  q     = []; heapq.heappush(q, (0,s))
  for u in V: d.setdefault(u, None)
  while q:
    n, u = heapq.heappop(q)
    if u in S: continue
    S.add(u)
    if at_dequeue: at_dequeue(u, q, d)
    for v in neighbors(u):
      if d[v] is None or d[v] > d[u] + w(u, v):
        d[v] = d[u] + w(u, v); heapq.heappush(q, (d[v],v)); p[v] = u
  return d, p
                                                                # }}}1

# === Bellman-Ford algorithm ===

class NegativeWeightCycle(Exception): pass

# TODO: add negative-weight cycle test case
def bellman_ford(G, s, w, after_pass = None):                   # {{{1
  """Bellman-Ford algorithm."""
  if isinstance(w, dict): w_, w = w, lambda u, v: w_[u][v]
  V, E  = G; d = { s: 0 }; p = { s: None }
  edges = lambda: ( (u,v) for u in V for v in E[u] )
  for u in V: d.setdefault(u, None)
  for i in xrange(len(V)-1):
    for u, v in edges():
      if d[u] is not None and (d[v] is None or d[v] > d[u] + w(u, v)):
        d[v] = d[u] + w(u, v); p[v] = u
    if after_pass: after_pass(d, p)
  for u, v in edges():
    if d[v] is None or d[v] > d[u] + w(u, v):
      raise NegativeWeightCycle()
  return d, p
                                                                # }}}1

# === Ford-Fulkerson algorithm ===

# TODO: confirm the algorithm actually works correctly
def ford_fulkerson(G, s, t, c, after_pass = None):              # {{{1
  """Ford-Fulkerson algorithm."""
  if isinstance(c, dict): c_, c = c, lambda u, v: c_[u][v]
  V, E  = G; ET = transpose(G)[1]; f = {}
  edges = lambda: ( (u,v) for u in V for v in E[u] )
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

# === Universal sink (celebrity problem) ===

def universal_sink(G):
  """Determine whether graph G has a universal sink; expects E to be
  an adjacency matrix."""
  V, E = G; n = 0
  for i in xrange(1, len(V)):
    if E[n][i]: n = i
  for i in xrange(len(V)):
    if i != n and (E[n][i] or not E[i][n]): return None
  return n

# === Miscellaneous graph algorithms ===

def transpose(G):
  """Transpose graph."""
  V, E = G; ET = {}
  for u in V: ET[u] = []
  for u, vs in E.items():
    for v in vs: ET[v].append(u)
  return (V, ET)

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

# === MiniMax w/ Alpha-Beta Pruning ===

def minimax_alphabeta(node, alpha, beta, leaf_node  = None,     # {{{1
                      value     = None , children   = None,
                      set_value = None , start_max  = True,
                      verbose   = False, pre        = ""):
  """MiniMax w/ Alpha-Beta Pruning."""
  leaf_node, value, children, set_value = minimax_defaults( \
  leaf_node, value, children, set_value)
  if verbose: print(pre + "minimax({}, {})".format(alpha, beta))
  if leaf_node(node):
    if verbose: print(pre + "| leaf (value = {})".format(value(node)))
    return value(node)
  for child_node in children(node):
    x = minimax_alphabeta(child_node, alpha, beta, leaf_node, value,
                          children, set_value, not start_max, verbose,
                          pre + "  ")
    if start_max: alpha = max(alpha, x)
    else:         beta  = min(beta , x)
    if verbose: print(pre + "| alpha = {} beta = {}".format(alpha, beta))
    if alpha >= beta:
      v = beta if start_max else alpha
      if verbose: print(pre + "| pruning; value = {}".format(v))
      set_value(node, v); return v
  v = alpha if start_max else beta
  if verbose: print(pre + "| value = {}".format(v))
  set_value(node, v); return v
                                                                # }}}1

def minimax_defaults(l, v, c, s):                               # {{{1
  if l is None: l = lambda x: not isinstance(x, dict)
  if v is None: v = lambda x: x if l(x) else x["value"]
  if c is None: c = lambda x: x["children"]
  if s is None:
    def s(x, v): x["value"] = v
  return l, v, c, s
                                                                # }}}1

# === d-ary heap ===

def heap_parent(d, i):
  """Parent in d-ary heap of element at position i in list."""
  return (i-1)//d

def maxheapify(d, A, i, size = None):                           # {{{1
  """Float element at position i in list down its subtrees in the
  d-ary heap (to preserve the max-heap property)."""
  if size is None: size = len(A)
  largest = i
  for j in xrange(d*i+1, min(size, d*i+d+1)):
    if A[j] > A[largest]: largest = j
  if largest != i:
    A[i], A[largest] = A[largest], A[i]
    maxheapify(d, A, largest, size)
                                                                # }}}1

# TODO: smaller range?
def build_maxheap(d, A):
  """Turn list A into a d-ary max-heap."""
  for i in xrange(len(A)-1, -1, -1): maxheapify(d, A, i)

def heapsort(d, A, copy = False):
  """Heapsort."""
  if copy: A = A[:]
  size = len(A); build_maxheap(d, A)
  for i in xrange(len(A)-1, 0, -1):
    A[0], A[i] = A[i], A[0]; size -= 1
    maxheapify(d, A, 0, size)
  if copy: return A

def heap_extract_max(d, A):
  """Pop maximum element from d-ary heap."""
  if len(A) < 1: raise IndexError("heap underflow")
  m, A[0] = A[0], A[len(A)-1]
  A.pop(); maxheapify(d, A, 0)
  return m

def heap_insert(d, A, key):
  """Insert element into d-ary heap."""
  A.append(None); i = len(A)-1
  while i > 0 and A[heap_parent(d, i)] < key:
    p = heap_parent(d, i); A[i], i = A[p], p
  A[i] = key

def heap_increase_key(d, A, i, key):
  """Increase key of element at position i in list whilst preserving
  the max-heap property of the d-ary heap."""
  if key < A[i]: raise ValueError("new key less than current key")
  A[i] = key
  while i > 0 and A[heap_parent(d, i)] < A[i]:
    p = heap_parent(d, i); A[i], A[p], i = A[p], A[i], p

# === Extended Euclidean algorithm ===

def egcd(a, b, verbose = False):                                # {{{1
  """Extended Euclidean algorithm.  Returns gcd, Bézout coefficients
  and quotients of a and b by their greatest common divisor."""
  r_, r, s_, s, t_, t = a, b, 1, 0, 0, 1
  if verbose:
    print("q=%10s r=%10d s=%10d t=%10d" % ("",r_,s_,t_))
    print("q=%10s r=%10d s=%10d t=%10d" % ("",r, s ,t ))
  while r != 0:
    q     = r_ // r
    r_, r = r, r_ - q*r
    s_, s = s, s_ - q*s
    t_, t = t, t_ - q*t
    if verbose: print("q=%10d r=%10d s=%10d t=%10d" % (q,r,s,t))
  return r_, (s_, t_), (t, s)
                                                                # }}}1

# === Lazy List ===

# NB: copied from https://github.com/obfusk/obfusk.py

class llist(object):                                            # {{{1
  """Lazy list."""
  class iterator(object):
    __slots__ = "l n".split()
    def __init__(self, l): self.l, self.n = l, 0
    def __iter__(self): return self
    def next(self):
      try:
        m = self.n; self.n += 1; return self.l[m]
      except IndexError: raise StopIteration
    __next__ = next
  __slots__ = "data it lock".split()
  def __init__(self, it, rec = None):
    """Initialise with iterable; for recursive definitions, rec can be
    passed a lambda that takes the llist and returns an iterable (to
    chain to the first one)."""
    self.data, self.lock = [], threading.RLock()
    self.it = iter(itertools.chain(it, rec(self)) if rec else it)
  def __iter__(self): return type(self).iterator(self)
  def __getitem__(self, k):
    """Item at index or islice."""
    if isinstance(k, slice):
      return itertools.islice(self, k.start, k.stop, k.step)
    elif not isinstance(k, int):
      raise TypeError("indices must be integers or slices")
    while k >= len(self.data):
      try:
        with self.lock: self.data.append(next(self.it))
      except StopIteration: break
    return self.data[k]
                                                                # }}}1

fibs = llist([0, 1], rec = lambda fibs:
       ( m+n for m,n in izip(fibs, fibs[1:]) ))

# === Prime Numbers (Sieve of Eratosthenes) ===

def erastothenes():                                             # {{{1
  """All prime numbers (generated using Sieve of Eratosthenes;
  adapted from Python Cookbook)."""
  composites = {} # maps composite ints to first found prime factor
  yield 2
  for k in itertools.count(3, 2):
    p = composites.pop(k, None)
    if p is None:
      composites[k*k] = k; yield k
    else:
      m = p + k
      while m in composites or not (m&1): m += p
      composites[m] = p
                                                                # }}}1

def _make_prime_sieve(sieve = None):                            # {{{1
  """Generate lazy memoising prime sieve."""
  PRIMES, lock  = [], threading.Lock()
  it            = iter(erastothenes() if sieve is None else sieve)
  def primes():
    """Generates all primes (i.e. lazy, memoising prime sieve; uses
    erastothenes())."""
    n = 0
    while True:
      with lock:
        if n < len(PRIMES): p = PRIMES[n]
        else:
          p = next(it); PRIMES.append(p)
      yield p; n += 1
  return primes
                                                                # }}}1

mprimes = _make_prime_sieve()   # memoised primes
lprimes = llist(erastothenes()) # lazy primes; slower

def primes_up_to(n, ps = None):
  """Prime numbers <= n."""
  if ps is None: ps = mprimes()
  return itertools.takewhile(lambda p: p <= n, ps)

def prime_factors(n, ps = None):                                # {{{1
  """Prime factors of n."""
  if ps is None: ps = mprimes()
  for p in itertools.takewhile(lambda p: p*p <= n, ps):
    while n > 1:
      q, r = divmod(n, p)
      if r != 0: break
      n = q; yield p
    if n == 1: break
  if n != 1: yield n
                                                                # }}}1

def divisors(n, factors = None):
  """Divisors of n (sorted)."""
  ps = tuple((prime_factors if factors is None else factors)(n))
  return sorted(set( reduce(operator.mul, xs, 1)
                     for r in xrange(len(ps)+1)
                     for xs in itertools.combinations(ps, r) ))

# === SAMPLE DATA ===

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
