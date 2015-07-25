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

# there are no inputs, output is an array of all departments for all available terms
def refresh_departments():

	# all possible semesters, variable to store all departments
	ALL_SEMESTERS = ["fall", "spring", "summer", "winter"]
	all_departments = []

	# loop through all terms and extract data pertinent to each one
	for term in ALL_SEMESTERS:

		# request page, convert to tree, extract all anchor values
		page = requests.get("http://www.njit.edu/registrar/schedules/courses/" + term + "/index_list.html")
		tree = html.document_fromstring(page.text)
	
		#for each anchor value, grab pertinent data!	
		for val in tree.xpath('//a'):
			all_departments.append([val.text, val.attrib['href'], term, val.attrib['href'][:4]])

	# return all departments in a nested array
	return all_departments

# takes the output of refresh_departments() as an input (array with 4 values in it), and inserts all courses in that
# department into the localhost database
def retrieve_courses(dept, url, term, year):

	# send a get request to the department page per input and convert to tree
	page = requests.get("http://www.njit.edu/registrar/schedules/courses/" + term + "/" + url)
	tree = html.document_fromstring(page.text)
	
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
			arr.append(url)
			arr.append(term)
			arr.append(year)
			
			# the first row is table headers, so there will be no table data to extract (uses th vs td), so ignore if there
			# are only 6 elements (course name and department data)
			if(len(arr) == 17):
				# when ready, create query string, insert and commit!
				query_string = "INSERT INTO courses (number, name, sect, cr, days, times, room, status, max, now, instructor, comments, credits, dept, url, term, year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				cursor.execute(query_string, arr)
				cnx.commit()
	

# main

# returns a nested array of all departments
departments = refresh_departments()

# start a timer
start = time.time()

# run as an SQL transaction so that there is no down time in requests to the database
cursor.execute("START TRANSACTION")
cnx.commit()
cursor.execute("TRUNCATE courses")
cnx.commit()

# for each department, retrieve courses
for dept in departments:
	if dept[2] == "fall":
		retrieve_courses(dept[0], dept[1], dept[2], dept[3])
		print dept[0] + ", " + dept[1] + ", " + dept[2] + ", " + dept[3]

# complete commit
cursor.execute("COMMIT")
cnx.commit()

# output run time
print "Run time: " + str(time.time() - start)

cursor.execute("SELECT * FROM requests")
result = cursor.fetchall()
print result

#close connection
cnx.close()
