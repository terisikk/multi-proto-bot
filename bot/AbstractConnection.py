# -*- coding: utf-8 -*-
# @Author: teemu
# @Date:   2016-05-21 21:43:53
# @Last Modified by:   teemu
# @Last Modified time: 2016-06-11 17:14:49


class AbstractConnection(object):
    connection = None
    servers = []
    channels = []

    def __init__(self):
        self._nick = ""

    def _connect(self):
        raise NotImplementedError("Connect not implemeneted")

    def join_channel(self, name):
        raise NotImplementedError("join_channel not implemented")

    @property
    def nick(self):
        return self._nick

    @nick.setter
    def nick(self, nickname):
        self._nick = nickname

    def start(self):
        self._connect()
        # TODO: Add threading code
