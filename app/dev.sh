#!/bin/bash

export DJANGO_SETTINGS_MODULE=settings.development

reset(){(
  echo "Resetting database"
	rm db.sqlite3
	python3 manage.py migrate
	source import_fixtures.sh
)}

for verb in "$@"; do
echo "verb: $verb"
  case "$verb" in
    reset) reset;;
  esac
done

