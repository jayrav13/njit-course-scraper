# imports
from lxml import html
import requests
import mysql.connector

# HTTP GET of webpage to scrape
page = requests.get("http://www.njit.edu/registrar/schedules/courses/fall/2015F.CS.html")
tree = html.document_fromstring(page.text)

# establish MySQL connection
cnx = mysql.connector.connect(user='root', password='',host='localhost',database='test')
cursor = cnx.cursor()

# loop
for row in tree.xpath('.//tr'):
	values = []
	for val in row.xpath('td'):
		values.append(val.text_content().strip())
		print val.text_content().strip()


	if len(values) == 11:	
		queryString = "INSERT INTO courses VALUES (%s, %s, %s, %s, %s, %s, %s ,%s, %s, %s, %s)"
		cursor.execute(queryString, values)
		cnx.commit();

# close connection
cursor.close()
cnx.close()
