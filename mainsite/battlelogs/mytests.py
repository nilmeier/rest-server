from django.utils import timezone
from models import Battlelog,Player; 


#b=Battlelog.objects.all()
#p=Player.objects.all()




from rest_framework.test import APIClient


now=timezone.now()
wrong_year=now.year+1 #adding 1 year to today's date for bad dates
json_string='{"attacker":"http://0.0.0.0:8000/players/5/",\
              "defender":"http://0.0.0.0:8000/players/7/",\
              "winner":"defender", \
              "start":"2014-11-29T01:20:51.122Z",\
              "end":"'+str(wrong_year)+'-11-29T01:19:51.122Z"}'    #date is in future (2015)


json_string='{"attacker":"http://0.0.0.0:8000/players/5/",\
              "defender":"http://0.0.0.0:8000/players/7/",\
              "winner":"defender", \
              "start":"2014-11-29T01:20:51.122Z",\
              "end":"'+str(wrong_year)+'-11-29T01:19:51.122Z"}'    #date is in future (2015)
              
              
client=APIClient()
#client.login(username='hagrid',password='hagrid')
request=client.post('/battlelogs/',json_string,content_type='application/json')
error_msg='{"msg": ["(end) Battle must end before present."]}'
print (error_msg==request.content)



