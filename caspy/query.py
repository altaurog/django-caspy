from django.db import utils
from . import models, django_orm


class IntegrityError(Exception):
    pass


class BaseQuery(object):
    def __init__(self, model):
        self.model = model
        self.qset = model.objects
        self.to_domain = django_orm.orm_to_domain
        self.to_orm = django_orm.domain_to_orm

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
        instance = self.to_orm(obj)
        instance.save()
        return instance

    def delete(self, pk):
        obj = self.by_pk(pk)
        if obj is not None:
            obj.delete()
            return True


currency = BaseQuery(models.Currency)
book = BaseQuery(models.Book)
accounttype = BaseQuery(models.AccountType)


class AccountQuery(BaseQuery):
    def all(self, book_id):
        return map(self.to_domain, self.model.tree.load_book(book_id))

    def by_pk(self, book_id, account_id):
        return self.model.tree.load_one(book_id, account_id)

    def get(self, book_id, account_id):
        instance = self.by_pk(book_id, account_id)
        if instance is not None:
            return self.to_domain(instance)

    def save(self, obj):
        try:
            instance = super(AccountQuery, self).save(obj)
            self.model.tree.detach(instance)
            self.model.tree.attach(instance, obj.parent_id)
        except utils.IntegrityError as e:
            raise IntegrityError(str(e))

    def delete(self, book_id, account_id):
        instance = self.by_pk(book_id, account_id)
        if instance is not None:
            instance.delete()
            return True

account = AccountQuery(models.Account)


class TransactionQuery(BaseQuery):
    def all(self, book_id):
        qset = self._split_qset(book_id)
        return list(self._load(qset))

    def get(self, book_id, transaction_id):
        qset = self._split_qset(book_id, transaction_id)
        result = list(self._load(qset))
        if result:
            return result[0]

    def save(self, obj):
        instance = super(TransactionQuery, self).save(obj)
        models.Split.objects.bulk_create(self.splits(obj, instance))
        return instance

    def delete(self, book_id, transaction_id):
        qset = self._split_qset(book_id, transaction_id)
        splits = iter(qset.select_related('transaction'))
        next(splits).transaction.delete()

    def splits(self, obj, instance):
        for s in obj.splits:
            si = self.to_orm(s)
            si.transaction = instance
            yield si

    def _split_qset(self, book_id, transaction_id=None):
        qargs = {'account__book_id': book_id}
        if transaction_id is not None:
            qargs['transaction'] = transaction_id
        return models.Split.objects.filter(**qargs)

    def _load(self, split_qset):
        transactions = {}
        for split in split_qset.select_related('transaction'):
            try:
                xact = transactions[split.transaction_id]
            except KeyError:
                xact = self.to_domain(split.transaction)
                transactions[split.transaction_id] = xact
            xact.splits.append(self.to_domain(split))
        return transactions.values()


transaction = TransactionQuery(models.Transaction)
