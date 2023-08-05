"""Ordering classes."""
from graphene.utils.str_converters import to_snake_case
from sqlalchemy import desc

DESC_ORDER_CHAR = '-'


def applicable_ordering(order_by):
    for _o in order_by:
        o = _o.lstrip(DESC_ORDER_CHAR)
        o_snake = to_snake_case(o)
        yield desc(o_snake) if o != _o else o_snake


def order_query(query, order_by):
    _order_by = list(applicable_ordering(order_by))
    return query.order_by(*_order_by)
