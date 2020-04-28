![tinderbot](/images/tinderbot_logo.png)

On April 2nd 2020 (day after April Fool's Day lol), Tinder announced that it will open up the use
of it's Passport feature to all Tinder users.  The Passport feature allows you to match
with people all over the world versus your immediate area in an attempt to combat lonliness and boredom during the shelter in place and quarantine directives being rolled out all over.

I decided to use this opportunity to gather Tinder profile information of users around the world to build a database to apply my newfound data science and analytical skills towards in an attempt to combat my own lonliness and boredom during the shelter in place and quarantine directives being rolled out all over.

## Chapter 1 - Robots Are Taking Our Jobs

The genesis of this project was heavily inspired by my friend who made a bot who's function was to promote himself as data scientist to help land him a job.  [Original project repository here](https://github.com/Aaronhjlee/swipe_bot).  I wanted to take his project one step further and webscrape the profile information of all the users it came across.

The bot is Python based and utilizes Selenium to run a WebDriver to simulate a user's session.  Luckily in addition to the popular mobile app, Tinder offers the same service on a computer internet browser.

TINDERBOT BOOT UP GIF

I also found it funny that the good people at Tinder offer a "work mode" to help get in some swipes while on the clock.  I'm more of an Alt-Tab man myself tho.

TINDER WORK MODE GIF

From here, I wrote a series of subfunctions to automatically execute clicks and keystrokes to simulate swiping behaviors.  I also wrote a webscaping script that dives into the HTML to extract relavant information.  The Tinder web app UI is beautiful but incorporates a lot of JavaScript and non-intuitive class names which makes webscraping a moving target.  But where there's a will, there's a way.

I set my bot to the "equal opportunity" setting which swipes right (in the positive direction for the uninitiated) for everyone.  It is also the only setting it has.  In the event that I want to use Tinder for it's intended purposes, I would ideally like to train it with my personal preferences via a neural network.  But that sounds like a lot of labeled data and will be slated for the future.

Click on the image below quick video of the bot in action overlayed with Beyonce's hit "Single Ladies" song for obvious reasons:

[![Video](images/cover_image.png)](https://streamable.com/bj5ps3)

[Link to video](https://streamable.com/bj5ps3)

![Sound On](images/sound_on.png)

(Note: Potential love of life alert at 0:23 of video)

Current limitations of the system is internet connectivity and system memory.  If the images do not load fast enough, the bot may skip a beat and record incomplete data.  And because the Tinder web app UI is a single page that is constantly fed new data, I believe that all the data is cached and never leaves - eventually eating up all your system memory and lagging things beyond functionality.  I ain't no web developer tho, just a hunch.  An expansion I would like to include one day is to run multiple instances of this bot on AWS EC2 in parallel to incorporate the power of cloud computing to my collection methods and not be limited to my 2012 MacBook.

All data per webscraping session is constantly saved and appended to a local .csv file that is later aggregated into a master file.  Eventually will be uploaded to Amazon RDS Postgres instance using Psycopg2 but we're not there yet.

The bot is what made the data collection possible.  Doing this manually would be insane.  I've used other methods like Beautiful Soup to webscrape static webpages ([shameless plug for my other rap based project](https://www.thwdesigns.com/what-we-talkin-bout)), but using Selenium for the first time to automate user sessions with credentials and actions is very cool.

## Chapter 2 - Initial Findings

I ran the bot overnight for about two weeks at the beginning of April 2020, roughly when COVID 19 started shutting everything down ([other shameless plug for my COVID19 based project](https://www.thwdesigns.com/united-states-of-covid)).  Here's an initial look at the overall dataset:


* 76,212 Total Profiles Gathered
* 75,609 ENTRIES HAVE AGE DATA (99.2%)
* 26,468 ENTRIES HAVE COLLEGE DATA (34.7%)
* 18,958 ENTRIES HAVE CITY DATA (24.9%)
* 18,822 ENTRIES HAVE JOB DATA (24.7%)
* 13,920 ENTRIES HAVE GENDER DATA (18.3%)
* 74,614 ENTRIES HAVE DISTANCE DATA (97.9%)
* 56,515 ENTRIES HAVE PROFILE DETAIL DATA (74.2%)
* 19,925 ENTRIES HAVE SPOTIFY ANTHEM DATA (26.1%)
* AVERAGE AGE IN DATA SET: 24
* NUMBER OF UNIQUE COLLEGES: 9719
* NUMBER OF UNIQUE JOBS: 11960
* NUMBER OF UNIQUE CITIES: 3413
* AVERAGE PICS PER PROFILE: 5

Quick discussion about the above:
* Age data is pretty self explanatory - but the ability to hide age is provided with the purchase of Tinder Plus, so if-so-fact-o (actually ipso facto in Latin lol), a minmum of 0.8% of women on Tinder flex with Plus?  You decide.
* About a third of users went to college / chose to add it to their profile.
* City data is relatively low (~25%), but fortunately I do have distance data of nearly all users.  Will do some calculations later to mathematically guesstimate the cities of the users with missing data.
* Approx a quarter of users chose to share their job with the most common being Student which is cool since Tinder started off on college campuses (thanks NPR How I Made This Podcast lol).
* About a fifth of users decided to explicitly list their gender.  Funnily enough the option is open-ended so the values range from specific LGBTQ definitions to others like "pizza" or "potato."
* Distance data is provided for most users but can also be hidden with Plus.  Ipso facto 2.1% are flexing here.
* Profile detail data is left blank for about 25% of the users.  This will be useful in later classification of "high effort" vs "low effort" profiles.
* A bit over a quarter of users choose to link the Spotify account and provide their "anthem."  Unsurprisinly "The Weekend" was the most chosen.  More on this later with genre clustering.
* There were ~3,400 unique cities in my dataset.  I used Geocoder to build a local location cache containing latitude/longitude info, state data (for USA), and country data for each city.

So Tinder Passport is pretty dope - here is a heatmap of the location of users my bot came across.  As you can see I was paired with users all over the world.  

![heatmap](images/heatmap.png)

Interactive version coming soon - needs to be hosted somewhere, maybe like heroku

However the majority of the data came from nearby local users in Los Angeles (which is where I was located during the data collection) so I.I.D. is out the window for the entire dataset.  However I think when we zoom into the city level outside the US, the datapoints are still chosen random enough to make insights about the population.

![distance_distribution](images/user_distances.png)

Below is the distribution of ages of the profiles in the dataset with a vertical line drawn at the mean age (24)

![age_distribution](images/user_ages.png)

Now we have an idea of what the overall data looks like - let's dive into the contents of each.  

## Chapter 3 - Into the Nitty Gritty

Below is a word cloud of the details section across the entire dataset.

![aggregate_word_cloud](images/aggregate_word_cloud.png)

Huh, a LOT of Instagram mentions on Tinder.  Who woulda thunk.  I wonder if users are using their profiles in an attempt to grow their IG following to become a more influencial influencer.  Sounds like another project for another time.

In the meantime, I hand picked certain topics I was interested in and checked for keywords relating to that topic.  This list can be easily appended and expanded with future topics or keywords.

Topics Include:
* COVID-19 / Quarantine Mentions
* Instagram / Snapchat Mentions
* 




BEHAVIORS
AGGREGATE WORD CLOUD
COVID19 MENTIONS
INSTAGRAM
SNAPCHAT
Premium Snap
office mentions

