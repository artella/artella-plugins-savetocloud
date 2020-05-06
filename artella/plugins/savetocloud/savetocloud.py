#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Artella Save to Cloud plugin implementation
"""

from __future__ import print_function, division, absolute_import

from artella.core import plugin


class SaveToCloudPlugin(plugin.ArtellaPlugin, object):

    ID = 'artellapipe-plugins-savetocloud'
    INDEX = 1

    def __init__(self, config_dict=None, manager=None):
        super(SaveToCloudPlugin, self).__init__(config_dict=config_dict, manager=manager)
