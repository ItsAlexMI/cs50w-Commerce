from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(User)
admin.site.register(Listado)
admin.site.register(Oferta)
admin.site.register(Comentario)
admin.site.register(ListaSeguimiento)

