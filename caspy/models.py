from django.db import models
from django.db.backends.signals import connection_created

from . import closure


def activate_foreign_keys(sender, connection, **kwargs):
    """Enable integrity constraint with sqlite."""
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')

connection_created.connect(activate_foreign_keys)


class Currency(models.Model):
    cur_code = models.CharField(max_length=8, primary_key=True)
    shortcut = models.CharField(max_length=1, null=True)
    symbol = models.CharField(max_length=24, null=True)
    long_name = models.CharField(max_length=128, null=True)

    class Meta:
        unique_together = [['shortcut'], ['long_name']]

    def __str__(self):
        return self.cur_code


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']
        unique_together = [['name']]


class AccountType(models.Model):
    account_type = models.CharField(max_length=128, primary_key=True)
    # (credits increase account balance) <=> (sign == True)
    sign = models.BooleanField(verbose_name="Credits increase balance",
                               default=False)
    credit_term = models.CharField(max_length=32)
    debit_term = models.CharField(max_length=32)

    def __str__(self):
        return self.account_type


class AccountTreeManager(closure.TreeManager):
    def path_name(self, path):
        return '::'.join([a.name for a in path])

    def path_parent(self, path):
        if len(path) > 1:
            return path[-2].account_id

    def annotate(self, path):
        account = path[-1]
        account.path = self.path_name(path)
        account.parent_id = self.path_parent(path)
        return account

    def load(self, *args, **kwargs):
        return map(self.annotate, self.paths(*args, **kwargs))

    def load_book(self, book_id):
        return self.load('WHERE book_id = %s', [book_id])

    def load_one(self, book_id, account_id):
        path = self.one_path(account_id, book=book_id)
        return self.annotate(list(path))


class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    book = models.ForeignKey(Book)
    account_type = models.ForeignKey(AccountType)
    currency = models.ForeignKey(Currency)
    description = models.CharField(max_length=255)

    objects = models.Manager()
    tree = AccountTreeManager()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [['name', 'book']]


AccountPath = closure.path_model(Account)
