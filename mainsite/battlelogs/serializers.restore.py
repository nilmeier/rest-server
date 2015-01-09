from django.shortcuts import render
from django.forms import widgets
from rest_framework import serializers
from battlelogs.models import Player, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User                             
                                    
class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.Field(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='player-highlight', format='html')

    class Meta:
        model = Player
        fields = ('url', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')
		


    def create(self, validated_attrs):
        """
        Create and return a new `Player` instance, given the validated data.
        """
        return Player.objects.create(**validated_attrs)

    def update(self, instance, validated_attrs):
        """
        Update and return an existing `Player` instance, given the validated data.
        """
        instance.title = validated_attrs.get('title', instance.title)
        instance.code = validated_attrs.get('code', instance.code)
        instance.linenos = validated_attrs.get('linenos', instance.linenos)
        instance.language = validated_attrs.get('language', instance.language)
        instance.style = validated_attrs.get('style', instance.style)
        instance.save()
        return instance



class UserSerializer(serializers.HyperlinkedModelSerializer):
    battlelogs = serializers.HyperlinkedRelatedField(many=True, view_name='battlelog-detail')

    class Meta:
        model = User
        fields = ('url', 'username', 'players')

