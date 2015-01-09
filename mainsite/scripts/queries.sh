#testing nickname search
curl -X GET http://0.0.0.0:8000/players/?nickname=bug

# testing date search 
curl -X GET http://0.0.0.0:8000/battlelogs/?start=2014-12-09T0:00&end=2014-12-10T11:59


