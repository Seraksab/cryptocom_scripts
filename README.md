# cryptocom_scripts

![GitHub](https://img.shields.io/github/license/Seraksab/cryptocom_scripts)

This repo contains various scripts for the Crypto.com exchange that i threw together because at the time there was no 
official way or function to accomplish these tasks.

## Configuration

Set your personal API key [here](api/ApiKey.py).
```python
API_KEY = "YOUR_KEY"
API_SECRET = "YOUR_KEY_SECRET"
```

## Scripts

### [ExportTradesCsv.py](scripts/ExportTradesCsv.py)

The Crypto.com Exchange API is not yet supported by CoinTracking.  
This script exports all trades within a given timeframe as a CSV file which can then be imported to 
CoinTracking or any similar site.

Example output:

```
id,time,side,amount_1,coin_1,amount_2,coin_2,fee_amount,fee_coin
659975,2020-01-15 22:49:44,BUY,445.14895656,CRO,20.47,USDT,0.89029791,CRO
659976,2020-01-15 22:49:44,BUY,23337.45973909,CRO,1073.52,USDT,46.67491947,CRO
679151,2020-01-17 10:51:40,SELL,157.958,CRO,7.42,USDT,0.31,CRO
679155,2020-01-17 10:52:05,SELL,3.38085106,CRO,0.15,USDT,0.00,CRO
```

### [GenerateCroStakingCsv.py](scripts/GenerateCroStakingCsv.py)

The Crypto.com Exchange API does not yet have an endpoint to retrieve or export the CRO staking rewards.  
This script generates a CSV with a daily entry of the gained CRO interest which can then be imported to 
CoinTracking or any similar site.

Example output:

```
datetime,coin,amount,comment
2019-12-06T00:00:00Z,CRO,5.47945205,CRO Staking Interest
2019-12-07T00:00:00Z,CRO,5.47945205,CRO Staking Interest
2019-12-08T00:00:00Z,CRO,5.47945205,CRO Staking Interest
2019-12-09T00:00:00Z,CRO,5.47945205,CRO Staking Interest
```
