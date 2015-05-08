from django.db import models
from caspy import closure

class Thing(models.Model):
    "Dummy model used for testing closure table"
    name = models.CharField(max_length=10)
    tgroup = models.IntegerField()

    objects = models.Manager()
    tree = closure.TreeManager()

    def __str__(self): return self.name

ThingPath = closure.path_model(Thing)
