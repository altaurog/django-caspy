from django.db import models
from django.utils import timezone

class Currency(models.Model):
    code = models.CharField(max_length=8, primary_key=True, db_column='currency_code')
    shortcut = models.CharField(max_length=1)
    symbol = models.CharField(max_length=24)
    long_name = models.CharField(max_length=128)

    def __str__(self):
        return self.code

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        super(Book, self).save(*args, **kwargs)
