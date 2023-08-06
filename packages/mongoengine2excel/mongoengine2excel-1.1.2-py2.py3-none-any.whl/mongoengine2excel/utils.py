# coding: utf-8
import pandas as pd


def make_renamed_df(records, mapper):
    df = pd.DataFrame(records)

    if mapper is None:
        mapper = list(df.columns)

    if isinstance(mapper, list):
        from collections import OrderedDict
        mapper = OrderedDict([(field, field) for field in mapper])
    elif isinstance(mapper, dict):
        mapper = mapper
    elif mapper:
        raise ValueError

    return df[list(mapper.keys())].rename(
        columns=mapper
    )


def to_excel(records, mapper, dst, keep_index_column=False):
    """
    :type records: list[dict]
    :type mapper: dict | list | None
    :type dst: basestring
    :param keep_index_column: If keep num index column in excel file
    """

    writer = pd.ExcelWriter(dst)
    output_df = make_renamed_df(records, mapper)
    output_df.to_excel(writer, index=keep_index_column)
    writer.save()
