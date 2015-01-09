from django.test import TestCase
#from rest_framework.test import APITestCase
from django.utils import timezone
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse

# a somewhat kloodgy solution to the difficulties
# in the way the urls are resolved for posts in the 
# test server.  client.post requests only work in the global
# namespace.  This is not a permanent solution, but will work 
# for the near term.  

now=timezone.now()
wrong_year=now.year+1 #adding 1 year to today's date for bad dates
json_string='{"attacker":"/players/5/",\
              "defender":"/players/7/",\
              "winner":"defender", \
              "start":"2014-11-29T01:20:51.122Z",\
              "end":"'+str(wrong_year)+'-11-29T01:19:51.122Z"}'    #date is in future (2015)

# Instead of using APITestCase in the class definitions, 
# We define the client here...not sure why this only works this way. 
client=APIClient()
request=client.post('/battlelogs/',json_string,content_type='application/json')
error_msg='{"msg": ["(end) Battle must end before present."]}'
#print request.content

#this value gets passed into the class for testing
battlelog_test_1=(error_msg==request.content)

#== faulty battlelog entry:  start > end
json_string= '{"attacker":"/players/5/",\
              "defender":"/players/7/",\
              "winner":"defender", \
              "start":"2014-11-29T01:21:51.122Z",\
              "end":"2014-11-29T01:20:50.12Z"}'    #date is in future (2015)

request=client.post('/battlelogs/',json_string,content_type='application/json')
error_msg='{"msg": ["(end) Battle must end after start time."]}'

battlelog_test_2=(error_msg==request.content)

#== faulty battlelog entry:  start time in future
# end time is checked first, then pos_delta.  If end>now, first error 
# is thrown, after that, if start>now, start>end
error_msg='{"msg": ["(end) Battle must end after start time."]}'
json_string='{"attacker":"/players/5/",\
              "defender":"/players/7/",\
              "winner":"defender", \
              "start":"'+str(wrong_year)+'-11-29T01:20:51.122Z",\
              "end":"2014-11-29T01:19:51.122Z"}'   

battlelog_test_3=(error_msg==request.content)


class BattlelogEntryTests(TestCase):
    
    def test_1_battlelog_with_future_end_time(self):
        print "\tTest 1:  future end time returns error?             "+str(battlelog_test_1)
        self.assertEqual(battlelog_test_1,True)
        
    def test_2_battlelog_with_pos_delta_t(self):
        print "\tTest 2:  end time before start time returns error?  "+str(battlelog_test_1)
        self.assertEqual(battlelog_test_2,True)
    
    def test_3_battlelog_with_bad_start_time(self):

        print "\tTest 3:  future start time returns error?           "+str(battlelog_test_3)
        self.assertEqual(battlelog_test_3,True)   
