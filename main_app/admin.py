from django.contrib import admin
from .models import Vinyl, Listens, Turntable, Photo

# Register your models here.
admin.site.register(Vinyl)
admin.site.register(Listens)
admin.site.register(Turntable)
admin.site.register(Photo)