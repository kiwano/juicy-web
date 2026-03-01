#!/usr/bin/python3

# searches to be incorporated in the search dropdown in the toolbar
toolbar_searches = [
  ['Google', 'https://www.google.com/search?q=%s'],
  ['Wikipedia', 'http://en.wikipedia.org/wiki/Special:Search?search=%s&go=Go'],
  ['Google Maps', 'https://www.google.ca/maps/search/%s/'],
  ['Youtube', 'https://www.youtube.com/results?search_query=%s'],
  ['IMDB', 'http://www.imdb.com/find?q=%s&s=all'],
  ['OED', 'http://www.chass.utoronto.ca.myaccess.library.utoronto.ca/patbin/new/oed-idx?query=%s&submit=Search&type=Lookup&size=First+100'],
  ['Debian', 'http://packages.debian.org/cgi-bin/search_packages.pl?keywords=%s&searchon=names&subword=1&version=all&release=all'],
]

# bookmarks to be displayed in the toolbar along the top of the page
toolbar_bookmarks = [
  ["QCYC", "http://www.qcyc.ca/"],
  ["Ferry", "http://www.torontoislandferryfinder.com/tiffWebApp/"],
  ["Meridian", "http://www.meridiancu.ca/"],
  ["Assante", "http://www.assante.com/"],
  ["Scotia", "https://www.scotiaonline.scotiabank.com/"],
  ["MyCardInfo", "https://meridian.mycardinfo.com/"],
  ["MBNA", "http://service.mbna.ca/"],
  ["Elevation", "https://elevationcpa.cchifirm.ca/clientportal/content/home"],
]

# unhideable bookmarks to be displayed in the sidebar above the bookmark director tree
sidebar_bookmarks = [
["Schedule", "https://unripe.melon.org/schedule.html"],
["Basic information", "https://unripe.melon.org/basicinfo.html"],
["My personal page", "https://unripe.melon.org/index.html"],
["Pics for linking", "https://unripe.melon.org/pictures/"],
["kiwano.melon.org", "https://kiwano.melon.org/"],
["Update kiwano", "https://kiwano.melon.org/wp-admin/post-new.php"],
]

bookmarkfile = "/home/kris/web/juicy/bookmarks"

db = "postgresql://juicy:4rft655@localhost/juicy"

weatherstations = ['CYTZ', 'CYYZ', 'CYHM', 'CYWA', 'KBOS']

metar_stations = {
'CYTZ': {'report': 'ftp://tgftp.nws.noaa.gov/data/observations/metar/stations/CYTZ.TXT', 'target': 'https://weather.gc.ca/en/location/index.html?coords=43.627,-79.394'},
'CYYZ': {'report': 'ftp://tgftp.nws.noaa.gov/data/observations/metar/stations/CYYZ.TXT', 'target': 'https://weather.gc.ca/en/location/index.html?coords=43.655,-79.383'},
'CYHM': {'report': 'ftp://tgftp.nws.noaa.gov/data/observations/metar/stations/CYHM.TXT', 'target': 'https://weather.gc.ca/en/location/index.html?coords=43.258,-79.869'},
'CYWA': {'report': 'ftp://tgftp.nws.noaa.gov/data/observations/metar/stations/CYWA.TXT', 'target': 'https://weather.gc.ca/en/location/index.html?coords=46.103,-77.495'},
'KBOS': {'report': 'ftp://tgftp.nws.noaa.gov/data/observations/metar/stations/KBOS.TXT', 'target': None},
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

