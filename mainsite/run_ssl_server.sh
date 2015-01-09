echo "launching stunnel and server"
stunnel4 stunnel/dev_https &
HTTPS=on python manage.py runserver 0.0.0.0:8003
echo ""
echo "killing stunnel4 (all versions) on exit"

pkill stunnel4 
