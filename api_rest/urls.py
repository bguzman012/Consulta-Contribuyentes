from django.conf.urls import url
from django.urls import path, include
from .views import *

# specify URL Path for rest_framework
urlpatterns = [
    path('consultas', ContribuyenteViewSet.as_view()),
    path('migracion', MigracionViewSet.as_view()),
]