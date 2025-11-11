from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Leitura, Alerta
from .serializers import LeituraSerializer, AlertaSerializer
from django.utils import timezone
from datetime import timedelta


class LeituraViewSet(viewsets.ModelViewSet):
    queryset = Leitura.objects.all()
    serializer_class = LeituraSerializer

    @action(detail=False, methods=['get'])
    def ultima(self, request):
        # Retorna a última leitura
        leitura = Leitura.objects.first()
        if leitura:
            serializer = self.get_serializer(leitura)
            return Response(serializer.data)
        return Response({'Erro': 'Nenhuma leitura encontrada'})

    @action(detail=False, methods=['get'])
    def ultimas_24h(self, request):
        # Retorna leituras das últimas 24 horas
        agora = timezone.now()
        vinte_quatro_horas_atras = agora - timedelta(hours=24)
        leituras = Leitura.objects.filter(data__gte=vinte_quatro_horas_atras)
        serializer = self.get_serializer(leituras, many=True)
        return Response(serializer.data)


class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer

    @action(detail=False, methods=['get'])
    def nao_lido(self, request):
        # Retorna alertas não lidos
        alertas = Alerta.objects.filter(lido=False)
        serializer = self.get_serializer(alertas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def marcar_lido(self, request, pk=None):
        # Marcar alerta como lido
        alerta = self.get_object()
        alerta.lido = True
        alerta.save()
        serializer = self.get_serializer(alerta)
        return Response(serializer.data)
