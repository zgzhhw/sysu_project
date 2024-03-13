from django.contrib import admin

# Register your models here.
from app import models

#admin.site.register(models.Person)
admin.site.disable_action('delete_selected')