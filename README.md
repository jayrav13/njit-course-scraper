# NJIT Course Page Scraper

This Python script currently scrapes all course data across available terms and stores the data in a MySQL table. Every time it is run, the courses are purged from the table before reinserting. My main motivation for writing it was to familiarize myself with Python.

Before running, please execute the following commands in terminal:
```
pip install --upgrade pip
pip install lxml
pip install requests
```

Below is the schema for the table used. Note that the reason for using VARCHAR's of size 255 across the board was because of corner cases where fields were massive because of spacing between words that I couldn't solve with `.strip()`. Fine tuning can easily bring that down to more reasonable sizes:

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

By executing `python scrape.py`, you'll be able to scrape and store all current schedule information across all terms in under 30 seconds. Just be sure to change the name of the database in `scrape.py` to whichever database your table is in.

##TODO
My goal is to implement an application similar to [Rutgers University's Course Sniper](sniper.rutgers.io) whereby users can submit a course to observe in case it opens up. If anyone reading this is interested in helping out, please reach out!

By Jay Ravaliya
