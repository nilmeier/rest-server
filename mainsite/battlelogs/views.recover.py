from battlelogs.models import Player,Battlelog
from battlelogs.serializers import PlayerSerializer, UserSerializer,BattlelogSerializer
from django.contrib.auth.models import User
from rest_framework import permissions, generics
from rest_framework import viewsets,renderers
from battlelogs.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import detail_route
from django.utils import timezone

from django.db.models import Q

class PlayerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

 
    def UpdateWinLossRecord(queryset):
        """
        Counting total wins, losses, and winning streak.  Winning as an attacker
        as well as a defender both count as wins.  
        """
        b = Battlelog.objects.all()
        for i_rec, line in enumerate(queryset):
            """
            Counting total wins, losses, and winning streak.  Winning as an attacker
            as well as a defender both count as wins.  
            """
            # Counting both types of victories
            wins=b.filter(attacker__id=line.id,winner='attacker').count()
            wins+=b.filter(defender__id=line.id,winner='defender').count()
            losses=b.filter(attacker__id=line.id,winner='defender').count()
            losses+=b.filter(defender__id=line.id,winner='attacker').count()

            # Computing winnning streak.
            battlerecord=b.filter(Q(attacker__id=line.id)|Q(defender__id=line.id)) 
            winstreak=0
            for battle in battlerecord.order_by('-end'):
                #t1 is True if the player as attacker loses
                t1=battle.attacker.id==line.id and battle.winner=='defender'
                #t2 is True is the player as defender loses
                t2=battle.defender.id==line.id and battle.winner=='attacker'
                #t3 is True is the player is battling himself...
                #right now, it is error handling.
                t3=battle.defender.id==battle.attacker.id
                
                if  not t3 and (t1 or t2) :
        #           print str(t1)+" "+str(t2)+" "+str(t3)
        #           print "loss for===> " + str(line)+" <===!!!!!!!"
                   break
                winstreak+=1
            #print str(winstreak) +"  consecutive wins"


            queryset[i_rec].wins=wins
            queryset[i_rec].losses=losses
            queryset[i_rec].winstreak=winstreak
            queryset[i_rec].save()

    # this will likely not scale to extremely large battlelogs without additional optimization. but it 
    UpdateWinLossRecord(queryset)

    def get_queryset(self):
            """
            Optionally restricts the returned purchases to a given user,
            by filtering against a `username` query parameter in the URL.
            """
            queryset = Player.objects.all()
            nickname_q = self.request.QUERY_PARAMS.get('nickname', None)
            if nickname_q is not None:
                queryset = queryset.filter(nickname__contains=nickname_q)
            return queryset   


    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        Player = self.get_object()
        return Response(Player.highlighted)

    def pre_save(self, obj):
        obj.owner = self.request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BattlelogViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Battlelog.objects.all()
    serializer_class = BattlelogSerializer

    def get_queryset(self):
       """
       Optionally restricts the returned purchases to a given user,
       by filtering against a `username` query parameter in the URL.
       """
       queryset = Battlelog.objects.all()
       end_low   = self.request.QUERY_PARAMS.get('start', None)
       end_high  = self.request.QUERY_PARAMS.get('end',None)
       
       if end_low is not None:
           """ using entry values as bracket for end date in 
           battlelogs"""
           if end_high is None:  #defaults to present if no entry
               end_high=timezone.now()
           queryset = queryset.filter(end__range=(end_low,end_high))

       return queryset   







#@api_view(('GET',))
#def api_root(request, format=None):
#    return Response
#    queryset = Battlelog.objects.all()
#    serializer_class = BattlelogSerializer
#

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'players': reverse('player-list', request=request, format=format),
        'battlelogs':  reverse('battlelog-list', request=request, format=format)
    })




