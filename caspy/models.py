from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=8, primary_key=True, db_column='currency_code')
    shortcut = models.CharField(max_length=1)
    symbol = models.CharField(max_length=24)
    long_name = models.CharField(max_length=128)

    def __str__(self):
        return self.code
