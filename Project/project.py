import requests
import time
import argparse
from datetime import datetime

iftt_link = "https://maker.ifttt.com/trigger"
fetch_price_link = 'https://api.coindesk.com/v1/bpi/currentprice.json'
key = 'd7GMZJWMxA4dLaglzWHi6ohkROrxL6KN5mBwlEMXYV2'
# Applet for send data to twitter
twitter_applet = '{}/twitter_notifier/with/key/{}'.format(iftt_link, key)
# Applet for send data to telegram
telegram_applet = '{}/telegram_notifier/with/key/{}'.format(iftt_link, key)


# Function for fetch the price form url (GET Request)
def price():
    response = (requests.get(fetch_price_link)).json()
    value = response['bpi']['USD']['rate']
    value = float(value.replace(",", ""))
    date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    return [date, value]


# Function for Sending fetched Price to Twitter and Telegram(POST Request)
def send_data(sleepTime, lowerLimit, upperLimit):
    arr = []
    while True:
        price_update = price()
        current_price = price_update[1]
        # send prices when price falling below lower limit
        if current_price < lowerLimit:
            data = {"value1": "Emergrncy Update ==> price falling down",
                    "value2": str(price_update)[1:-1]
                    }
            requests.post(twitter_applet, json=data)
            requests.post(telegram_applet, json=data)
        # send prices when price going up above upper limit
        if current_price > upperLimit:
            data = {"value1": "Emergrncy Update ==> price going Up",
                    "value2": str(price_update)[1:-1]
                    }
            requests.post(twitter_applet, json=data)
            requests.post(telegram_applet, json=data)
        price_update = "{}: ${}".format(price_update[0], price_update[1])
        arr.append(price_update)
        # send latest five prices in time intervals
        if len(arr) == 5:
            arr = "<br>".join(arr)
            data = {"value1": "Random Update ",
                    "value2": arr
                    }
            requests.post(twitter_applet, json=data)
            requests.post(telegram_applet, json=data)
            arr = []
            return None
        time.sleep(sleepTime)


# this is is command line utility function,
# that takes the argument, parse it ans then call the run function
def main():
    parser = argparse.ArgumentParser(description="Bitcoin Notifier")
    # command line variable for time interval between prices
    parser.add_argument("-t", "--interval", type=int, nargs=1,
                        metavar="Interval", default=[2],
                        help="Time interval in seconds")
    # command line variable for Lower Limit In USD
    parser.add_argument("-l", "--lowerLimit", type=int, nargs=1,
                        metavar="Lower Limit", default=[9000],
                        help="Lower Limit In USD")
    # command line variable for Upper Limit In USD
    parser.add_argument("-u", "--upperLimit", type=int, nargs=1,
                        metavar="Upper Limit", default=[10000],
                        help="Upper Limit In USD")
    new_args = parser.parse_args()
    print('Running A Program with Interval of =',
          new_args.interval[0], "Seconds.",
          'Upper Limit =', new_args.upperLimit[0],
          'Lower Limit =', new_args.lowerLimit[0])
    # calls the run function
    send_data(new_args.interval[0],
              new_args.lowerLimit[0], new_args.upperLimit[0])


if __name__ == '__main__':
    main()
