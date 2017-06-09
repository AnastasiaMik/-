from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.name)

class Tasklist(models.Model):
    name = models.CharField(max_length=200, blank=True)
    owner = models.ForeignKey(User)

    def __str__(self):
        return "{}".format(self.name)

class Task(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    date_modified = models.DateField(auto_now=True)
    tags = models.ManyToManyField(Tag)


    PRIORITY = (
        ('h', 'High'),
        ('m', 'Medium'),
        ('l', 'Low'),
        ('n', 'None')
    )

    priority = models.CharField(max_length=1, choices=PRIORITY, default='n')
    tasklist = models.ForeignKey(Tasklist, related_name='tasks', on_delete=models.CASCADE)

# Create your models here.

    def __str__(self):
        return "{}".format(self.name)

