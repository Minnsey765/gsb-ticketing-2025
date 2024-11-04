AWS bit

buy tickets

- assigned a ticket to a person
- assigns a debt to the ticket assignment
  -- different debt based on which college etc
- user gets an invoice/recipt
- information stored in a spreadsheet

post-processing

- parse spreadsheet
  -- create a spreadsheet per college

TODO

- check what college you are in
  -- from cambridge?
  --- which college?
  a

Setup

- ( del gsb_db.db)
- create the empty database
  -- python3 ./manage.py migrate
- populate the lookup tables
  -- ./import_fixtures.ps1
- create super user
  -- python3 ./manage.py createsuperuser
  --- Seems to be an issue with setting the password

Delete /admin/login.html
-- access to /admin console and actions
