# -*- coding: utf-8 -*-
# @Author: teemu
# @Date:   2016-05-22 19:29:49
# @Last Modified by:   teemu
# @Last Modified time: 2016-05-22 19:32:47

from bot.AbstractConnection import AbstractConnection


class MumbleConnection(AbstractConnection):
    def __init__(self):
        super(MumbleConnection, self).__init__()
