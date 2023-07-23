from django.contrib import admin

from .models import Contribuyente, ContribuyenteAdmin

admin.site.register(Contribuyente, ContribuyenteAdmin)
