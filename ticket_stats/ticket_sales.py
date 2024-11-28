import csv
import io

import pandas as pd

kinds = {}
with open("./ticketSales.txt", 'r', encoding='utf-8') as f:
    headers = f.readline()

    for line in f.readlines():
        data = line.split(',')
        try:
            kinds[data[2]].append(data)
        except KeyError:
            kinds[data[2]] = [data]

    with pd.ExcelWriter("ticket_sales.xlsx") as writer:
        for kind in kinds.keys():
            name = "./ticketSales_" + kind + ".txt"
            buffer = io.StringIO()
            writer_csv = csv.writer(buffer)
            writer_csv.writerow(headers.split(","))
            writer_csv.writerows(kinds[kind])
            buffer.seek(0)
            content = pd.read_csv(buffer)
            content.to_excel(writer, sheet_name=kind, index=False)
