from graphene import (
    ID,
    UUID,
    Boolean,
    Field,
    Float,
    Int,
    List,
    String,
)
from graphene.types.json import JSONString
from singledispatch import singledispatch
from sqlalchemy import types
from sqlalchemy.dialects import postgresql

try:
    from sqlalchemy_utils import ChoiceType, JSONType, ScalarListType, TSVectorType
except ImportError:
    ChoiceType = JSONType = ScalarListType = TSVectorType = object


def get_column_doc(column):
    return getattr(column, 'doc', None)


def is_column_nullable(column):
    return bool(getattr(column, 'nullable', True) or
                getattr(column, 'default'))


def convert_sqlalchemy_column(column, registry, resolver, **field_kwargs):
    field_kwargs.setdefault('type', convert_sqlalchemy_type(getattr(column, 'type', None), column, registry))
    field_kwargs.setdefault('required', not is_column_nullable(column))
    field_kwargs.setdefault('description', get_column_doc(column))

    return Field(
        resolver=resolver,
        **field_kwargs,
    )


@singledispatch
def convert_sqlalchemy_type(type, column, registry=None):  # noqa: A002
    raise Exception(
        "Don't know how to convert the SQLAlchemy field {0} ({1})".format(column, column.__class__),
    )


@convert_sqlalchemy_type.register(postgresql.UUID)
def convert_column_to_uuid(type, column, registry=None):  # noqa: A002
    return UUID


@convert_sqlalchemy_type.register(types.Date)
@convert_sqlalchemy_type.register(types.Time)
@convert_sqlalchemy_type.register(types.String)
@convert_sqlalchemy_type.register(types.Text)
@convert_sqlalchemy_type.register(types.Unicode)
@convert_sqlalchemy_type.register(types.UnicodeText)
@convert_sqlalchemy_type.register(postgresql.INET)
@convert_sqlalchemy_type.register(postgresql.CIDR)
@convert_sqlalchemy_type.register(TSVectorType)
def convert_column_to_string(type, column, registry=None):  # noqa: A002
    return String


@convert_sqlalchemy_type.register(types.DateTime)
def convert_column_to_datetime(type, column, registry=None):  # noqa: A002
    from graphene.types.datetime import DateTime
    return DateTime


@convert_sqlalchemy_type.register(types.SmallInteger)
@convert_sqlalchemy_type.register(types.Integer)
def convert_column_to_int_or_id(type, column, registry=None):  # noqa: A002
    return ID if column.primary_key else Int


@convert_sqlalchemy_type.register(types.Boolean)
def convert_column_to_boolean(type, column, registry=None):  # noqa: A002
    return Boolean


@convert_sqlalchemy_type.register(types.Float)
@convert_sqlalchemy_type.register(types.Numeric)
@convert_sqlalchemy_type.register(types.BigInteger)
def convert_column_to_float(type, column, registry=None):  # noqa: A002
    return Float


@convert_sqlalchemy_type.register(ScalarListType)
def convert_scalar_list_to_list(type, column, registry=None):  # noqa: A002
    return List(String)


@convert_sqlalchemy_type.register(types.ARRAY)
@convert_sqlalchemy_type.register(postgresql.ARRAY)
def convert_array_to_list(_type, column, registry=None):
    inner_type = convert_sqlalchemy_type(column.type.item_type, column)
    return List(inner_type)


@convert_sqlalchemy_type.register(postgresql.HSTORE)
@convert_sqlalchemy_type.register(postgresql.JSON)
@convert_sqlalchemy_type.register(postgresql.JSONB)
def convert_json_to_string(type, column, registry=None):  # noqa: A002
    return JSONString


@convert_sqlalchemy_type.register(JSONType)
def convert_json_type_to_string(type, column, registry=None):  # noqa: A002
    return JSONString
