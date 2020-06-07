import json
import os
import time

from api.ApiKey import *
from api.ApiV1 import ApiV1

api = ApiV1(API_KEY, API_SECRET)

export_start = "2019-12-01 00:00:00"
export_end = "2020-06-01 00:00:00"


def json_pretty(string):
    return json.dumps(string, sort_keys=True, indent=2)


def to_json(string):
    return json.loads(string)


def get_all_symbols():
    symbols_data = api.symbols()
    syms = []
    for sym in symbols_data["data"]:
        syms.append([sym["symbol"], sym["base_coin"], sym["count_coin"]])
    return syms


def get_trades(sym):
    trades_data = api.get_trades(sym, export_start, export_end)
    count = trades_data["data"]["count"]
    if count <= 0:
        return []
    return trades_data["data"]["resultList"]


def get_header_csv():
    header_data = [
        "id",
        "time",
        "side",
        "amount_1",
        "coin_1",
        "amount_2",
        "coin_2",
        "amount_fee",
        "coin_fee"
    ]
    return ','.join(header_data)


def trade_to_csv(base_coin, count_coin, trade):
    csv_data = [
        trade["id"],
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(trade["ctime"]/1000)),
        trade["side"],
        trade["volume"],
        base_coin,
        trade["deal_price"],
        count_coin,
        trade["fee"],
        trade["feeCoin"]
    ]
    return ','.join(map(str, csv_data))

# print(json_pretty(api.get_trades('ethusdt', export_start, export_end)))
# exit(0)

name = "../exports/trading_export_" \
       + export_start.split()[0] \
       + "_" \
       + export_end.split()[0] \
       + ".csv"
with open(name, "w+") as file:
    print("Exporting all trades from %s to %s" % (export_start, export_end))
    print("File: %s" % os.path.basename(file.name))
    file.write(get_header_csv() + "\n")
    symbols = get_all_symbols()
    total_trades = 0
    for symbol in symbols:
        print("%s" % symbol[0].upper(), end=": ")
        trades = get_trades(symbol[0])
        total_trades += len(trades)
        print("%s trades" % len(trades))
        for trade in trades:
            csv_line = trade_to_csv(symbol[1], symbol[2], trade)
            file.write(csv_line + "\n")
            # print(csv_line)
    print("Exported %d trades" % total_trades)

