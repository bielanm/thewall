from django.db import models

class WorkExpenseModel(models.Model):
    profile = models.IntegerField()
    day = models.IntegerField()
    ice = models.IntegerField()
