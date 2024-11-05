from django.db import models


class Machine(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Record(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    states = models.ManyToManyField(State)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.datetime)
