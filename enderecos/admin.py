from django.contrib import admin
from .models import Cidade, Endereco, Estado
# Register your models here.
admin.site.register(Endereco)
admin.site.register(Estado)
admin.site.register(Cidade)