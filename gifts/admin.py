from django.contrib import admin

# Register your models here.
from .models import Gift
from .models import Contribution

admin.site.register(Gift)
admin.site.register(Contribution)
