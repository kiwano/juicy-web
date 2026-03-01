#!/usr/bin/python

import config

class bookmarks():

  def __init__(self):
    with open(config.bookmarkfile, "r") as f:
      self.bookmarklines = f.readlines()

  def juicy_bookmarks(self):
    print('<ul style="list-style-type:none; margin:0; padding:0;">')
    print('<li><a href="javascript:exp_coll(100);">Bookmarks</a>')
    print('<ul id="list_100" style="list-style-type:none; padding:10; display:none">')
    folder_id = 101
    line_counter = 0
    for line in self.bookmarklines:
      parts = line.split(' ', 1)
      line_counter += 1
      if len(parts) != 2:
        print('<li>----</li>')
        continue
      url = parts[0]
      name = parts[1].strip('\n')
      if url == 'folder':
        #print('folder: ' + name + '(' + str(folder_id) + ')')
        print('<li><a class="dir" href="javascript:exp_coll(' + str(folder_id) + ');">' + name + '</a>')
        print('<ul id="list_' + str(folder_id) + '" style="list-style-type:none; padding:10; display:none">')
        folder_id += 1
        continue
      if url == 'endfolder':
        print('</ul></li>')
        continue
      print('<li><a class="bm" href="' + url + '">' + name + '</a></li>')
    print('</ul></li>')
    print('</ul>')
