# -*- coding: utf-8 -*-
# @Author: teemu
# @Date:   2016-06-12 11:22:49
# @Last Modified by:   teemu
# @Last Modified time: 2016-06-13 22:03:39

import configparser
from Singleton import Singleton


class Configurations(metaclass=Singleton):
    parser = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation())

    def __init__(self):
        pass

    def read(self, filepath):
        self.parser.read(filepath)

    def sections(self):
        return self.parser.sections()

    def get(self, section, setting, default=None):
        return self.parser.get(section, setting, fallback=default)
