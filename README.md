# NJIT Course Page Scraper

This simple Python script currently just scans through the Fall 2015 course list and extracts <td> elements within all <tr> elements throughout the DOM. To start, be sure to update pip, and install lxml and requests:

```
pip install --upgrade pip
pip install lxml
pip install requests
```
You'll probably have to use `sudo` for the first, but the latter two should be fine without.

Be sure to check out the DatabaseSchema.sql file to see what the table looks like that I'm using. Field "sizes" are approximations based on data samples I've seen.

NOTE - just change the database name in the script itself and you should be good to go.

## TODO
This script is just a start, but is a cool learning opportunity for anyone interested. A great goal would be to have this script running fast enough to extract course data every 15 minutes and store it in a MySQL database. With that, my goal would be to create an API whereby anyone with a key can send GET requests to return data in JSON, allowing them to use NJIT course data in their applications.
