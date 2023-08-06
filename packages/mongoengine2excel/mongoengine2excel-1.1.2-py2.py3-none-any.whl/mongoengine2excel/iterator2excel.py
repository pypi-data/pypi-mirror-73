# coding: utf-8
import os
import logging

from mongoengine2excel import utils


class Iterator2Excel(object):
    def __init__(
            self,
            iterator,
            chunk_size,
            dest_directory='/tmp',
            dest_prefix='documents',
            row_mapper=None,
            logger=logging.getLogger(__name__).getChild('iter2excel')
    ):
        self._iterator = iterator

        self._current_rows = []
        self._current_file = None
        self._current_chunk = 0
        self._chunk_size = chunk_size
        self._current_file = None

        self._dest_directory = dest_directory
        self._dest_prefix = dest_prefix
        self._dest_filenames = []

        self._row_mapper = row_mapper

        self._logger = logger

    def maybe_flush(self):
        if len(self._current_rows) % self._chunk_size == 0:
            self.flush()

    def flush(self):
        self._current_chunk += 1
        dest_filename = os.path.join(
            self._dest_directory,
            '{}-{}.xls'.format(self._dest_prefix, self._current_chunk)
        )
        self._logger.info('generate excel file: dst={} rows={}'.format(dest_filename, len(self._current_rows)))
        utils.to_excel(self._current_rows, self._row_mapper, dest_filename)
        self._dest_filenames.append(dest_filename)
        self._current_rows = []

    def add_row(self, row_data, auto_flush=True):
        """
        :type row_data:  dict
        :type auto_flush: bool
        """
        self._current_rows.append(row_data)
        if auto_flush:
            self.maybe_flush()

    def to_excel(self):
        for row in self._iterator:
            self.add_row(row)
        if self._current_rows:
            self.flush()
        return self._dest_filenames
