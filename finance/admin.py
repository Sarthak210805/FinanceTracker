from django.contrib import admin
from .models import Goal, Transaction

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Goal)

