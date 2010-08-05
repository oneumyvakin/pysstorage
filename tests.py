#!/usr/bin/env python
from __future__ import with_statement

import sys
import logging

import unittest

from pysstorage import *

class TestCompoundFile(unittest.TestCase):
    def testRead(self):
        with CompoundFile('test.doc') as cf:
            self.assertFalse(cf.closed)

if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG if "-v" in sys.argv else logging.WARN,
                        format='%(asctime)s %(levelname)s %(message)s')

    unittest.main()
    