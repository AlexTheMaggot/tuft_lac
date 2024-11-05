from django.db import models


class Machine(models.Model):
    name = models.CharField(max_length=20, unique=True)