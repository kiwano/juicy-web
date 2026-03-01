#!/usr/bin/python
import cgi, cgitb
import urllib
import sys
import codecs
import config

# Set encoding and enable cgitb
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
cgitb.enable()

# Get access to the CGI data
form = cgi.FieldStorage()


# Set up a hash for the various available searches
searches = {}
for search in config.toolbar_searches:
  search_key = urllib.quote_plus(search[0])
  searches[search_key] = search[1]


# Get the search information from the CGI data
search = form.getfirst('search')
query = urllib.quote_plus(form.getfirst('query'))


# Construct the redirect URL from the search data and hash
if search in searches.keys():
  refresh_dest = searches[search] % (query)
else:
  refresh_dest = 'http://juicy.melon.org/'


# And now produce the redirect page
print("Content-Type: text/html;charset=utf-8")
print('')
print '<html>'
print '<head>'
print '<meta http-equiv="refresh" content="0 url=%s">' % (refresh_dest)
print '</head>'
print '</html>'

