$servername = $args[0]

$env:DJANGO_SETTINGS_MODULE="settings.development"
Write-Output "DJANGO_SETTINGS_MODULE=$env:DJANGO_SETTINGS_MODULE"

function Reset-Environment {
  Write-Output "Resetting environment"
  Write-Output "Removing gsb_db.db"
  Remove-Item -Path gsb_db.db
  Write-Output "Running migrations"
	python3 manage.py migrate
  Write-Output "Importing fixtures"
	& ./import_fixtures.ps1
}

if ( $args.Count -gt 0 -And $args[0] -eq "reset" )
{
  Reset-Environment
}
else {
  Write-Output "Usage: dev.ps1 reset"
  Write-Output "      delete db.sqlite3, run migrations and load fixtures"
}


