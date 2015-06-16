from . import models, orm


class BaseQuery:
    def __init__(self, model):
        self.qset = model.objects
        self.to_domain = orm.orm_to_domain
        self.to_orm = orm.domain_to_orm

    def all(self):
        return map(self.to_domain, self.qset.all())

    def by_pk(self, pk):
        return self.qset.filter(pk=pk)

    def get(self, pk):
        return self.to_domain(self.by_pk(pk).get())

    def save(self, obj):
        self.to_orm(obj).save()

    def delete(self, pk):
        self.by_pk(pk).delete()


currency = BaseQuery(models.Currency)
book = BaseQuery(models.Book)
accountttype = BaseQuery(models.AccountType)
