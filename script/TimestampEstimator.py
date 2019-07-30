#!/usr/bin/env	python3

import requests
from datetime import datetime
import twitter
import random
import csv
import argparse
import os
import time


'''
Generate data points for estimation of Tweet Id sand their timestamps before Snowflake
'''


def break_tweet_timeline(tolerance):
    '''
    Last timestamp found from Memento Link:
    https://web.archive.org/web/20190618182911/https://twitter.com/nytimes/status/29548970348
    We used curl bach command to find the last tweet id
    '''
    end_tweet_id = 29700859247
    start_tweet_id = 20
    list_tweets = []
    twitter_object = create_twitter_instance()
    tweet_timestamp = get_tweet_timestamp(start_tweet_id, twitter_object)
    list_tweets.append({"TweetId": start_tweet_id, "Timestamp": tweet_timestamp})
    tweet_timestamp = get_tweet_timestamp(end_tweet_id, twitter_object)
    list_tweets.append({"TweetId": end_tweet_id, "Timestamp": tweet_timestamp})
    list_tweet_ids = generate_tweet_timestamp_id(list_tweets[0], list_tweets[1], twitter_object, list_tweets, tolerance)
    write_data_points(list_tweets)


'''
Write the data points to a file
'''


def write_data_points(list_tweets):
    list_tweet_ids = []
    list_tweet_timestamps = []
    data_directory = os.path.join(os.path.dirname( __file__ ), '..', "data")
    if not os.path.exists(data_directory):
        os.mkdir(data_directory)
    for json_object in list_tweets:
        list_tweet_ids.append(json_object["TweetId"])
        list_tweet_timestamps.append(json_object["Timestamp"])
    list_tweet_timeline = []
    list_tweet_timestamps, list_tweet_ids = zip(*sorted(zip(list_tweet_timestamps, list_tweet_ids)))
    for i in range(0, len(list_tweet_ids)):
        list_tweet_timeline.append([list_tweet_ids[i], list_tweet_timestamps[i]])
    with open(os.path.join(data_directory, "TweetTimelineList.txt"), "w") as file_tweets:
        file_tweets.write(str(list_tweet_timeline))
    with open(os.path.join(data_directory, "TweetTimeline.txt"), "w") as file_tweet_timeline:
        for i in range(0, len(list_tweet_ids)):
            file_tweet_timeline.write(str(list_tweet_ids[i]) + "," + str(list_tweet_timestamps[i]) + "," +  str(datetime.utcfromtimestamp(list_tweet_timestamps[i]))+ "\n")


'''
Use divide and conquer technique to find the data points between start and end tweet ids
'''


def generate_tweet_timestamp_id(start, end, twitter_object, list_tweets, tolerance):
    if abs(end["Timestamp"] - start["Timestamp"]) <= tolerance or end["Timestamp"] < start["Timestamp"]:
        return list_tweets
    mid = int((start["TweetId"] + end["TweetId"]) / 2)
    tweet_id = get_current_tweet_id(mid, int(start["TweetId"]), int(end["TweetId"]))
    if tweet_id > 0:
        tweet_timestamp  = get_tweet_timestamp(tweet_id, twitter_object)
        mid = {"TweetId": tweet_id, "Timestamp": tweet_timestamp}
        list_tweets.append(mid)
        generate_tweet_timestamp_id(start, mid, twitter_object, list_tweets, tolerance)
        generate_tweet_timestamp_id(mid, end, twitter_object, list_tweets, tolerance)
    return list_tweets


'''
Get timestamp of any Tweet in millisconds using Twitter API
'''


def get_tweet_timestamp(tweet_id, twitter_object):
    try:
        twitter_response = twitter_object.GetStatus(tweet_id)
        tweet_date_time = datetime.strptime(twitter_response.created_at, "%a %b %d %H:%M:%S %z %Y")
        return int(tweet_date_time.timestamp())
    except Exception as e:
        print(e)
        time.sleep(300)
        get_tweet_timestamp(tweet_id, twitter_object)

'''
Get the current valid tweet id around the specified tweet id
'''


def get_current_tweet_id(tweet_id, left_limit_tweet_id, right_limit_tweet_id):
    sample_twitter_url = "https://twitter.com/jack/status/"
    step_size = 0
    data_directory = os.path.join(os.path.dirname( __file__ ), '..', "data")
    current_tweet_id = tweet_id
    counter = 0
    while current_tweet_id and left_limit_tweet_id < current_tweet_id < right_limit_tweet_id:
        response = requests.head(sample_twitter_url + str(current_tweet_id))
        if response.status_code == 200:
            return current_tweet_id
        elif response.status_code == 301 or response.status_code == 302:
            if "status/" in response.headers['location']:
                redirect_response = requests.head(response.headers['location'])
                if redirect_response.status_code == 200:
                    return int (str(response.headers['location']).split("/")[-1])
                else:
                    with open(os.path.join(data_directory, "WeirdUrls.txt"), "a+") as file_urls:
                        file_urls.write(str(current_tweet_id) + "," + response.headers['location'] + "," + str(redirect_response.status_code) + "\n")
                    return -1
            else:
                current_tweet_id += 1
        else:
            if counter < 100:
                counter += 1
                current_tweet_id += 1
            else:
                current_tweet_id += pow(2, step_size)
                step_size += 1
    step_size = 0
    counter= 0
    while tweet_id and left_limit_tweet_id < tweet_id < right_limit_tweet_id:
        response = requests.head(sample_twitter_url + str(tweet_id))
        if response.status_code == 200:
            return tweet_id
        elif response.status_code == 301 or response.status_code == 302:
            if "status/" in response.headers['location']:
                redirect_response = requests.head(response.headers['location'])
                if redirect_response.status_code == 200:
                    return int (str(response.headers['location']).split("/")[-1])
                else:
                    with open(os.path.join(data_directory, "WeirdUrls.txt"), "a+") as file_urls:
                        file_urls.write(str(current_tweet_id) + "," + response.headers['location'] + "," + str(redirect_response.status_code) + "\n")
                    return -1
            else:
                current_tweet_id += 1
        else:
            if counter < 100:
                counter += 1
                tweet_id -= 1
            else:
                tweet_id -= pow(2, step_size)
                step_size += 1
    return -1


'''
Create Twitter Instance. All the fields can be collected from the developer site of Twitter
'''


def create_twitter_instance():
    api = twitter.Api(consumer_key='5Q3CFnvq02nKj6kI9gRpGNHXH',
                      consumer_secret='4OBnuBjedjwZUZmtslwzzPmWxeQtN7LHUeYHf4jsqZjQkEyW4v',
                      access_token_key='907341293717737473-for4ikiKhPAHxD54pnRqhJSPpr1QmNB',
                      access_token_secret='jV6TplxXfCQOu8C8zArB2wzlwGisq2Y0kRHUtrvuKYQNr',
                      sleep_on_rate_limit=True)
    return api


'''
Get Tweet Timestamp post SnowFlake
2010-11-04
'''


def find_tweet_timestamp_post_snowflake(tid):
    offset = 1288834974657
    tstamp = (tid >> 22) + offset
    return tstamp


'''
Returns Tweet Timestamp for pre-Snowflake Tweets
Success: Returns the estimated timestamp of the tweet
Failure: Returns -1
'''


def find_tweet_timestamp_pre_snowflake(tid):
    data_directory = os.path.join(os.path.dirname( __file__ ), '..', "data")
    with open(os.path.join(data_directory, "TweetTimeline.txt"), "r") as file_tweet_timeline:
        prev_line_parts = file_tweet_timeline.readline().rstrip().split(",")
        if tid < int(prev_line_parts[0]):
            return -1
        elif tid == int(prev_line_parts[0]):
            return int(prev_line_parts[1]) * 1000
        else:
            for line in file_tweet_timeline:
                line_parts = line.rstrip().split(",")
                if tid == int(line_parts[0]):
                    return int(prev_line_parts[1]) * 1000
                if int(prev_line_parts[0]) < tid < int(line_parts[0]):
                    estimated_timestamp = round(int(prev_line_parts[1]) + (((tid - int(prev_line_parts[0])) / (int(line_parts[0]) - int(prev_line_parts[0]))) * (int(line_parts[1]) - int(prev_line_parts[1]))))
                    return estimated_timestamp * 1000
                else:
                    prev_line_parts = line_parts
    return -1

'''
Find timestamp of a tweet
'''


def find_tweet_timestamp(tid):
    pre_snowflake_last_tweet_id = 29700859247
    if tid < pre_snowflake_last_tweet_id:
        tweet_timestamp = find_tweet_timestamp_pre_snowflake(tid)
    else:
        tweet_timestamp = find_tweet_timestamp_post_snowflake(tid)
    return tweet_timestamp


'''
Generate test points of Tweet Ids
'''


def create_test_set(start_tweet_id, end_tweet_id, data_points=0, data_interval=0):
    list_current_test_id = []
    data_directory = os.path.join(os.path.dirname( __file__ ), '..', "data")
    with open(os.path.join(data_directory, "testset.txt"), "w") as file_test_set:
        if data_interval > 0:
            with open(os.path.join(data_directory, "TweetTimeline.txt"), "r") as file_tweets:
                list_interval_tweet_ids = []
                line_parts = file_tweets.readline().rstrip().split(",")
                week_timestamp = int(line_parts[1])
                list_interval_tweet_ids.append(int(line_parts[0]))
                temp_tweet_id = 0
                for line in file_tweets:
                    line_parts = line.rstrip().split(",")
                    if int(line_parts[1]) < week_timestamp + (data_interval * 24 * 60 * 60):
                        temp_tweet_id = int(line_parts[0])
                    else:
                        list_interval_tweet_ids.append(temp_tweet_id)
                        week_timestamp += (data_interval * 24 * 60 * 60)
            for i in range(1, len(list_interval_tweet_ids)):
                find_tweet_ids(list_interval_tweet_ids[i - 1], list_interval_tweet_ids[i], data_points, list_current_test_id, file_test_set)
        else:
            find_tweet_ids(start_tweet_id, end_tweet_id, data_points, list_current_test_id, file_test_set)


'''
Find tweet id status
'''


def find_tweet_ids(start_tweet_id, end_tweet_id, data_points, list_current_test_id, file_test_set):
    sample_twitter_url = "https://twitter.com/jack/status/"
    points = 0
    twitter_object = create_twitter_instance()
    count = 0
    while points < data_points and count < (data_points * 5):
        tweet_status = False
        current_tweet_id = random.randint(start_tweet_id, end_tweet_id)
        response = requests.head(sample_twitter_url + str(current_tweet_id))
        if response.status_code == 200:
            tweet_status = True
        elif response.status_code == 301 or response.status_code == 302:
            if "status/" in response.headers['location']:
                redirect_response = requests.head(response.headers['location'])
                if redirect_response.status_code == 200:
                    tweet_status = True
        if tweet_status and current_tweet_id not in list_current_test_id:
            list_current_test_id.append(current_tweet_id)
            random_tweet_timestamp = get_tweet_timestamp(current_tweet_id, twitter_object)
            file_test_set.write(str(current_tweet_id) + "," + str(random_tweet_timestamp) + "\n")
            points += 1
        count += 1
    return


'''
Find average error on test points
'''


def find_estimate_error():
    data_directory = os.path.join(os.path.dirname( __file__ ), '..', "data")
    if not os.path.exists(data_directory):
        os.mkdir(data_directory)
    cumulative_error = 0
    data_points = 0
    file_test_error = open(os.path.join( data_directory, "testerror.csv"), "w")
    fieldnames = ["TweetId", "TweetTimestamp", "EstimatedTimestamp", "Error"]
    writer = csv.DictWriter(file_test_error, fieldnames=fieldnames)
    writer.writeheader()
    with open(os.path.join(data_directory, "testset.txt"), "r") as file_test_test:
        for line in file_test_test:
            data_points += 1
            line_parts = line.rstrip().split(",")
            estimated_timestamp = find_tweet_timestamp(int(line_parts[0]))
            error = abs(int(estimated_timestamp / 1000) - int(line_parts[1]))
            cumulative_error += error
            writer.writerow({"TweetId": line_parts[0], "TweetTimestamp": line_parts[1], "EstimatedTimestamp": int(estimated_timestamp / 1000), "Error": error})
    file_test_error.close()
    error_rate = int(cumulative_error / data_points)
    hour_error = int(error_rate / (60*60))
    error_rate = error_rate % (60*60)
    minute_error = int(error_rate / 60)
    error_rate = error_rate % 60
    print("Error rate: " + str(hour_error) + ":" + str(minute_error) + ":" + str(error_rate))

def fix_test_set_arguments(argument):
    start_tweet_id = argument[0]
    end_tweet_id = argument[1]
    data_points = argument[2]
    data_interval = argument[3]
    return start_tweet_id, end_tweet_id, data_points, data_interval

def threshold_value(tolerance):
    tolerance = tolerance.split("*")
    result = 1
    for i in tolerance:
        result = result * int(i)
    return result


if __name__== "__main__":
    parser = argparse.ArgumentParser(description='Create a pre-Snowflake Tweet Id dataset based on threshold value, Find timestamp of any pre or post Snowflake Tweet id ,Create Pre-Snowflake Twitter test dataset and check errors on them')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', dest='testset', nargs='*', type=int, default=None, help="Create test set with argument of start, end Tweet Id, and no. of data points")
    group.add_argument('-d', dest='dataset', nargs='?', const="7*24*60*60", type=threshold_value, help="Create a dataset with argument of theshold value in seconds")
    group.add_argument('-e', dest='errortest', action='store_true', help="Check error on pre-Snowflake ids")
    group.add_argument('-t', dest='timestamp', type=int, help="Find timestamp of any tweet id")
    args = parser.parse_args()
    if args.testset:
        start_tweet_id, end_tweet_id, data_points, data_interval = fix_test_set_arguments(args.testset)
        create_test_set(start_tweet_id, end_tweet_id, data_points, data_interval)
    elif args.dataset:
        break_tweet_timeline(args.dataset)
    elif args.errortest:
        find_estimate_error()
    elif args.timestamp:
        tstamp = find_tweet_timestamp(args.timestamp)
        utcdttime = datetime.utcfromtimestamp(tstamp / 1000)
        print(str(args.timestamp) + "   :  " + str(tstamp) + " => " + str(utcdttime))
    elif not args.testset:
        args.testset = [20, 29700859247, 1000, 0]
        start_tweet_id, end_tweet_id, data_points, data_interval = fix_test_set_arguments(args.testset)
        create_test_set(start_tweet_id, end_tweet_id, data_points, data_interval)
