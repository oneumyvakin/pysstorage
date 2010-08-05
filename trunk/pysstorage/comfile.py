#!/usr/bin/env python

from __future__ import with_statement

import sys, os, os.path

class CompoundFile(object):
    def __init__(self, file_or_path=None, readonly=True):
        if file_or_path:
            self.open(file_or_path, mode)
        else:
            self.file = None
    
    def open(self, file_or_path, mode='rb'):        
        if type(file_or_path) in [str, unicode]:
            self.file = open(file_or_path, mode)
        else:
            self.file = file_or_path
            
        self.file.seek(0)
        
    def close(self):
        self.file.close()
        
    @property
    def closed(self):
        return self.file.closed 
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()