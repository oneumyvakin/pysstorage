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
            
            self.assertEquals(4, cf.major_ver)
            self.assertEquals(0x3E, cf.minor_ver)
            self.assertEquals(CompoundFile.DEFAULT_V4_SECTOR_SHIFT, cf.sector_shift)
            self.assertEquals(CompoundFile.DEFAULT_MINI_SECTOR_SHIFT, cf.mini_sector_shift)

if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG if "-v" in sys.argv else logging.WARN,
                        format='%(asctime)s %(levelname)s %(message)s')

    unittest.main()
    