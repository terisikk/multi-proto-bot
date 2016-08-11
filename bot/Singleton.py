# -*- coding: utf-8 -*-
# @Author: teemu
# @Date:   2016-06-13 22:02:23
# @Last Modified by:   Teemu Risikko
# @Last Modified time: 2016-06-18 09:29:22
import threading


def singleton(theclass):
    instances = {}
    # theclass._shared_state = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        with lock:
            if theclass not in instances:
                instances[theclass] = theclass(*args, **kwargs)
        return instances[theclass]
    return get_instance


class Singleton(type):
    _instances = {}
    lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls.lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
