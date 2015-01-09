# setup instructions from a stack overflow discussion:
http://stackoverflow.com/questions/8023126/

# First you'll need stunnel which can be downloaded here or may be provided by your platform's package system (e.g.: apt-get install stunnel). I'll be using version 4 of stunnel (e.g.: /usr/bin/stunnel4 on Ubuntu), version 3 will also work, but has different configuration options.
# First create a directory in your Django project to hold the necessary configuration files and SSLish stuff.

mkdir stunnel
cd stunnel

# Next we'll need to create a local certificate and key to be used for the SSL communication. For this we turn to openssl.
# Create the key:

openssl genrsa 1024 > stunnel.key

# Create the certificate that uses this key (this will ask you a bunch of information that will be included in the certficate - just answer with whatever feels good to you):

openssl req -new -x509 -nodes -sha1 -days 365 -key stunnel.key > stunnel.cert

# Now combine these into a single file that stunnel will use for its SSL communication:

cat stunnel.key stunnel.cert > stunnel.pem
Create a config file for stunnel called dev_https with the following contents:

pid=

cert = stunnel/stunnel.pem
sslVersion = SSLv3
foreground = yes
output = stunnel.log

[https]
accept=8443
connect=8001
TIMEOUTclose=1
# This file tells stunnel what it needs to know. Specifically, you're telling it not to use a pid file, where the certificate file is, what version of SSL to use, that it should run in the foreground, where it should log its output, and that it should accept connection on port 8443 and shuttle them along to port 8001. The last parameter (TIMEOUTclose) tells it to automatically close the connection after 1 second has passed with no activity.


# need to change permissions
chmod 600 stunnel/stunnel.pem


# Now pop back up to your Django project directory (the one with manage.py in it):

cd ..

# Here we'll create a script named runserver that will run stunnel and two django development servers (one for normal connections, and one for SSL connections):

stunnel4 stunnel/dev_https &
python manage.py runserver&
HTTPS=1 python manage.py runserver 8001
Let's break this down, line-by-line:

Line 1: Starts stunnel and point it to the configuration file we just created. This has stunnel listen on port 8443, wrap any connections it receives in SSL, and pass them along to port 8001
Line 2: Starts a normal Django runserver instance (on port 8000)
Line 3: Starts another Django runserver instance (on port 8001) and configures it to treat all incoming connections as if they were being performed using HTTPS.
Make the runscript file we just created executable with:

chmod a+x runserver
Now when you want to run your development server just execute ./runserver from your project directory. To try it out, just point your browser to http://localhost:8000 for normal HTTP traffic, and https://localhost:8443 for HTTPS traffic. Note that you're browser will almost definitely complain about the certificate used and require you to add an exception or otherwise explicitly instruct the browser to continue browsing. This is because you created your own certificate and it isn't trusted by the browser to be telling the truth about who it is. This is fine for development, but obviously won't cut it for production.

Unfortunately, on my machine this runserver script doesn't exit out nicely when I hit Ctrl-C. I have to manually kill the processes - anyone have a suggestion to fix that?
