# 1- fear & greed indicator 
import requests
import numpy as np

def fearngreed_today_ratio(period):
    try:
        int(period)
    except:
        print('Wrong arguments passed')
        return None

    url = 'https://api.alternative.me/fng/?limit='
    url += str(period)
    response = requests.get(url).json()

    fearngreed_data = response['data']

    fearngreed_values = []
    for row in fearngreed_data:
        fearngreed_values.append(int(row['value']))

    return fearngreed_values[0]/np.mean(fearngreed_values)



