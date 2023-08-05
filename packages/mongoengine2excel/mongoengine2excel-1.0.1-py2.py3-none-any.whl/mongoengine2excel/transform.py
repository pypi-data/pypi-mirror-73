# coding: utf-8
import typing

NormalizedDoc = typing.TypeVar('NormalizedDoc')


class DefaultTransformer(object):

    def normalize_doc(self, mongo_doc) -> NormalizedDoc:
        """
        :type mongo_doc: mongoengine.Document
        """

        normalized = dict(mongo_doc.to_mongo())
        normalized['id'] = str(normalized.pop('_id'))
        to_truncate_fields = [k for k, v in normalized.items() if isinstance(v, str) and len(v) > 32000]

        for field in to_truncate_fields:
            normalized[field] = normalized[field][:32000]

        return normalized

    def normalized_doc_to_rows(self, normalized: NormalizedDoc) -> typing.List[typing.Dict]:
        return [normalized]
