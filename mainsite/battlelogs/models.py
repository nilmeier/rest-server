from django.db import models
from pygments.lexers import get_all_lexers,get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from django.forms import SplitDateTimeField
from django.core.exceptions import ValidationError
from django.utils import timezone


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())
WINNER_CHOICES=(('attacker','attacker'),('defender','defender'))

class Player(models.Model):
    first    = models.CharField(max_length=100, blank=True, default='')
    last     = models.CharField(max_length=100, blank=True, default='')
    nickname = models.CharField(max_length=100, blank=True, unique=True,default='')
    wins=models.IntegerField(default=0)
    losses=models.IntegerField(default=0)
    winstreak=models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    lastseen= models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='players')
    highlighted = models.TextField()

    def __str__(self):
       print_string=self.first + " "+ self.last+ " ("+self.nickname+")"
       return print_string
    
    class Meta:
        ordering = ('created',)
    
    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code battlelog.
        """
        super(Player, self).save(*args, **kwargs)


class Battlelog(models.Model):

    def clean(self):
       if (self.start>self.end):
           raise ValidationError({'msg':'(end) Battle must end after start time.'})
                 #str(end.time()) + ' date: '+str(end.date()) )
       now=timezone.now()

       if (self.end>now):
           raise ValidationError({'msg':'(end) Battle must end before present.'})
       if (self.attacker==self.defender):
           raise ValidationError( {'msg': '(attacker/defender) pair should be different'} )    


    
    attacker = models.ForeignKey(Player,related_name='attacker')
    defender = models.ForeignKey(Player,related_name='defender')
    winner   = models.CharField(max_length=100, choices=WINNER_CHOICES)

    start = models.DateTimeField()
    end   = models.DateTimeField()    
    created = models.DateTimeField(auto_now_add=True)
    lastseen= models.DateTimeField(auto_now=True)


    def __str__(self):
      print_string=str(self.attacker)+ " vs. "+ str(self.defender)
      return print_string
    
    class Meta:
        ordering = ('created',)
