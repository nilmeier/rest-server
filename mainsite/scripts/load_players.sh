 # for reference: 
echo "enter hagrid's password:  (usually hagrid)" 
python manage.py createsuperuser --username hagrid --email hagrid@hogwarts.com
echo "enter dumbledore's password: (usually dumbledore)"
python manage.py createsuperuser --username dumbledore --email dumbledore@hogwarts.com

## loading player database
echo "loading players"
echo "hagrid's players"
python scripts/load_players.py POST hagrid 1 3 > scripts/load_players.log

echo "dumbledore's players"
python scripts/load_players.py POST dumbledore 4 7 > tmp.log
cat tmp.log >> scripts/load_players.log
rm tmp.log

