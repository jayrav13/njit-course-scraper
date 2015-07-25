# NJIT Course Page Scraper

To start familiarizing myself with Python, I wrote page scraping tools for NJIT's Course Schedule. Two of them are up and running so far:
	`history.py` pulls historical data from 2000 to 2014
	`scrape.py` pulls all course data for active semesters. 

Before running, please execute the following commands in terminal:
```
pip install --upgrade pip
pip install lxml
pip install requests
```

Below is the schema for the table used to store both historical data and active data. You can fine tune the varchar sizes, but I just made them 255 to account for corner cases where there were extensive spaces within the text. 

```SQL
CREATE TABLE courses (
	id int(11) AUTO_INCREMENT,
	number varchar(255),
	name varchar(255),
	sect varchar(255),
	cr varchar(255),
	days varchar(255),
	times varchar(255),
	room varchar(255),
	status varchar(255),
	max varchar(255),
	now varchar(255),
	instructor varchar(255),
	comments varchar(255),
	credits varchar(255),
	term varchar(255),
	dept varchar(255),
	url varchar(255),
	year varchar(255),
	PRIMARY KEY (id)
)
```

By executing `python scrape.py`, you'll be able to scrape and store all current schedule information across all terms in under 30 seconds. Just be sure to change the name of the database in `scrape.py` to whichever database your `courses` table is in. `history.py` will take a bit longer and will yield north of 100,000 rows of data.

##Issues
There are some corner cases in the Course Schedule itself. Example: http://www.njit.edu/registrar/schedules/courses/fall/2006F.ACCT.html. Here, multiple rows have "missing" table data values so right now my script ignores any row missing table data values entirely. 

##TODO
There are a few cool things to try with this. The first is possibly implementing a version of [Rutgers University's Course Sniper](http://sniper.rutgers.io) for these courses (active courses only). The other is building an API that can be used at HackNJIT. Feel free to clone and use however you'd like!

By Jay Ravaliya
