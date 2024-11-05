from django.db import models


class Machine(models.Model):
    name = models.CharField(max_length=20, unique=True)


class State(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Record(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    states = models.ManyToManyField(State, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
