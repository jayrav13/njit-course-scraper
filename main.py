# imports
from lxml import html
import requests
import mysql.connector

# database setup
my_host = "localhost"
my_username = "root"
my_password = ""
my_database = "njit"

# establish MySQL connection
cnx = mysql.connector.connect(user=my_username, password=my_password,host=my_host,database=my_database)
cursor = cnx.cursor()

# there are no inputs, output is an array of all departments for all available terms
def refresh_departments():

	# all possible semesters, variable to store all departments
	ALL_SEMESTERS = ["fall", "spring", "summer", "winter"]
	all_departments = []

	# start a transaction that clears the table and adds all departments back to it
	cursor.execute("START TRANSACTION")
	cnx.commit()
	cursor.execute("TRUNCATE departments")
	cnx.commit()

	# loop through all terms and extract data pertinent to each one
	for term in ALL_SEMESTERS:

		# request page, convert to tree, extract all anchor values
		page = requests.get("http://www.njit.edu/registrar/schedules/courses/" + term + "/index_list.html")
		tree = html.document_fromstring(page.text)
	
		#for each anchor value, extract!	
		for val in tree.xpath('//a'):
			cursor.execute("INSERT INTO departments (department, url, term, year) VALUES(%s, %s, %s, %s)", [val.text, val.attrib['href'], term, val.attrib['href'][:4]])	
			cnx.commit()	
			all_departments.append([val.text, val.attrib['href'], term, val.attrib['href'][:4]])

	# commit all sql queries, fail if any one fails
	cursor.execute("COMMIT")
	cnx.commit()
	
	# return all departments in a nested array
	return all_departments

# return all courses for a given url input, where the url input is the html file of a particular year/term/department
def retrieve_courses(url, term):
	# HTTP GET of webpage to scrape
	page = requests.get("http://www.njit.edu/registrar/schedules/courses/" + term + "/" + url)
	tree = html.document_fromstring(page.text)

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

# main
departments = refresh_departments()

for dept in departments:
	print dept[1]
	retrieve_courses(dept[1], dept[2])
