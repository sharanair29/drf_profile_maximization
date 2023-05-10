from django.db import models

# Create your models here.


class Contracts(models.Model):
    name = models.CharField(max_length=65)
    start = models.BigIntegerField()
    duration = models.BigIntegerField()
    price = models.BigIntegerField()

    def __str__(self):
        return self.name
