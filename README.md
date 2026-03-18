# TweetedAt and Reverse TweetedAt

[TweetedAt](https://oduwsdl.github.io/tweetedat/) extracts date and time from the tweet ID by reverse-engineering [Twitter Snowflake](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake.html). It is the only web service which allows users to find the timestamp of the Snowflake tweet IDs and estimate tweet timestamps for pre-Snowflake Tweet IDs.

[ReverseTweetedAt](https://oduwsdl.github.io/tweetedat/) converts timestamp to a tweet ID prefix by reversing [TweetedAt](https://oduwsdl.github.io/tweetedat/).

[1] Mohammed Nauman Siddique and Sawood Alam. 2019. TweetedAt: Finding Tweet Timestamps for Pre and Post Snowflake Tweet IDs. (August 2019). Retrieved July 25, 2020 from https://ws-dl.blogspot.com/2019/08/2019-08-03-tweetedat-finding-tweet.html

[2] Tarannum Zaki, Michael L. Nelson, and Michele C. Weigle. 2026. Reverse TweetedAt: Determining Tweet ID prefixes from Timestamps. (March 2026).

## Why not check on Twitter directly?

* Twitter developer API has [access rate limits](https://developer.twitter.com/en/docs/basics/rate-limits). It acts as a bottleneck in finding timestamps over a data set of Tweet IDs. This bottleneck is not present in TweetedAt because we do not interact with Twitter's developer API for finding timestamps. 
* [Deleted]((https://help.twitter.com/en/using-twitter/delete-tweets)), [suspended](https://help.twitter.com/en/managing-your-account/suspended-twitter-accounts), and [protected](https://help.twitter.com/en/safety-and-security/public-and-protected-tweets) Tweets do not have their metadata accessible from Twitter's developer API. TweetedAt is the solution for finding the timestamps of any of these inaccessible Tweets. 

## Repo Content Description
```bash
 .
 ├── script                     
 │  ├── TimestampEstimator.py   # Script file 
 ├── data                           
 │  ├── TweetTimeline.txt       # Contains list of Tweet IDs and timestamps for pre-Snowflake IDs used in timestamp estimation
 │  ├── TweetTimelineList.txt   # Contains the TweetTimeline.txt data as list of lists 
 │  ├── testerror.csv           # Shows the result of error on test set
 │  ├── testset.txt             # Contains test set of Tweet IDs and their timestamps 
 │  └── WeirdUrls.txt           # Lists all pre-Snowflake Twitter URLs which didn't resolve to 200 after chasing the redirect location 
 ├── index.html                 # TweetedAt implementation
 ├── LICENSE
 └── README.MD
 ```
## Python Script: TimestampEstimator.py

The script can be used for:

* Finding the timestamp of any Snowflake ID or estimating timestamp of any pre-Snowflake ID
* Creating a test set of pre-Snowflake IDs
* Calcualting error of the test set

### Using CLI Version of Python Script

* Option -h: for help 
```bash
$  ./TimestampEstimator.py -h
usage: TimestampEstimator.py [-h] [-s [TESTSET ...] | -d [DATASET] | -e | -t TIMESTAMP]

Create a pre-Snowflake Tweet ID dataset based on threshold value, Find timestamp of any pre or post Snowflake Tweet ID, Create Pre-
Snowflake Twitter test dataset and check errors on them

options:
  -h, --help        show this help message and exit
  -s [TESTSET ...]  Create test set with argument of start, end Tweet ID, and no. of data points
  -d [DATASET]      Create a dataset with argument of theshold value in seconds
  -e                Check error on pre-Snowflake ids
  -t TIMESTAMP      Find timestamp of any Tweet ID

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
## Using Tweet ID Regex to Retrieve Tweet URLs at Different Levels of Granularity

* Use Reverse TweetedAt to determine tweet ID regex across temporal granularity
* Use the tweet ID regex to grep through a CDX API response of all tweets associated with a Twitter account

**Example:**

For a tweet ID '1495226962058649603,' using Reverse TweetedAt we can get the timestamp at millisecond-level granularity (2022-02-20T02:41:02.385Z). We can use this timestamp to get the tweet ID regex at millisecond-level granularity using Reverse TweetedAt.

  **Finding search space at millisecond-level granularity:**
```bash
$ curl -s "https://web.archive.org/cdx/search/cdx?url=https://twitter.com/randyhillier/status/&matchType=prefix" \
| grep -E 'status/14952269620[0-9]{8}' | wc -l
```

  We can further reduce the precision of the tweet ID prefix to second- and minute-level granularity and obtain the tweet ID regex to compute the corresponding search space. 
  
  **Finding search space at millisecond-level granularity:**
  ```bash
$ curl -s "https://web.archive.org/cdx/search/cdx?url=https://twitter.com/randyhillier/status/&matchType=prefix" \
| grep -E 'status/149522696[0-9]{10}' | wc -l
```

  **Finding search space at millisecond-level granularity:**
```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=https://twitter.com/randyhillier/status/&matchType=prefix" \
| grep -E 'status/149522[0-9]{13}' | wc -l
```
This illustrates how lower temporal granularity expands the potential search space. However, a wider ID range does not necessarily produce more results; it only increases the number of possible candidate IDs.
