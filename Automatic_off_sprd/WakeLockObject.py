# -*- coding: UTF-8 -*-
class WakeLock(object):

    def __init__(self, name, lock,time):
        self.name = name
        self.lock = lock
        self.time = time

    @property
    def _name_(self):
        return self.name

    @_name_.setter
    def _name_(self,name):
        self.name = name

    @property
    def _lock_(self):
        return self.lock

    @_lock_.setter
    def _lock_(self,lock):
        self.lock = lock

    @property
    def _time_(self):
        return self.time

    @_time_.setter
    def _time_(self,time):
        self.time = time


