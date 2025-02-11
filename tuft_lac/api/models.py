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
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='records')
    states = models.ManyToManyField(State, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return str(self.datetime)

    def get_states(self):
        return ', '.join([state.name for state in self.states.all()])
