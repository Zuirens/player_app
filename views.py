from rest_framework.viewsets import ModelViewSet
from player_app.serializers import AuthenUserSerializer, AnonyVisitorSerializer, MessageSerializer, CensorWordSerializer, StreamStatisticSerializer
from player_app.models import AuthenUser, AnonyVisitor, Message, CensorWord, StreamStatistic

from django.shortcuts import render
def index(request):
    return render(request, 'index.html', locals())



class AuthenUserViewSet(ModelViewSet):
    queryset = AuthenUser.objects.all()
    serializer_class = AuthenUserSerializer


class AnonyVisitorViewSet(ModelViewSet):
    queryset = AnonyVisitor.objects.all()
    serializer_class = AnonyVisitorSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class CensorWordViewSet(ModelViewSet):
    queryset = CensorWord.objects.all()
    serializer_class = CensorWordSerializer


class StreamStatisticViewSet(ModelViewSet):
    queryset = StreamStatistic.objects.all()
    serializer_class = StreamStatisticSerializer
