#!/usr/bin/python3
import cgitb
import codecs
import config
from rss_display import *
from weather_display import *
from bookmarks import *
from urllib.parse import quote_plus


# Sets output encoding to utf-8, and enables cgitb
def init_cgi():
  cgitb.enable()


# Prints the page header
def page_header():
  print("Content-Type: text/html;charset=utf-8")
  print('')
  print('''<html>
             <head>
  
               <title>
                 Utility Page.
               </title>
  
               <link rel="stylesheet" href="homepage.css" type="text/css">
               <link rel="shortcut icon" href="https://juicy.melon.org/favicon.ico">
  
               <style type="text/css"> <!--
                 a.dir {font-weight: bold;}
                 a.bm {font-weight: normal; color:#00dd00;}
               --> </style>
           
               <script type="text/javascript"> <!--
           
                 function exp_coll(index)
                 {
                   s = document.getElementById("list_"+index);
           	if (s.style.display == 'none')
           	{
           	  s.style.display = 'block';
           	}
           	else if (s.style.display == 'block')
           	{
           	  s.style.display = 'none';
           	}
                 }
           
                 function exp(index)
                 {
                   s = document.getElementById("list_"+index);
           	if (!s) return false;
           	s.style.display = 'block';
                 }
           
                 function coll(index)
                 {
                   s = document.getElementById("list_"+index);
           	if (!s) return false;
           	s.style.display = 'none';
                 }
           
                 function coll_all()
                 {
                 }
           
               --> </script>
           
             </head>''')


# Provides the toolbar (should be exported to a module)
def toolbar():
  print('''<div id="toolbar">

           <form target="_blank" name="search" action="toolbar.py" method="post">
             <select name="search">''')
  for search in config.toolbar_searches:
    search_key = quote_plus(search[0])
    print(f'<option value="{search_key}">{search[0]}</option>')
  print('''</select>
             <input size=30 name="query" class="search" value="" title="Search Field">
             <input type="submit" class="destroy" value="S">
             -
             <input type="reset" class="destroy" value="D">''')
  for bookmark in config.toolbar_bookmarks:
    print(f'- <a href="{bookmark[1]}">{bookmark[0]}</a>')
  print('''</form>
     
           </div>''')


# Provides the sidebar
def sidebar():
  print('<div id="sidebar">')
  bookmark_list = "<br>\n".join(f'<a href="{bookmark[1]}">{bookmark[0]}</a>\n' for bookmark in config.sidebar_bookmarks)
  print(bookmark_list)
  bms = bookmarks()
  bms.juicy_bookmarks()
  print('</div>')


# Provides weather data (should done as a module)
def weather():
  disp = weather_display()
  disp.juicy_display_weather()


# Provides RSS feeds
def rss_feeds():
  disp = rss_display()
  disp.juicy_feed_entries(20, 0)
  print('<hr>')


def footer():
  print('''</div>
           </body>
           </html>''')


init_cgi()
page_header()
print('<body>')
toolbar()
sidebar()
print('<div id="meat">')
weather()
rss_feeds()
footer()
