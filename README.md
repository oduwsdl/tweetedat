# TweetedAt

[TweetedAt](https://oduwsdl.github.io/tweetedat/) extracts date and time from the tweet ID by reverse-engineering [Twitter Snowflake](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake.html).

[1] Mohammed Nauman Siddique and Sawood Alam. 2019. TweetedAt: Finding Tweet Timestamps for Pre and Post Snowflake Tweet IDs. (August 2019). Retrieved July 25, 2020 from https://ws-dl.blogspot.com/2019/08/2019-08-03-tweetedat-finding-tweet.html

## Why not check on Twitter directly?

* It is the only web service which allows users to find the timestamp of the Snowflake tweet IDs and estimate tweet timestamps for pre-Snowflake Tweet IDs.
* Twitter developer API has [access rate limits](https://developer.twitter.com/en/docs/basics/rate-limits). It acts as a bottleneck in finding timestamps over a data set of tweet IDs. This bottleneck is not present in TweetedAt because we do not interact with Twitter's developer API for finding timestamps. 
* [Deleted]((https://help.twitter.com/en/using-twitter/delete-tweets)), [suspended](https://help.twitter.com/en/managing-your-account/suspended-twitter-accounts), and [protected](https://help.twitter.com/en/safety-and-security/public-and-protected-tweets) tweets do not have their metadata accessible from Twitter's developer API. TweetedAt is the solution for finding the timestamps of any of these inaccessible tweets. 

## Repo Content Description
```bash
 .
 ├── script                     
 │  ├── TimestampEstimator.py   # Script file 
 ├── data                           
 │  ├── TweetTimeline.txt       # Contains list of tweet IDs and timestamps for pre-Snowflake IDs used in timestamp estimation
 │  ├── TweetTimelineList.txt   # Contains the TweetTimeline.txt data as list of lists 
 │  ├── testerror.csv           # Shows the result of error on test set
 │  ├── testset.txt             # Contains test set of tweet IDs and their timestamps 
 │  └── WeirdUrls.txt           # Lists all pre-Snowflake Twitter URLs which didn't resolve to 200 after chasing the redirect location 
 ├── index.html                 # TweetedAt implementation
 ├── LICENSE
 └── README.MD
 ```
## Python Script: TimestampEstimator.py

The script can be used for:

* finding the timestamp of any Snowflake ID or estimating timestamp of any pre-Snowflake ID
* creating a test set of pre-Snowflake IDs
* calcualting error of the test set

### Using CLI Version of Python Script

* Option -h: for help 
```bash
$ ./TimestampEstimator.py -h
usage: TimestampEstimator.py [-h] [-s [TESTSET [TESTSET ...]] | -d [DATASET] |
                             -e | -t TIMESTAMP]

Create a pre-Snowflake Tweet Id dataset based on threshold value, Find
timestamp of any pre or post Snowflake Tweet id ,Create Pre-Snowflake Twitter
test dataset and check errors on them

optional arguments:
  -h, --help            show this help message and exit
  -s [TESTSET [TESTSET ...]]
                        Create test set with argument of start, end Tweet Id,
                        and no. of data points
  -d [DATASET]          Create a dataset with argument of threshold value in
                        seconds
  -e                    Check error on pre-Snowflake ids
  -t TIMESTAMP          Find timestamp of any tweet id

```
* Option -t: for finding timestamp of a Tweet ID

```bash
$ ./TimestampEstimator.py -t 20
```
* Option -d: for creating pre-Snowflake data set for estimating timestamp. It accepts the threshold value in seconds. When no parameter is supplied, it creates a weekly data set.

For creating daily data set

```bash
$ ./TimestampEstimator.py -d 24*60*60
```
* Option -s: For creating test set. It accept start tweet ID, end tweet ID,number of test data points, and data point interval as parameters.

For creating a weekly data set of 10 tweet IDs between tweet ID 20 and 1000

```bash
$ ./TimestampEstimator.py -s 20 1000 10 7
```

For creating random data set of 100 points between tweet ID 20 and 1000

```bash
$ ./TimestampEstimator.py -s 20 1000 10 7
```
* Option -e: Calculates error csv file of the test set
```bash
$ ./TimestampEstimator.py -e
```
