"""Filtering classes."""
import operator

DELIMITER = '_'
RANGE_BEGIN = 'begin'
RANGE_END = 'end'

SEPARATOR = '__'
EQUAL = ''
NOT_EQUAL = 'Ne'
INTENSIVE_LIKE = 'Ilike'
IS_NULL = 'IsNull'
IN = 'In'
NOT_IN = 'NotIn'
LESSER_THAN = 'Lt'
LESSER_THAN_OR_EQUAL = 'Lte'
GREATER_THAN = 'Gt'
GREATER_THAN_OR_EQUAL = 'Gte'
RANGE = 'Range'
CONTAINS = 'Contains'
CONTAINED_BY = 'ContainedBy'
OVERLAP = 'Overlap'
ALL = (
    EQUAL,
    NOT_EQUAL,
    INTENSIVE_LIKE,
    IS_NULL,
    IN,
    NOT_IN,
    LESSER_THAN,
    LESSER_THAN_OR_EQUAL,
    GREATER_THAN,
    GREATER_THAN_OR_EQUAL,
    RANGE,
    CONTAINS,
    CONTAINED_BY,
    OVERLAP,
)
OPERATOR = {
    EQUAL: operator.eq,
    NOT_EQUAL: operator.ne,
    INTENSIVE_LIKE: lambda a, b: getattr(a, 'ilike')(b),
    IS_NULL: lambda a, b: getattr(a, 'in_')(b),
    IN: lambda a, b: getattr(a, 'in_')(b),
    NOT_IN: lambda a, b: getattr(a, 'notin_')(b),
    LESSER_THAN: operator.lt,
    LESSER_THAN_OR_EQUAL: operator.le,
    GREATER_THAN: operator.gt,
    GREATER_THAN_OR_EQUAL: operator.ge,
    RANGE: lambda a, b: a.between(a[RANGE_BEGIN], b[RANGE_END]),
    CONTAINS: lambda a, b: getattr(a, 'contains')(b),
    CONTAINED_BY: lambda a, b: True,  # todo
    OVERLAP: lambda a, b: True,  # todo
}


def _where_clause(applicable_filters):
    try:
        cond = next(applicable_filters)
        for op in applicable_filters:
            cond = operator.and_(cond, op)
        return cond
    except StopIteration:
        return True


def _applicable_filters(filters, model):
    for filter_, val in filters.items():
        try:
            field, op = filter_.split(SEPARATOR)
        except ValueError:
            field, op = filter_, EQUAL
        args = [getattr(model, field), val]
        # TODO filter restrictions
        yield OPERATOR[op](*args)


def filter_query(query, filters, model):
    """
    Get an operator to perform filtering.

    :return:
    """
    applicable_filters = _applicable_filters(filters, model)
    where_clause = _where_clause(applicable_filters)
    return query.where(where_clause)
