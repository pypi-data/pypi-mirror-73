import operator

from graphene import (
    Field,
    InputField,
)
from graphene.relay.mutation import ClientIDMutation
from graphene.types.utils import yank_fields_from_attrs

from .logging import logger
from .registry import get_global_registry
from .types import (
    GinoObjectTypeOptions,
    construct_fields,
)
from .utils import exists


class GinoMutation(ClientIDMutation):
    @classmethod
    def __get_fieldset__(cls, meta, only_fields=(), exclude_fields=(), _as=Field):
        registry = get_global_registry()
        f = construct_fields(
            obj_type=cls,
            model=meta.model,
            registry=registry,
            only_fields=only_fields,
            exclude_fields=exclude_fields,
            batching=False,
            connection_field_factory=None,
        )
        return yank_fields_from_attrs(f, _as=Field)

    @classmethod
    def __get_fields__(cls, meta):
        return (), ()

    @classmethod
    def __init_subclass_with_meta__(cls, model=None, **options):
        db = model.__metadata__
        table = db.tables[model.__tablename__]

        _meta = GinoObjectTypeOptions(cls)
        _meta.model = model
        _meta.primary_key = table.primary_key.columns.keys()[0]
        _meta.primary_key_readonly = options.get('primary_key_readonly', True)
        _meta.readonly_fields = options.get('readonly_fields', ())
        _meta.db = db
        _meta.fields, input_fields = cls.__get_fields__(_meta)

        super(GinoMutation, cls).__init_subclass_with_meta__(
            _meta=_meta,
            input_fields=input_fields,
            **options,
        )

    @classmethod
    def ident(cls, data):
        """
        Object identifier retrieved from payload.

        :return: object primary key value
        """
        return data.get(cls._meta.primary_key)

    @classmethod
    async def validate(cls, **data):
        pass

    class Meta:
        abstract = True


class CreateMutation(GinoMutation):
    @classmethod
    def __get_fields__(cls, meta):
        fields = cls.__get_fieldset__(meta)
        exclude_fields = (
            *((meta.primary_key,) if meta.primary_key_readonly else ()),
            *getattr(meta, 'readonly_fields', ()),
        )
        input_fields = cls.__get_fieldset__(
            meta,
            exclude_fields=exclude_fields,
            _as=InputField,
        )
        return fields, input_fields

    @classmethod
    async def perform_create(cls, data):
        obj = await cls._meta.model.create(**data)
        return obj

    @classmethod
    async def mutate(cls, info, *args, **kwargs):
        model = cls._meta.model
        data = kwargs['input']
        ident = cls.ident(data)
        expr = operator.eq(getattr(model, cls._meta.primary_key), ident)
        await cls.validate(**data)
        if not await exists(cls._meta.db, expr):
            obj = await cls.perform_create(data)
        else:
            logger.debug('Object {0} with ident = {1} already exists'.format(
                model.__name__,
                ident,
            ))
            raise
        return cls(**obj.to_dict())

    class Meta:
        abstract = True


class UpdateMutation(GinoMutation):
    @classmethod
    def __get_fields__(cls, meta):
        fields = cls.__get_fieldset__(meta)
        input_fields = cls.__get_fieldset__(
            meta,
            exclude_fields=meta.readonly_fields,
            _as=InputField,
        )
        return fields, input_fields

    @classmethod
    async def perform_update(cls, obj, data):
        if obj:
            await obj.update(**data).apply()
        return obj

    @classmethod
    async def mutate(cls, info, *args, **kwargs):
        model = cls._meta.model
        data = kwargs['input']
        ident = cls.ident(data)
        expr = operator.eq(getattr(model, cls._meta.primary_key), ident)
        obj = await model.query.where(expr).gino.one()
        await cls.validate(**data)
        obj = await cls.perform_update(obj, data)
        return cls(**obj.to_dict())

    class Meta:
        abstract = True


class DeleteMutation(GinoMutation):
    @classmethod
    def __get_fields__(cls, meta):
        input_fields = cls.__get_fieldset__(meta, only_fields=(meta.primary_key,), _as=InputField)
        return (), input_fields

    @classmethod
    async def perform_delete(cls, obj):
        if obj:
            await obj.delete()

    @classmethod
    async def mutate(cls, info, *args, **kwargs):
        model = cls._meta.model
        data = kwargs['input']
        ident = cls.ident(data)
        expr = operator.eq(getattr(model, cls._meta.primary_key), ident)
        obj = await model.query.where(expr).gino.one()
        await cls.perform_delete(obj)

    class Meta:
        abstract = True
