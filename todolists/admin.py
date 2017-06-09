from django.contrib import admin
from .models import Tag, Tasklist, Task

admin.site.register(Tag)
admin.site.register(Tasklist)
admin.site.register(Task)
# Register your models here.
