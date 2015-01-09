from django.shortcuts import render
from django.forms import widgets
from rest_framework import serializers
from battlelogs.models import Player, Battlelog
from django.contrib.auth.models import User                             

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    # Serialization class for Players
    owner = serializers.Field(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='player-highlight', format='html')

     
    class Meta:
        model = Player
 
        fields=('url','owner',
                 'id','first','last','nickname','wins','losses','winstreak','created','lastseen')		

        read_only_fields=('wins','losses','winstreak')        

    def create(self, validated_attrs):
        """
        Create and return a new `Player` instance, given the validated data.
        """
        return Player.objects.create(**validated_attrs)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.HyperlinkedRelatedField(many=True, view_name='user-list')
    class Meta:
        model = User
        fields = ('url', 'username', 'players')

class BattlelogSerializer(serializers.HyperlinkedModelSerializer):

    battlelogs = serializers.HyperlinkedIdentityField(view_name='battlelog-detail', format='html')
    class Meta:
        model = Battlelog
        fields=('url', 'attacker','defender','winner','start','end',
        'created','lastseen')		

    def create(self, validated_attrs):
        """
        Create and return a new `Player` instance, given the validated data.
        """
        return Battlelog.objects.create(**validated_attrs)
