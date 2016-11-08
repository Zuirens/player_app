from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from player_app.models import AuthenUser, AnonyVisitor, Message, CensorWord, StreamStatistic
from django.contrib.auth.models import User

class AuthenUserSerializer(ModelSerializer):

    class Meta:
        model = AuthenUser
        exclude = []


class AnonyVisitorSerializer(ModelSerializer):

    class Meta:
        model = AnonyVisitor


class MessageSerializer(ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'recieved_time', 'author', 'content', 'is_blacklist')


class CensorWordSerializer(ModelSerializer):

    class Meta:
        model = CensorWord
        fields = ('word',)


class StreamStatisticSerializer(ModelSerializer):

    class Meta:
        model = StreamStatistic
