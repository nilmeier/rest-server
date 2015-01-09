# removes database (name set in mainsite/settings.py)
#rm tmp.db
rm mainsite.db

# removes migration contents from app directory
rm -r $1/migrations

# creates "migration" of database
python manage.py makemigrations $1
python manage.py migrate

