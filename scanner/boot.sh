python3 manage.py migrate --check

# check for unapplied migrations
if [ $? -ne 0 ]
then
  python3 manage.py migrate


  # check for a good exit
  if [ $? -ne 0 ]
  then
    # something went wrong; convey that and exit
    exit 1
  fi

fi

gunicorn --workers=1 --bind=0.0.0.0:8080 scanner.wsgi:application

