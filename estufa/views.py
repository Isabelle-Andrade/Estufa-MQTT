from django.shortcuts import render

from rest_framework import viewsets #viewsets: classes que agrupam visualizações, como CRUD em uma única classe
from rest_framework.decorators import action #actions: ações personalizadas para criar rotas em ViewSets
from rest_framework.response import Response #response: retorna respostas HTTP formatadas
from .models import Leitura, Alerta
from .serializers import LeituraSerializer, AlertaSerializer



class  LeituraViewSet(viewsets):
    queryset = Leitura.objects.all() #Pegue dois objetos contidos em Leitura
    serializer_class = LeituraSerializer

    @action(detail=False, methods=['get'])
    def ultima(self, request):
        #retorna a última leitura
    
        leitura = Leitura.objects.first()
        if leitura:
            serializer = self.get_serializer(leitura)
            return Response (serializer.data)
        return Response({'Erro':'Nenhuma leitura encontrada'})
    
    @action(detail=False, methods=['get'])
    def ultimas_24h(self,request):
        #retorna leituras das últimas 24 horas
        from django.utils import timezone
        from datetime import timedelta #intervalo de tempo

        agora = timezone.now() #verificando o horário atual com configuração correta do fuso horário

class AlertaView(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer

    @action(detail=False, methods=['get'])
    def nao_lido (self, request):
        #retorna alertas não lidos
        alertas = Alerta.objects.filter(lido=False)
        serializer = self.get_serializer(alertas, many="True")
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def marcar_lido(self, request, pk=None):
        #Marcar alerta como lido
        alerta = self.get_object()
        alerta.lido = True
        alerta.save()
        serializer = self.get_serializer(alerta)
        return Response(serializer.data)

     

    
