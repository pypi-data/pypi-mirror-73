
from graphene_gino.filtering import filter_query
from graphene_gino.ordering import order_query

TOTAL_FIELD = '__total__'


async def exists(db, expr):
    """
    Check if object exists.

    :param expr: SQL Alchemy core expression
    :return: True if an object exists
    """
    return await db.scalar(db.exists().where(
        expr,
    ).select())


async def get_query(model, info, filters=None, order_by=None, page=None, paginate_by=None, total_query=None):
    query = getattr(model, 'query', None)
    query = filter_query(query, filters or {}, model)
    query = order_query(query, order_by or [])
    return query


def to_type_name(name):
    """Convert the given name to a GraphQL type name."""
    return ''.join(part[:1].upper() + part[1:] for part in name.split('_'))
