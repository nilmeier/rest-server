# this is a list of instructions for installing and exploring 
# website.  Commands are listed as uncommented items, but this 
# is not a script to be run.
# To start:

# There are some caveats to the project to consider

#   - some of the responses adhere to the rest-framework 
#     defaults, rather than to the spec. 
#   - to allow for the browsable api, player ids are included
#     as a full address.  This is required for POST commands as well.
#   - Users are administrators here, and players are participants
#     in battles.
#   - The date entry fields have good validation properties, but
#     it would be nice to have dropdown dates for entries and queries in 
#     the future.
#   - ssl layer is not fully functional with curl.  https works, but
#     the authentication is currently disabled with -k flag.


#======================================================================
# Mission I:


# make sure you have django and the rest framework installed in 
# python 2.7.  

# If not, use pip to install:
pip install django 
pip install djangorestframework
pip install markdown

# Some of the shell scripts are written to run in bash shell.  The required commandline
# tools are:

openssl
curl
stunnel4

# Python has very good apis to these routines, and I can implement a full python stack at a 
# future time.



# untar mainsite directory in a convenient location 
tar -xvf mainsite.tar

# cd to mainsite.  This will be your working directory 
cd mainsite

# launch your site (in another terminal or in background)
# ...address is set to be viewable on port 8000

python manage.py runserver 0.0.0.0:8000

# you should now be able to view this either locally
# or with your external ip address.

# most of the examples here will be done without SSL.
# SSL requests are discussed later in this file.

# launch db_create.sh, located in the scripts directory:
bash -x scripts/db_create.sh battlelogs

#this script will:
# a) remove the database, if present
# b) create a new database for 'battlelogs' app

# open your browser to http://0.0.0.0:8000
# you will see a json string with 3 hyperlinks:
# players, users, and battlelogs.  clicking any of thes links will 
# open new pages with empty lists.  Let's populate these databases.  

bash -x scripts/load_players.sh

# this will create 2 administrators (called users).
# the names are hagrid and dumbledore.
# you will be prompted for administrator passwords 
# enter hagrid and dumbledore, respectively (these passwords are used in some of the scripts, so it will be easiest to stick with these)

# continuing...a script load_players.py will be called to load 
# players (via REST API) from a file called scripts/players.json:

# d) hagrid will load players 1-3
# e) dumbledore will load players 4-7

# from the homepage, browse to 'users' to see dumbledore and hagrid as users.

# returning to the homepage...browse to players, and all 7 players will be 
# listed.. the first 3 are loaded by hagrid, and the remaining players are
# loaded by dumbledore.  

# look at scripts/load_players.log for the exact curl 
# commands that were issued to load the players.

# it also lists the api response...it is slightly different from the spec...I was using the framework defaults here.


# Using PUT to update players.
# put commands can also be issued to update entries.  Look at player #7s
# nickname ("Sssslytherin in da Hayowsssss!") on the API browser.  
# We will update it using scripts/updates.json to  
# ("Ssssspecial!") using a (rather specialized) python script

python scripts/load_players.py PUT dumbledore 

# Browsing to the entry now shows the new nickname, along with an updated 'lastseen'
# field.

# now we want to enter a battlelog:
bash -x scripts/load_battlelogs.sh > scripts/load_battlelogs.log

# this will upload the battlelogs with the (admittedly finicky) 
# syntax required. the 'attacker' field is the url+playerid, 
# which is an artifact of the browsable api.
# I kept this format because the browsable api is still quite convenient
# for development.

# looking at scripts/battlelogs.log gives the api responses for 
# each of the uploads.  Mostly, it gives a response that is similar to 
# the spec.  The first line gives an error message, because we tried to 
#  have player 2 (Ron Weasley) battle himself.


# entering from the website.
# you can edit players and battlelogs from the website.  First, you must log in as either 
# hagrid or dumbledore, and then you can either add entries (from list view), or edit (from detail view)
# of either players or battlelogs tables.  To add users, you must still use  the command line:

python manage.py createsuperuser

#==========
# creating  battlelogs on the website
# attacker and defenders are foreign keys linked to the players table, which allows for a dropdown
# menu when selecting the players.  It currently lists the players, their nicknames, and the url
# The winner field is a dropdown choice that will be used.

# The date field date field is a text box, and another 
# rather finicky format that will be fixed up in the near future as well.  It will correctly
# filter for the required format, but it would be nice to have some dropdowns for this.

# battlelogs can be also pdated with PUT commands through the api.  Each battlelog has an id that is encoded in the url, much like the player id.
  
#==========
# Derived values for players.
# players can be edited through PUT commands via the api, as was shown in the example above.
# They can also be added through the website.

# Look at http://0.0.0.0:8000/players/ 
# the entries list wins, losses, and win streaks.  These are derived values.
# Harry Potter should have 15 wins, 5 losses, and a win streak of 7. 

#======================================================================
# Mission II:

#   - the /users/<userid> is changed to /players/<playerid>, since users
#     refers to the administrators (with passwords). You can browse to these
#     entries, or get them from a GET request

# for example, the command 
curl -X GET http://0.0.0.0:8000/players/1/ 

# will give the following response:
{"url": "http://0.0.0.0:8000/players/1/", "owner": "hagrid", "id": 1,"first":"Harry", "last": "Potter", "nickname": "avada suviva", "wins": 15, "losses": 5, "winstreak":7, "created": "2014-12-12T07:17:14.254Z", "lastseen": "2014-12-12T07:21:45.294Z"}

# Queries:
# querying by player nickname:

# the command line request:
curl -X GET http://0.0.0.0:8000/players/?nickname=bug

# will search for all nicknames with "bug" in the name.  
# (Colin's nickname is shutterbug) 

{"count": 1, "next": null, "previous": null, "results": [{"url": "http://0.0.0.0:8000/players/4/", "owner": "dumbledore", "id": 4, "first": "Colin", "last": "Creevey","nickname": "shutterbug", "wins": 6, "losses": 7, "winstreak": 0,"created": "2014-12-12T07:17:14.485Z", "lastseen": "2014-12-12T07:26:06.910Z"}]}

# This is a list with a count of 1.   nickname is required to be unique, but 
# we can have multiple entries matching the partial key.

# You can also enter this type of address in your browser to give the same 
# results.  At the bottom of the /players/ screen is a query box that 
# you can also use.

# querying by battlelog date range:

# let's query Harry's winning streak.
curl -X GET http://0.0.0.0:8000/battlelogs/?start=2014-12-1

# This will get all values from 12-1-2014 to the present.  The full syntax, with times 
# and end specified, is:

curl -X GET http://0.0.0.0:8000/battlelogs/?start=2014-12-1T12:00&end=2014-12-10T12:00

# both queries should give the same results.  Harry played eight games, and won 
# the last seven during this time.  This matches his winstreak stats shown on /players/1/

# There is no form as of yet to enter the date query.  I'd like to generate a nice dropdown date
# entry form here, but I ran out of time.

#==========
# Unit Tests

# both django and the rest framework have a very robust
# error handling.  I added a couple of minimal tests
# that were specific to the project.  Run the following script:
 
bash -x scripts/load_bad_battlelogs.sh > scripts/load_bad_battlelogs.log 

# and inspect the output to see the types of error messages that 
# are generated when evealuating the model.  Mostly, we are enforcing 
# chronology requirements, and also making sure players don't battle
# themselves.  Many other semantic filters could be applied here, but
# a simple set of examples is presented.

# The same set of tests are encoded in the django test framework, and 
# can be run using the django test command:

python manage.py test

# It will test 3 of the validation screens and should give an OK result.
# (the last test has not yet been implemented in battlelogs/tests.py)

# SSL (TSL) website:
# you must have openssl installed.
# To launch the https server, use the command
./run_ssl_server.sh

# This will launch a server that can be viewed on https://0.0.0.0:8002.  
# Don't background this script...it is set up to shut down the stunnel when
# you use ctrl-c. 

# Your browser will complain about not having a certificate, but you should
# eventually be able to see the site, and follow the https links.

# posting with ssl.  
# I had some issues getting the authentication to work here, but I 
# was able to disable the authentication and get it to work.  An example is
# in the shell script given here:

bash -x scripts/ssl_requests.sh

# My installation doesn't work unless I use the -k flag...if you are able to get it to work, let me know!

# Thanks...let me know what you think!
# J

