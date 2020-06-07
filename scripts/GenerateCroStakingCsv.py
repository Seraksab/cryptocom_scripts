import datetime
import os


export_start = "2019-12-01"

staking_amount = [
    ['2019-12-06', 10000],
    ['2019-12-24', 50000],
    ['2020-05-15', 60225]
]


def get_header_csv():
    header_data = [
        "datetime",
        "coin",
        "amount",
        "comment"
    ]
    return ','.join(header_data)


def generate_entries(start_date, days, staking_amount):
    entries = ""
    daily_amount = round((staking_amount * 0.2) / 365, 8)
    for x in range(0, days):
        date = start_date + datetime.timedelta(days=x)
        csv_data = [
            date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "CRO",
            daily_amount,
            "CRO Staking Interest"
        ]
        entries += (','.join(map(str, csv_data)) + "\n")
    return entries


date_from = staking_amount[0][0]
date_to = datetime.datetime.today().strftime("%Y-%m-%d")
name = "../exports/staking_export_" + date_from + "_" + date_to + ".csv"
with open(name, "w+") as file:
    print("Generating CRO staking from %s to %s" % (date_from, date_to))
    print("File: %s" % os.path.basename(file.name))
    total_entries = 0
    file.write(get_header_csv() + "\n")
    for x in range(0, len(staking_amount)):
        d1 = datetime.datetime.strptime(staking_amount[x][0], "%Y-%m-%d")
        d2 = datetime.datetime.today() if x >= len(staking_amount) - 1 else datetime.datetime.strptime(
            staking_amount[x + 1][0], "%Y-%m-%d")
        days = abs((d2 - d1).days)
        total_entries += days
        file.write(generate_entries(d1, days, staking_amount[x][1]))
    print("Generated %d CRO staking entries" % total_entries)
