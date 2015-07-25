# imports
from lxml import html
import requests
import mysql.connector
import time

# database setup
my_host = "localhost"
my_username = "root"
my_password = ""
my_database = "njit"

# establish MySQL connection
cnx = mysql.connector.connect(user=my_username, password=my_password,host=my_host,database=my_database)
cursor = cnx.cursor()

# takes the output of refresh_departments() as an input (array with 4 values in it), and inserts all courses in that
# department into the localhost database
def retrieve_courses(url, term, year):

	# send a get request to the department page per input and convert to tree
	page = requests.get("http://www.njit.edu" + url)
	tree = html.document_fromstring(page.text)
	dept = tree.xpath('//h1')[0].text

	# check where the bold tag is - that's where we'll start
	for val in tree.xpath('//b'):
		
		# get ready to loop through all sections in the course in the table directly after the bold tag
		# starting with the bold tag
		for sec in val.xpath('following::table')[0].xpath('tr'):
			# but before looping through table data, grab the course number and name via the bold tag
			arr = [val.xpath('a')[0].text, val.xpath('u')[0].text.strip()]

			# loop through details of each section and append it to the array
			for det in sec.xpath('td'):
				arr.append(det.text_content().strip().encode('ascii','replace'))
			
			# add department info to array
			arr.append(dept)
			arr.append("http://www.njit.edu" + url)
			arr.append(term)
			arr.append(year)
			
			# the first row is table headers, so there will be no table data to extract (uses th vs td), so ignore if there
			# are only 6 elements (course name and department data)
			if(len(arr) == 17):
				# when ready, create query string, insert and commit!
				query_string = "INSERT INTO courses (number, name, sect, cr, days, times, room, status, max, now, instructor, comments, credits, dept, url, term, year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				cursor.execute(query_string, arr)
				cnx.commit()
	

sems = {'fall':'F','winter':'W','spring':'S','summer':'U'}

for key, sem in sems.iteritems():

	for i in range(2014, 1999, -1):
		page = requests.get("http://www.njit.edu/registrar/schedules/courses/" + key  + "/" + str(i) + sem + ".html")
		tree = html.document_fromstring(page.text)

		if page.status_code == 300:		
			for val in tree.xpath('//a'):
				url = val.attrib['href']				
				retrieve_courses(url, key, str(i))
