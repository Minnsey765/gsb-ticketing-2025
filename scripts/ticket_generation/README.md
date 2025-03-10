# Ticket Generation
Uses a CSV file containing the following headed columns

    name,uuid,kind

with example data like:

    Julia Torres,GSBOOA65B1N,QJ

## Year Tickets

Create a new SVG file for 

- STANDARD
- QUEUE_JUMP

Name them as:

- STANDARD_{YEAR}.svg
- QUEUE_JUMP_{YEAR}.svg

## To Run

Minimum 

    python3 {csv file}

Defaults to using 2024 tickets

Set the year

    python3 {csv file}  -y {2-digit year}

Uses the _{2-digit year}.svg files.


## To Test

Use the test file

    python3 ./csv_to_svgs.py ../demo_tickets_export.csv