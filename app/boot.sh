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
  python3 manage.py loaddata ticketing/fixtures/*
  python3 manage.py createsuperuser --noinput --username om380 --email om380@cam.ac.uk


  # check for a good exit
  if [ $? -ne 0 ]
  then
    # something went wrong; convey that and exit
    exit 1
  fi

fi

gunicorn --workers=1 --bind=0.0.0.0:8080 wsgi:application
