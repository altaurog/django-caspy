from django.db import models
from django.utils import timezone


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

    class Meta:
        ordering = ['created_at']
        unique_together = [['name']]
