# TweetedAt

[TweetedAt](https://oduwsdl.github.io/tweetedat/) extracts date and time from the tweet ID by reverse-engineering [Twitter Snowflake](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake.html).

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




