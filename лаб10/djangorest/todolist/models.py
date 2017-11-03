from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return "{}".format(self.name)


class TaskList(models.Model):

    name = models.CharField(max_length=200, blank=True)
    owner = models.ForeignKey('auth.User', related_name='owner')
    friend = models.CharField(max_length=200, default='')
    shared = models.ManyToManyField(User, blank=True)


    def __str__(self):
        return "{}".format(self.name)


class Task(models.Model):

    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    date_modified = models.DateField(auto_now=True)
    tags = models.ManyToManyField('Tag', related_name='tasks')

    tasklist = models.ForeignKey(TaskList, related_name='tasks', on_delete=models.CASCADE)

    PRIORITY = (
        ('h', 'High'),
        ('m', 'Medium'),
        ('l', 'Low'),
        ('n', 'None')
    )

    priority = models.CharField(max_length=1, choices=PRIORITY, default='n')

    def __str__(self):
        return "{}".format(self.name)


from datetime import date

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=date.today())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = u'User profiles'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)




