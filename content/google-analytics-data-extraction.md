Title: Getting your Google Analytics Data into R
Slug: google-analytics-data-extraction
Date: 28th Oct, 2014
Tags: R
Summary: Step by step guide to data extraction using RGoogleAnalytics

R is often cited to be the *lingua franca* of analysis. While that claim might be held debatable by many folks, R certainly packs in a lot of good implementations in the form of libraries. A simple glance at the [CRAN Task Views](http://cran.r-project.org/web/views/) will tell you the range of problems you can solve via R. So as a digial analyst, here is the conundrum? One that I have certainly faced

- R is very powerful in terms of its libraries and statistical capabilities
- I have extremely good Google Analytics Data
- I also have business problems that my boss would want to be solved
- But Google Analytics does not have a native client library for the R language! 

Not having a client library means a lot of tedious jobs - **Authentication**, **JSON Parsing**, **Error handling with the Core Reporting API** would have to be solved *just in order to get the data into R*. For someone who is primarily interested in analyzing data, this low level plumbing work is best left to libraries. This is the problem that RGoogleAnalytics solves. Put simply, RGoogleAnalytics is a wrapper over the Google Analytics API
(Side Note - It is not the only library which solves this problem. Shout out to [Bror Skardhamar](https://twitter.com/skardhamar) for his excellent implementation in the form of rga package)

But why would you want to use the API to extract your data? What is wrong with just dumping csv files from the
Google Analytics Interface?

- The User Interface allows you to only export Standard Reports which means they contain a preset combination of dimensions and metrics. With the API, you can extract an vast combination of dimension/metric combinations. Combine this with the power of R, this opens up new and interesting avenues to explore your data.
- Oh I almost forgot, you can always create Custom Reports! Yes, but these Custom Reports can contain only 4 dimensions per report. The API has a limit of 7 dimensions per query
- And wait did I mention Sampling? Better I leave that for another post

####Enough with the talk! Show me how to get my data into R

Before we actually dive into the R script, there is a one time setup required. 

### Getting the OAuth 2.0 credentials

1. Head over to [Google Developers Console](http://console.developers.google.com) 
2. Create a New Project
3. Once created, navigate to APIs and enable the Analytics API for your project
4. Navigate to Credentials and create a New Client ID
5. The wizard will ask you to add a Product Name and set your email address
6. On the Next Screen, set Application Type as *Installed Application* and Installed Application Type as *Other*

It should look like the screen shown here 

![Application Type Selection Dialong](/static/images/credentials.png)

6. Your OAuth 2.0 credentials are now created. Copy the Client ID and the Client Secret to your R Script 

Note that the OAuth Credentials are unique to your account and best practices dictate that they not be shared with others or exposed in public scripts

```sh
require(RGoogleAnalytics)

# Authorize the Google Analytics account
# This need not be executed in every session once the token object is created 
# and saved
client.id <- "xxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com"
client.secret <- "xxxxxxxxxxxxxxxd_TknUI"
token <- Auth(client.id,client.secret)

# Save the token object for future sessions
save(token,file="./token_file")

# In future sessions it can be loaded via 
load("./token_file")
```

*What did we just do? What the heck is OAuth anyway?*

Think of OAuth this way - We will be using R to extract data from a particular Google Analytics Account

We will be using R to extract data from Google's Servers via the Google Analytics API. Each request to the API has to be authenticated via an Access Token. Your OAuth Credentials **(Client ID + Client Secret)** are used to retrieve this Access Token. Access Tokens have a lifetime of 60 minutes after which they need to be
regenerated. But we will get to that.

The next step is to get the Profile ID/View ID of the Google Analytics profile for which the data extraction is to be carried out. It can be found within the Admin Panel of the Google Analytics UI. This profile ID maps to the *table.id* argument below. The rest of the query parameters are pretty much standard. Having said that, keep the following points handy

- Dimensions and Metrics Names are a bit different from the ones you see normally in the UI. The complete list of valid names can be found at [this](https://developers.google.com/analytics/devguides/reporting/core/dimsmets) link
- Dimensions and Metric names use (Camel Case)[http://en.wikipedia.org/wiki/CamelCase] e.g. ga:sourceMedium

- A better workaround to remembering these minute things is to test your queries using the [Query Feed Explorer](http://ga-dev-tools.appspot.com/explorer/). Once your query runs successfully, you can quickly copy the parameters to your R Script saving you from a lot of legwork. 

Here is the remainder of the script which gets you the requested data into a dataframe.

### Extraction 

```sh
# Build a list of all the Query Parameters

# Get the Sessions & Transactions for each Source/Medium sorted in 
# descending order by the Transactions
 
query.list <- Init(start.date = "2014-08-01",
                   end.date = "2014-09-01",
                   dimensions = "ga:sourceMedium",
                   metrics = "ga:sessions,ga:transactions",
                   max.results = 10000,
                   sort = "-ga:transactions",
                   table.id = "ga:7994504")

# Create the Query Builder object so that the query parameters are validated
ga.query <- QueryBuilder(query.list)

# Extract the data and store it in a data-frame
ga.data <- GetReportData(ga.query, token)

# Sanity Check
summary(ga.data)
dim(ga.data)

```

Coming back to the point about Access Tokens, since they expire after 60 minutes. How do we ensure whether the current Access Token is valid or it needs to be regenerated? This functionality is wrapped within *ValidateToken()* It validates the token and regenerates a fresh version if it has expired. Here's how to use it in practice

```sh
ValidateToken(token)
```
In case if you want the entire script, it can be found [here](https://gist.github.com/shahkushan1/9c61b9f7c46308d13f6e). In upcoming posts, we will see how to work around Sampling and also discuss some use-cases by marrying the power of Google Analytics and R