# coding: utf-8
import os
from mongoengine2excel import transform, utils

import logging


class MongoEngineToExcel(object):
    def __init__(
            self,
            qs: callable,
            including_fields: set = None,
            excluding_fields: set = None,
            dest_directory='/tmp',
            dest_prefix='documents',
            mapper: dict = None,
            chunk_size=60000,
            transformer=transform.DefaultTransformer(),
            logger=logging.getLogger(__name__).getChild('mongoengine2excel')
    ):
        self._qs = qs().no_cache()
        self._including_fields = set(including_fields or [])
        self._excluding_fields = set(excluding_fields or [])

        self._mapper = mapper
        self._dest_directory = dest_directory
        self._dest_prefix = dest_prefix

        self._current_rows = []
        self._current_file = None
        self._current_chunk = 0
        self._chunk_size = chunk_size

        self._transformer = transformer
        self._logger = logger

        self._dest_filenames = []

    def add_rows(self, mongo_document, auto_flush=True):
        normalized = self._transformer.normalize_doc(mongo_document)
        rows = self._transformer.normalized_doc_to_rows(normalized)
        for row in rows:
            self._current_rows.append(row)
            if auto_flush:
                self.maybe_flush()

    def maybe_flush(self):
        if len(self._current_rows) % self._chunk_size == 0:
            self.flush()

    def flush(self):
        self._current_chunk += 1
        dest_filename = os.path.join(
            self._dest_directory,
            f'{self._dest_prefix}-{self._current_chunk}.xls'
        )
        self._logger.info(f'generate excel file: dst={dest_filename} rows={len(self._current_rows)}')
        utils.to_excel(self._current_rows, self._mapper, dest_filename)
        self._dest_filenames.append(dest_filename)
        self._current_rows = []

    def to_excel(self):
        qs = self._qs
        if self._including_fields:
            qs = qs.only(*self._including_fields)
        if self._excluding_fields:
            qs = qs.only(*self._excluding_fields)
        total = qs.count()
        for idx, doc in enumerate(qs, 1):
            if idx % 100 == 0:
                self._logger.info(f'handle doc: {idx}/{total}')
            self.add_rows(doc, auto_flush=True)

        if self._current_rows:
            self.flush()

        return self._dest_filenames
