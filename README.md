# CoffeeRec

Across different industries, our preferences are being used to generate recommendations of products we may like. Amazon recommends goods we might like based on our past purchases, and Netflix recommends movies based on our watching histories. This personalization makes it easier to make decisions and to find new products. Amazon and Netflix have the advantage of having a huge an established product that generates data to fuel their recommendation	 system. This project will seek to implement a system for recommending coffees. Without any large store of coffee data, an alternative solution will need to be used to generate the initial data for the recommendations. Mining twitter and correlating mentions of different coffees to the user that posts the tweet can generate this data store. By monitoring the tweets users make about different coffee, we will create an initial database of coffee preferences that can be used to generate recommendations

There are a huge number of coffee roasters and different coffees to choose from. This application will allow a user to track past coffees they have tried. The data will be compared with other users histories along with data from several other data sources to generate recommended coffees for a user. The recommendations will be integrated into an iOS mobile app to allow users to track coffees and view recommendations.


## Building and Running the project
### Scrapers
Scrapers have been written for various coffee roasters. These will be used to populate database of coffees, which will then be used to direct the data collection from twitter. To run the scrapers install scrapy as instructed <a href="http://scrapy.org/">here</a>. The easiest way to accomplish this is using the python package mananger pip and the command  `pip install scrapy`. 
To run the scrapers use the command `scrapy crawl scraper_name`. To use the scraper, needs to be running (Default port 3001 on localhost). Currently to change the database location, the location must be changed in the scrapers/pipelines.py file.

### Web Application
The user interface is available at <a href="http://brewbetter.meteor.com">brewbetter.meteor.com</a>.
### Data Analysis 
The data analysis and twitter mining files are currently in ipython notebooks. To view and run these, run `ipython notebook` at the command line and direct your browser to localhost:8080

## Milestones
#### 1. <a href="https://github.com/abachman11/CoffeeRecs/milestones/Milestone%201">Milestone 1 Prototyping</a> 1/14-1/21
#### 1. <a href="https://github.com/abachman11/CoffeeRec/issues?q=milestone%3A%22Build+Cycle+1%22">Milestone 2</a>
#### 1. <a href="https://github.com/abachman11/CoffeeRec/milestones/Build%20Cycle%202">Milestone 3</a>
#### 1. <a href="https://github.com/abachman11/CoffeeRec/milestones/Build%20Cycle%203">Milestone 4 - Build Cycle 3</a>

Andrew Bachman - 2014
