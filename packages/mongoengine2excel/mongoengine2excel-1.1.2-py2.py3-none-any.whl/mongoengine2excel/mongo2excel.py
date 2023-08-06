# coding: utf-8
import logging

from mongoengine2excel import transform
from mongoengine2excel.iterator2excel import Iterator2Excel


class MongoEngineToExcel(object):
    def __init__(
            self,
            qs,
            including_fields=None,
            excluding_fields=None,
            dest_directory='/tmp',
            dest_prefix='documents',
            mapper=None,
            chunk_size=60000,
            transformer=transform.DefaultTransformer(),
            logger=logging.getLogger(__name__).getChild('mongoengine2excel')
    ):
        """
        :type qs: callable
        :type including_fields: set
        :type excluding_fields: set
        :type dest_directory: str
        :type dest_prefix: str
        :type mapper: dict
        :type chunk_size: int
        :type transformer:
        :type logger:
        """
        self._qs = qs().no_cache()
        self._including_fields = set(including_fields or [])
        self._excluding_fields = set(excluding_fields or [])

        self._transformer = transformer
        self._logger = logger

        self._iter2excel = Iterator2Excel(
            self.make_iter(),
            chunk_size,
            dest_directory,
            dest_prefix,
            mapper
        )

    def make_iter(self):
        qs = self._qs
        if self._including_fields:
            qs = qs.only(*self._including_fields)
        if self._excluding_fields:
            qs = qs.only(*self._excluding_fields)
        total = qs.count()
        for idx, mongo_doc in enumerate(qs, 1):
            if idx % 100 == 0:
                self._logger.info('handle doc: {}/{}'.format(idx, total))
            normalized = self._transformer.normalize_doc(mongo_doc)
            for row in self._transformer.normalized_doc_to_rows(normalized):
                yield row

    def to_excel(self):
        return self._iter2excel.to_excel()
