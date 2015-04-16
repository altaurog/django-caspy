from django.db import models
from django.utils import timezone

from . import closure


class Currency(models.Model):
    cur_code = models.CharField(max_length=8, primary_key=True)
    shortcut = models.CharField(max_length=1)
    symbol = models.CharField(max_length=24)
    long_name = models.CharField(max_length=128)

    class Meta:
        unique_together = [['shortcut'], ['long_name']]

    def __str__(self):
        return self.cur_code


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField()

    def set_created_at(self):
        "Instead of auto_now_add"
        if self.created_at is None:
            self.created_at = timezone.now()

    def save(self, *args, **kwargs):
        self.set_created_at()
        super(Book, self).save(*args, **kwargs)

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


class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    book = models.ForeignKey(Book)
    account_type = models.ForeignKey(AccountType)
    currency = models.ForeignKey(Currency)
    description = models.CharField(max_length=255)

    objects = models.Manager()
    tree = closure.TreeManager()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [['name', 'book']]


AccountPath = closure.path_model(Account)
