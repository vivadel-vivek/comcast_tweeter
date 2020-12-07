import tweepy
import yaml
import os
import csv
import sys
import time
import socket
import datetime
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def load_info():
    """ Loads info yaml file """
    try:
        with open('info.yaml') as file:
            info = yaml.load(file, Loader=yaml.FullLoader)
            print("Loaded user info:", info)
            return info
    except Exception as err:
        print("Error loading yaml file:", err)
        return


def internet(host="8.8.8.8", port=53, timeout=3):
    """ Generates a new request"""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        return False


def current_timestamp():
    """ Get Current timestamp string """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def str_to_date(timestamp):
    """ Convert timestamp string to date object """
    return datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")


def secs_to_min(secs):
    """ Convert seconds to second and minutes
    Format : HH:MM:SS
    """
    # return str(datetime.timedelta(seconds=secs))
    return int(round(float(secs)/60))


def record_file_exist():
    """ Check if records file exist """
    return os.path.isfile('data.csv')


def create_record_file():
    """ Create a new record file """
    with open('data.csv', 'a') as csvfile:
        columns = ['timestamp', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()


def last_record_status():
    """ Get last record """
    result = None
    with open('data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result = row
    return None if result is None else result['status']


def write_record(status):
    """ Create a new record """
    with open('data.csv', 'a') as csvfile:
        columns = ['timestamp', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writerow(
            {'timestamp': str(current_timestamp()), 'status': status})


def get_total_downtime():
    """ Calculate downtime """
    seconds = 0
    down = None
    up = None
    with open('data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for record in reader:
            try:
                if record['status'] is '0':
                    print('Went Down at : ', record['timestamp'])
                    down = str_to_date(record['timestamp'])
                    next_record = next(reader)
                    up = str_to_date(next_record['timestamp'])
                    seconds += (up - down).total_seconds()
                    print('Went up at   : ', next_record['timestamp'])
            except Exception as ex:
                print('\nCurrent Status    :  Still Down')
                seconds += (str_to_date(current_timestamp()) -
                            down).total_seconds()
    return secs_to_min(seconds)


def get_downtime_by_week():
    """ Calculate downtime in past week"""
    seconds = 0
    down = None
    up = None
    with open('data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for record in reader:
            try:
                if record['status'] is '0':
                    print('Went Down at : ', record['timestamp'])
                    down = str_to_date(record['timestamp'])
                    next_record = next(reader)
                    up = str_to_date(next_record['timestamp'])
                    # check within 1 week
                    now = datetime.now()
                    if now - timedelta(hours=(24*7)) <= up:
                        # if within one week from now, add to tally
                        seconds += (up - down).total_seconds()
                        print('Went up at   : ', next_record['timestamp'])
                    else:
                        break
            except Exception as ex:
                print("downtime by week exception", ex)
                # print('\nCurrent Status    :  Still Down')
                # seconds += (str_to_date(current_timestamp()) -
                #             down).total_seconds()
    return secs_to_min(seconds)


def watch_and_tweet(api, info):
    """ Start monitoring """
    print('Monitoring your connection and tweeting to comcast as necessary')
    while True:
        last_record = last_record_status()
        if not internet():
            if last_record is '1' or last_record is None:
                print('Internet went down')
                write_record(0)
        else:
            if last_record is '0':
                print('Internet is up')
                write_record(1)
                # if our internet recovers, we want to tweet at comcast
                message = info["Custom_Message"]
                down_mins_this_week = get_downtime_by_week()
                # calculate our refund based on 43,805 minutes per month
                comcast_rate_per_minute = round(
                    info["Monthly_Comcast_Payment"]/43805)
                refund = comcast_rate_per_minute * down_mins_this_week
                tweet_content = 'Hey @comcast! {} My internet has been out for {} minutes this week. Based on my monthly payment, you owe me a refund of ${}.'.format(
                    message, down_mins_this_week, refund)
                print(tweet_content)
                api.update_status(tweet_content)
            elif last_record is None:
                print('Internet is up, but the file just started. Not tweeting just yet!')
                write_record(1)
        time.sleep(60)


# run our bot
if __name__ == "__main__":
    # install non-standard dependencies as needed
    install("tweepy")
    install("pyyaml")

    if not record_file_exist():
        create_record_file()

    # load user info
    user_info = load_info()

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(
        user_info["API_key"], user_info["API_secret_key"])
    auth.set_access_token(
        user_info["Access_token"], user_info["Access_token_secret"])

    # Create API object
    twitter_api = tweepy.API(auth)

    # start monitor
    watch_and_tweet(twitter_api, user_info)
