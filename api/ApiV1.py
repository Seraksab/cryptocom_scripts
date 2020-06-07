import urllib
import urllib.parse
import requests
import hashlib
import time


def get_timestamp():
    ts = "%d" % int(round(time.time() * 1000))
    return ts


class ApiV1:
    def __init__(self, key, sec):
        self.timeout = 1000
        self.apiurl = "https://api.crypto.com"
        self.apikey = key
        self.apisec = sec
        return

    def http_get(self, url, params):
        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }
        data = urllib.parse.urlencode(params or {})
        try:
            response = requests.get(url, data, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                return {"code": -1, "msg": "response status:%s" % response.status_code}
        except Exception as e:
            print("httpGet failed, detail is:%s" % e)
            return {"code": -1, "msg": e}

    def http_post(self, url, params):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
        }
        data = urllib.parse.urlencode(params or {})
        try:
            response = requests.post(url, data, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                return {"code": -1, "msg": "response status:%s" % response.status_code}
        except Exception as e:
            print("httpPost failed, detail is:%s" % e)
            return {"code": -1, "msg": e}

    def api_key_get(self, url, params):
        if not params:
            params = {}
        params["api_key"] = self.apikey
        params["time"] = get_timestamp()
        params["sign"] = self.create_sign(params)
        return self.http_get(url, params)

    def api_key_post(self, url, params):
        if not params:
            params = {}
        params["api_key"] = self.apikey
        params["time"] = get_timestamp()
        params["sign"] = self.create_sign(params)
        return self.http_post(url, params)

    def create_sign(self, params):
        sorted_params = sorted(params.items(), key=lambda d: d[0], reverse=False)
        s = "".join(map(lambda x: str(x[0]) + str(x[1] or ""), sorted_params)) + self.apisec
        h = hashlib.sha256(s.encode('utf-8'))
        return h.hexdigest()

    def depth(self, sym):
        url = self.apiurl + "/v1/depth"
        params = {"symbol": sym,
                  "type": "step0"}
        return self.http_get(url, params)

    def symbols(self):
        url = self.apiurl + "/v1/symbols"
        return self.http_get(url, {})

    def balance(self):
        url = self.apiurl + "/v1/account"
        return self.api_key_post(url, {})

    def get_all_orders(self, sym):
        url = self.apiurl + "/v1/allOrders"
        params = {}
        params['symbol'] = sym
        return self.api_key_post(url, params)

    def get_order(self, sym, oid):
        url = self.apiurl + "/v1/showOrder"
        params = {}
        params['order_id'] = oid
        params['symbol'] = sym
        return self.api_key_post(url, params)

    def get_ordst(self, sym, oid):
        url = self.apiurl + "/v1/showOrder"
        params = {}
        params['order_id'] = oid
        params['symbol'] = sym
        res = self.api_key_post(url, params)
        if ('code' in res) and (res['code'] == '0') and ('order_info' in res['data']):
            return res['data']['order_info']['status']
        return -1

    def get_open_orders(self, sym):
        url = self.apiurl + "/v1/openOrders"
        params = {}
        params['pageSize'] = '200'
        params['symbol'] = sym
        return self.api_key_post(url, params)

    def get_trades(self, sym, start, end):
        url = self.apiurl + "/v1/myTrades"
        params = {}
        params['symbol'] = sym
        params['startDate'] = start
        params['endDate'] = end
        params['pageSize'] = 1000
        return self.api_key_post(url, params)

    def cancel_order(self, sym, oid):
        url = self.apiurl + "/v1/orders/cancel"
        params = {}
        params['order_id'] = oid
        params['symbol'] = sym
        return self.api_key_post(url, params)

    def cancel_order_all(self, sym):
        url = self.apiurl + "/v1/cancelAllOrders"
        params = {}
        params['symbol'] = sym
        return self.api_key_post(url, params)

    def create_order(self, sym, side, prx, qty):
        """
            s:return:
        """
        url = self.apiurl + "/v1/order"
        params = {}
        params['price'] = prx
        params['side'] = side
        params['symbol'] = sym
        params['type'] = 1
        params['volume'] = qty
        return self.api_key_post(url, params)
