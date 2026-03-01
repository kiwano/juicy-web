#!/usr/bin/python3

# searches to be incorporated in the search dropdown in the toolbar
toolbar_searches = [
  ['Wikipedia', 'https://en.wikipedia.org/wiki/Special:Search?search=%s&go=Go'],
  ['Google', 'https://www.google.com/search?q=%s'],
  ['Google Maps', 'https://www.google.ca/maps/search/%s/'],
  ['Youtube', 'https://www.youtube.com/results?search_query=%s'],
  ['IMDB', 'https://www.imdb.com/find?q=%s&s=all'],
]

# bookmarks to be displayed in the toolbar along the top of the page
toolbar_bookmarks = [
  ["Debian", "https://www.debian.org/"],
  ["Python", "https://python.org/"],
]

# unhideable bookmarks to be displayed in the sidebar above the bookmark director tree
sidebar_bookmarks = [
["Apache", "https://apache.org/"],
["Wordpress", "https://wordpress.org/"],
]

bookmarkfile = "/path/to/bookmarks"

db = "postgresql://username:password@localhost/dbname"

weatherstations = ['CYYZ', 'CYTZ']

metar_stations = {
'CYTZ': {'report': 'ftp://tgftp.nws.noaa.gov/data/observations/metar/stations/CYTZ.TXT', 'target': 'https://weather.gc.ca/en/location/index.html?coords=43.627,-79.394'},
'CYYZ': {'report': 'ftp://tgftp.nws.noaa.gov/data/observations/metar/stations/CYYZ.TXT', 'target': 'https://weather.gc.ca/en/location/index.html?coords=43.655,-79.383'},
}

fpcn = {
'short-term': {'url': 'http://www.weather.gc.ca/data/forecast/fpcn11.cwto.html',
                        'id': 'FPCN11', 'headregex': re.compile('^FPCN11'),
                        'locregex': re.compile('^City of Toronto')},
'long-term': {'url': 'http://www.weather.gc.ca/data/forecast/fpcn51.cwto.html',
                        'id': 'FPCN51', 'headregex': re.compile('^FPCN51'),
                        'locregex': re.compile('^City of Toronto')},
'marine': {'url': 'http://www.weather.gc.ca/data/forecast/fqcn13.cwto.html',
                        'id': 'FQCN13', 'headregex': re.compile('^FQCN13'),
                        'locregex': re.compile('Western Lake Ontario|^Lake Ontario')},
'marine-lt': {'url': 'http://www.weather.gc.ca/data/forecast/fqcn53.cwto.html',
                        'id': 'FQCN53', 'headregex': re.compile('^FQCN53'),
                        'locregex': re.compile('Western Lake Ontario|^Lake Ontario')},
}

