from django.contrib import admin
from django.urls import path, include
from estufa.views import LeituraViewSet, AlertaViewSet
from rest_framework import routers

router = routers.DefaultRouter() #r: rotas
router.register(r'leituras', LeituraViewSet)
router.register(r'alertas', AlertaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
