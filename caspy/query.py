from . import models, orm


class BaseQuery:
    def __init__(self, model):
        self.qset = model.objects
        self.to_domain = orm.orm_to_domain
        self.to_orm = orm.domain_to_orm

    def all(self):
        return map(self.to_domain, self.qset.all())

    def by_pk(self, pk):
        try:
            return self.qset.get(pk=pk)
        except self.qset.model.DoesNotExist:
            return None

    def get(self, pk):
        obj = self.by_pk(pk)
        if obj is not None:
            return self.to_domain(obj)

    def save(self, obj):
        self.to_orm(obj).save()

    def delete(self, pk):
        obj = self.by_pk(pk)
        if obj is not None:
            obj.delete()
            return True


currency = BaseQuery(models.Currency)
book = BaseQuery(models.Book)
accounttype = BaseQuery(models.AccountType)
