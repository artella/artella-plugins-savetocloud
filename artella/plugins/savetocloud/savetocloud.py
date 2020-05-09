#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Artella Save to Cloud plugin implementation
"""

from __future__ import print_function, division, absolute_import

import os

import artella
from artella import dcc
from artella import logger
from artella.core import plugin


class SaveToCloudPlugin(plugin.ArtellaPlugin, object):

    ID = 'artella-plugins-savetocloud'
    INDEX = 1

    def __init__(self, config_dict=None, manager=None):
        super(SaveToCloudPlugin, self).__init__(config_dict=config_dict, manager=manager)

    def save_to_cloud(self, file_path=None):
        """
        Uploads a new file/folder or a new version of current opened DCC scene file

        :param str file_path: Optional path of the file we want to create new version of. If not given, current
            opened DCC scene file path will be used.
        :return: True if the operation was successful; False otherwise.
        :rtype: bool
        """

        if not self.is_loaded():
            logger.log_warning('Impossible to save file to cloud. Save to Cloud Artella Plugin is not loaded!')
            return False

        artella_drive_client = artella.DccPlugin().get_client()
        if not artella_drive_client:
            return False

        if not file_path:
            file_path = dcc.scene_name()
            if not file_path:
                msg = 'Please open a file before creating a new version'
                logger.log_warning(msg)
                dcc.show_warning(title='Artella Failed to make new version', message=msg)
                return False

        can_lock = artella_drive_client.can_lock_file(file_path=file_path)
        if not can_lock:
            msg = 'Unable to lock file to make new version. File is already locked by other user.'
            dcc.show_error('File already locked by other user', msg)
            logger.log_error(msg)
            return False

        comment = self.get_version_comment(current_file=file_path)
        if comment is False:
            return False

        make_new_version = artella.DccPlugin().make_new_version(file_path=file_path, comment=comment)

        if make_new_version:
            msg = 'Save to Cloud was completed successully! New file version is available in Artella Drive.'
            logger.log_info(msg)
            dcc.show_info('Save to Cloud', msg)

        return make_new_version

    def get_version_comment(self, current_file):
        """
        Retrieves comment version in a DCC specific way.
        This class can be override to retrieve the version comment on different ways

        :param str current_file: Absolute local file path we want to create new comment for
        :return: Typed comment write by the user
        :rtype: str
        """

        artella_drive_client = artella.DccPlugin().get_client()
        if not artella_drive_client:
            return False

        file_version = artella_drive_client.file_current_version(current_file)
        if file_version <= -1:
            return False

        next_version = file_version + 1
        comment, ok = dcc.input_comment(
            'Artella - Save to Cloud', 'Saving {} (version {})\n\nComment:'.format(
                os.path.basename(current_file), next_version))
        if not ok:
            logger.log_info('Cancelled Save to Cloud operation by user.')
            return False

        return comment
