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


Links
=====


"""
                                                                # }}}1

from __future__ import print_function

import argparse, sys

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

# ...

if __name__ == "__main__":
  sys.exit(main(*sys.argv[1:]))

# vim: set tw=70 sw=2 sts=2 et fdm=marker :
