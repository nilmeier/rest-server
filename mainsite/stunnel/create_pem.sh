#export OPENSSL_CONF=/usr/lib/ssl/openssl.cnf
#openssl genrsa 1024 > stunnel.key
#openssl req -new -x509 -nodes -sha1 -days 365 -key stunnel.key > stunnel.cert
#cat stunnel.key stunnel.cert > stunnel.pem


#alternative method
export OPENSSL_CONF=/usr/lib/ssl/openssl.cnf
openssl req -new -days 365 -nodes -out newreq.pem -keyout stunnel.pem
