#!/usr/bin/env python

from __future__ import with_statement

import sys, os, os.path
import struct

class FormatError(Exception):
    pass

class CompoundFile(object):
    DEFAULT_BUFFER_SIZE = 1024 * 1024
        
    DEFAULT_V3_SECTOR_SHIFT = 0x09
    DEFAULT_V4_SECTOR_SHIFT = 0x0C
    DEFAULT_MINI_SECTOR_SHIFT = 0x06
    
    SIGNATURE = '\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
    
    def __init__(self, file_or_path=None, readonly=True, overwrite=False, bufsize=DEFAULT_BUFFER_SIZE):
        if file_or_path:
            self.open(file_or_path, readonly, overwrite, bufsize)
        else:
            self.file = None
            self.mmap = None
        
        self.major_ver = 4    
        self.minor_ver = 0x3E
        
        self.sector_shift = self.DEFAULT_V4_SECTOR_SHIFT
        self.mini_sector_shift = self.DEFAULT_MINI_SECTOR_SHIFT
        
        self.dir_sector_count = 0        
        self.fat_sector_count = 0
        self.first_dir_sector_pos = 0
        self.trans_sig_num = 0
        self.mini_stream_cutoff_size = 0
        self.first_mini_fat_sector_pos = 0
        self.mini_fat_sector_count = 0
        self.first_difat_sector_pos = 0        
        self.difat = []
        
    @property
    def sector_size(self):
        return 1 << self.sector_shift
    
    @property
    def sector_count(self):
        return self.mmap.size() / self.sector_size
    
    @property
    def mini_sector_size(self):
        return 1 << self.mini_sector_shift
    
    def open(self, file_or_path, readonly=True, overwrite=False, bufsize=DEFAULT_BUFFER_SIZE):
        import mmap
        
        if readonly:
            mode = 'rb'
        elif overwrite:
            mode = 'wb'
        else:
            mode = 'wb+'
        
        if type(file_or_path) in [str, unicode]:
            self.file = open(file_or_path, mode, bufsize)
        else:
            self.file = file_or_path
            
        params = {}
            
        if sys.platform == 'win32':
            params['access'] = mmap.ACCESS_READ if readonly else mmap.ACCESS_WRITE
        
        self.mmap = mmap.mmap(self.file.fileno(), 0, **params)
            
        self._parseFileHeader()
        
    def close(self):
        if self.mmap: self.mmap.close()
        if self.file: self.file.close()
        
    @property
    def closed(self):
        return self.file.closed if self.file else True
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        
    def _parseFileHeader(self):
        if self.mmap.size() < 512:
            raise FormatError("invalid size of header")
            
        if self.SIGNATURE != self.mmap[:8]:
            raise FormatError("invalid signature in header")
            
        if '\0'*16 != self.mmap[8:24]:
            raise FormatError("invalid clsid in header")
            
        self.minor_ver, self.major_ver, byte_order, \
        self.sector_shift, self.mini_sector_shift = struct.unpack('<5H', self.mmap[24:34])
        
        if 0x3E != self.minor_ver or self.major_ver not in [3, 4] or 0xFFFE != byte_order or \
           self.DEFAULT_MINI_SECTOR_SHIFT != self.mini_sector_shift or \
           { 3: self.DEFAULT_V3_SECTOR_SHIFT, 4: self.DEFAULT_V4_SECTOR_SHIFT}[self.major_ver] != self.sector_shift:
            raise FormatError("invalid fields in header")
        
        self.dir_sector_count, self.fat_sector_count, self.first_dir_sector_pos, \
        self.trans_sig_num, self.mini_stream_cutoff_size, self.first_mini_fat_sector_pos, \
        self.mini_fat_sector_count, self.first_difat_sector_pos, difat_sector_count \
            = struct.unpack('<9i', self.mmap[40:76])
        self.difat = list(struct.unpack('<109I', self.mmap[76:76+109*4]))
        
        if (self.dir_sector_count + self.fat_sector_count + \
            self.mini_fat_sector_count + difat_sector_count) >= self.sector_count or \
           self.first_dir_sector_pos >= self.sector_count or \
           self.first_mini_fat_sector_pos >= self.sector_count or \
           self.first_difat_sector_pos >= self.sector_count:
            raise FormatError("invalid size of body")