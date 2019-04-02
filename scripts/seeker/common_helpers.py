#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# seekiir Framework - Common Files
# Helper Functions and Classes
#

__author__ = 'David Maxwell <maxwelld90@gmail.com>'
__date__ = '2012-10-17'

def file_exists(filename):
    '''
    Helper function which returns a boolean value indicating if the file specified by string parameter filename exists.
    Solution from http://stackoverflow.com/questions/82831/how-do-i-check-if-a-file-exists-using-python
    '''
    try:
        with open(filename) as f: pass
        return True
    except IOError:
        return False



class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
