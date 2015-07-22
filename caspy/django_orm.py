from .domain import models as domain_models
from . import models as django_models

django_m = {}
domain_m = {}


def register(adaptor_class):
    adaptor = adaptor_class()
    django_m[adaptor.django_model] = adaptor
    domain_m[adaptor.domain_model] = adaptor
    return adaptor_class


def domain_to_orm(obj):
    return domain_m[obj.__class__].to_orm(obj)


def orm_to_domain(obj):
    return django_m[obj.__class__].to_domain(obj)


class BaseAdaptor:
    def to_orm(self, obj):
        kwargs = obj.dict()
        return self.django_model(**kwargs)

    def to_domain(self, instance):
        kwargs = {f: getattr(instance, f) for f in self.domain_model._fields}
        return self.domain_model(**kwargs)


@register
class CurrencyAdaptor(BaseAdaptor):
    django_model = django_models.Currency
    domain_model = domain_models.Currency


@register
class BookAdaptor(BaseAdaptor):
    django_model = django_models.Book
    domain_model = domain_models.Book


@register
class AccountTypeAdaptor(BaseAdaptor):
    django_model = django_models.AccountType
    domain_model = domain_models.AccountType


@register
class AccountAdaptor(BaseAdaptor):
    django_model = django_models.Account
    domain_model = domain_models.Account

    def to_orm(self, obj):
        instance = self.django_model(
                            account_id=obj.account_id,
                            name=obj.name,
                            book_id=get_field(obj.book),
                            account_type_id=get_field(obj.account_type),
                            currency_id=get_field(obj.currency),
                            description=obj.description,
                        )
        instance.path = obj.path
        instance.parent_id = obj.parent_id
        return instance

    def to_domain(self, instance):
        return self.domain_model(
                            account_id=instance.account_id,
                            name=instance.name,
                            book=instance.book_id,
                            account_type=instance.account_type_id,
                            currency=instance.currency_id,
                            description=instance.description,
                            parent_id=getattr(instance, 'parent_id', None),
                            path=getattr(instance, 'path', None),
                        )


@register
class TransactionAdaptor(BaseAdaptor):
    django_model = django_models.Transaction
    domain_model = domain_models.Transaction

    def to_orm(self, obj):
        return self.django_model(
                        transaction_id=obj.transaction_id,
                        date=obj.date,
                        description=obj.description,
                    )

    def to_domain(self, instance):
        return self.domain_model(
                        transaction_id=instance.transaction_id,
                        date=instance.date,
                        description=instance.description,
                    )


@register
class SplitAdaptor(BaseAdaptor):
    django_model = django_models.Split
    domain_model = domain_models.Split


def get_field(obj, field_name=None):
    if not isinstance(obj, domain_models.Base):
        return obj
    if field_name is not None:
        return getattr(obj, field_name)
    return getattr(obj, obj._fields[0])
