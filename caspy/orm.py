from .domain import models as dm
from . import models as om


relations = {
    'Account': ('book', 'currency', 'account_type'),
}


def domain_to_orm(obj):
    """
    Convert a lightweight business obj to django ORM.
    Assume the class and attribute names are the same.
    """
    name = obj.__class__.__name__
    klass = getattr(om, name)
    kwargs = dto(obj, relations.get(name, []))
    return klass(**dict(kwargs))


def dto(obj, relations):
    for name, val in obj._items():
        yield get_field_dto(name, relations)(name, val)


def get_field_dto(name, relations):
    return deep_field_dto if name in relations else shallow_field_dto


def shallow_field_dto(name, val):
    """Handle non-relation fields"""
    return name, val


def deep_field_dto(name, val):
    """Handle foreign-key relations on django ORM objects"""
    if isinstance(val, dm.Base):
        return name, domain_to_orm(val)
    else:
        return name + '_id', val  # assume it's an id


def orm_to_domain(instance):
    """
    Convert a django ORM instance to lightweight business obj.
    For now we just do shallow serialization, to avoid ORM
    automatically returning to the db for related objects.
    """
    name = instance.__class__.__name__
    klass = getattr(dm, name)
    data = otd(instance, klass._fields, relations.get(name, []))
    return klass(**dict(data))


def otd(instance, fields, relations):
    for f in fields:
        name = orm_attr(f, relations)
        yield f, getattr(instance, name)


def orm_attr(field, relations):
    return field + '_id' if field in relations else field
