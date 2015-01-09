#shortcut to load database with players.json
import sys
import os

#usage:  load_players.py POST username start stop
#POST is a new entry
#username is one of the superusers (hagrid,dumbledore)
#line start,stop are the line numbers to range through
# when processing players.json

api_type=sys.argv[1]  
user=sys.argv[2]
if (len(sys.argv)>=5):
    line_start=int(sys.argv[3])
    line_stop=int(sys.argv[4])
else: line_start=1;line_stop=1e4
            
user_password=user  #currently set to user for all cases
post_to_address='http://0.0.0.0:8000/players/'


# adding post_type specific portion of prefix
if (api_type=='POST'):
    prefix  = 'curl -X POST '
    filename=open('scripts/players.json','r')
if (api_type=='PUT'):
    prefix  = 'curl -X PUT '
    filename=open('scripts/updates.json','r')
    post_to_address+='7/'  #wow this is really specific


# adding the rest...http and -d flag
prefix  += post_to_address + " -d "+ "'"

# postfix (after json text) tells api the type, and uses login    
postfix = "'" + ' -H "Content-Type: application/json"'
postfix += " -u "+user+":"+user_password 

startflag=False
for i,line in enumerate(filename,start=1):
    #print i
    if (i==line_start):
        startflag=True
    if startflag:
        command_string =prefix + line.strip()+ postfix
        print('line '+ str(i)+ ': '+command_string)
        os.system(command_string)
    if i==line_stop: break

filename.close()        
