# not completely working...-k option disables verification
# it does, however, correctly post to the https address.
curl -k -E stunnel/stunnel.pem -X POST https://0.0.0.0:8002/battlelogs/ -d '{"attacker":"http://0.0.0.0:8000/players/5/","defender":"http://0.0.0.0:8000/players/7/","winner":"defender", "start":"2014-11-29T01:20:51.122Z","end":"2014-11-29T01:21:51.122Z"}' -H "Content-Type: application/json" -u hagrid:hagrid
