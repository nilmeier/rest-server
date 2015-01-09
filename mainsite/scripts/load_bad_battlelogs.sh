echo "faulty battlelog entry:  start > end"
curl -X POST http://0.0.0.0:8000/battlelogs/ -d '{"attacker":"http://0.0.0.0:8000/players/5/","defender":"http://0.0.0.0:8000/players/7/","winner":"defender", "start":"2014-11-29T01:20:51.122Z","end":"2014-11-29T01:19:51.122Z"}' -H "Content-Type: application/json" -u hagrid:hagrid
echo""
echo "faulty battlelog entry:  start time in future AND start > end"
curl -X POST http://0.0.0.0:8000/battlelogs/ -d '{"attacker":"http://0.0.0.0:8000/players/5/","defender":"http://0.0.0.0:8000/players/7/","winner":"defender", "start":"2015-12-29T01:20:51.122Z","end":"2014-11-29T01:19:51.122Z"}' -H "Content-Type: application/json" -u hagrid:hagrid
echo""
echo "faulty battlelog entry:  end time in future"
curl -X POST http://0.0.0.0:8000/battlelogs/ -d '{"attacker":"http://0.0.0.0:8000/players/5/","defender":"http://0.0.0.0:8000/players/7/","winner":"defender", "start":"2014-11-29T01:20:51.122Z","end":"2015-11-29T01:19:51.122Z"}' -H "Content-Type: application/json" -u hagrid:hagrid
echo""
echo "faulty battlelog entry:  battle against self"
curl -X POST http://0.0.0.0:8000/battlelogs/ -d '{"attacker":"http://0.0.0.0:8000/players/1/","defender":"http://0.0.0.0:8000/players/1/","winner":"attacker", "start":"2014-11-29T01:20:51.122Z","end":"2014-11-29T01:21:51.122Z"}' -H "Content-Type: application/json" -u hagrid:hagrid
echo""

