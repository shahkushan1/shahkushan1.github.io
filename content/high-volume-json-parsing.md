Title: High Volume JSON Parsing using Python and/or Bash
Slug: high-volume-json-parsing-python-bash
Date: 1st Nov, 2014
Tags: Python, Bash
Summary: Or how I learnt not to write a script everytime

#The Problem

Your friend gives you a 1.2 gb [JSON Dump of the Twitter Streaming API](https://www.dropbox.com/s/wc32q81gxkc8umr/sample_tweets_data.json?dl=0) and asks you to parse it to find occurrences of Youtube URL patterns e.g. *youtube.com/* and *youtu.be/* in it.

TL;DR If you're interested in a one line solution scroll down to the end of this blog post.

#The Solution

This describes the train of events going through my mind.Be aware that I was doing this for the first time.

Naturally, the *json.load* function led to a memory error. Well, a 1.2 gb file was certainly large for a system with 4 gb memory but I thought I could easily load it into MongoDB and then query it for the url pattern. So I quickly tried to import the json file into MongoDB 

`mongoimport --db test --collection twitter_dump --type json --file sample_tweets_data.json`

and it resulted into -

`exception:read error, or input line too long (max length: 16777216)`

I also tried appending the *jsonArray* switch with the thought that MongoDB would accept multiple documents in a single JSON array

`mongoimport --db test --collection twitter_dump --type json --file sample_tweets_data.json --jsonArray`

`exception:JSONArray file too large`

I thus came to the conclusion that in memory parsing wasn't the way to go. Moreover, since I was only interested in getting the URLs there was no point storing the data into a database. After some google-fu, I came to know about a streaming SAX like Parser for JSON. Aptly called *yajl* [Yet Another JSON Library](https://github.com/lloyd/yajl) I was able to use this and its Python bindings [yajl-py](http://pykler.github.io/yajl-py/) to great effect.

For those who are familiar with the Event driven programming paradigm, you might want to skip the below explanation and jump directly to the code - 

A JSON tree contains the following objects - 

1. { - Start Map

2. } - End Map

3. [ - Start Array

4. ] - End Array

5. keys

6. allowable Values - Null, Integer, Double & String

YAJL contains a core event loop that iterates over the given JSON file. It generates events on hitting each of the above object types. We define custom callback routines that are hit whenever an event is generated. These routines are responsible for extracting the objects of our interest. If all that sounds Greek to you here's a more simplified explanation - 

Since we are interested in finding out all the Youtube URLs in the JSON document, we define a callback routine that is fired on every string value and checks whether the string matches a regex. 

The code is available in [this](https://github.com/shahkushan1/tweet_parser) repository. Besides JSON parsing, YAJL is feature rich and its streaming implementation makes it useful for other things as well - JSON Reformattng, JSON Validation. It's source has detailed [examples](https://github.com/pykler/yajl-py/tree/master/examples/)

I later discovered that besides writing a Python script to accomplish this task, I could have tried these options as well - 

1. [**jq**](http://stedolan.github.io/jq/) - A Commandline JSON Parser written in C

2. `grep -Po 'http[s]:\/\/www\.youtube\.com/watch\?v\=.{11}|https:\/\/youtu.be\/.{11}' sample_tweets_data.json`

As a quick performance check I compared the time taken by my Python script (which used yajl) vs the *grep* command. 

- *grep* - 1 minute 55 seconds

- Python - 3 minutes 1 seconds 

It was clear that *grep* was the winner here in terms of speed. But I did learn a whole bunch of new tools and a practical use of the Event Driven Programming paradigm while attempting to solve this problem. What are your favorite techniques for JSON Parsing? Do you optimize for speed, code maintainability or quick solutions?