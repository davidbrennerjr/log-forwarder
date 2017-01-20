#!/usr/bin/python3.5

################################################################################
# Copyright 2017 by David Brenner Jr <david.brenner.jr@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
################################################################################

# import required modules
try:
  import os
  import sys
  import time
  import calendar
  import json
  import re
  import syslog
except ImportError:
  print("FAILURE: Failed to import required modules for deepsentry_records")
  sys.exit()

# import required globals
try:
  from deepsentry_check import CLIENT_API_KEY
  from deepsentry_check import CLIENT_LOG_PATHNAME
except NameError:
  print("FAILURE: Failed to import required globals from module deepsentry_check")
  sys.exit()

# open existing record file or create new record file
def create_record_file():
  try:
    fd = open("deepsentry_records.json", "a")
    fd.close()
  except OSError:
    fd = open("deepsentry_records.json", "x")
    fd.close() 
  # json.dump() doesn't dump valid json. afterwards file "deepsentry_records.json"
  # has file size equal to 2.    
  if os.path.getsize("deepsentry_records.json") == 0:  
    fd = open("deepsentry_records.json", "w+")
    fd.write('[\n')
    fd.close()

# return next record number, highest numbered record plus one
def next_record_number():
  number = 0
  largest = 0
  fd = open("deepsentry_records.json", "r")
  data = fd.readlines()
  fd.close()
  for line in data:
    if "size" in line:
      number = str(number)
      number, _ = line.split(":")
      number = number.replace("size","")
      number = number.strip()
      number = number[1:-1]
      number = int(number)
    # keep largest number
    if largest < number:
      largest = number
    else:
      number = largest 
  count = largest + 1
  return(count)

# create records in file "deepsentry_records.json" of all files in target
# directory specified by user. ignore hidden folders and their files.
def create_records():
  count = next_record_number()
  fd = open("deepsentry_records.json", "a+")
  for root,dirs,files in os.walk("/tmp/tmpdir/", topdown=True, onerror=None, followlinks=True):
    files_list = []
    # get list of files
    for fname in files:
      files_list.append(os.path.realpath(os.path.join(root,fname)))
    # remove duplicates
    files_list = list(set(files_list))
    # create record for file  
    for name in files_list:
      if os.path.exists(os.path.realpath(os.path.join(root, name))):
        if os.path.getsize("deepsentry_records.json") != 2:
          data = fd.readlines()
          for line in data:
            if not os.path.realpath(os.path.join(root, name)) in line:
              pathname_name = "%s pathname" % count
              size_name = "%s size" % count
              checked_name = "%s checked" % count
              sent_name = "%s sent" % count
              json.dump({pathname_name:os.path.realpath(os.path.join(root, name)), size_name:os.path.getsize(os.path.realpath(os.path.join(root, name))), checked_name:calendar.timegm(time.gmtime()), sent_name:0}, fd, indent=4)
              # json.dump() doesn't dump valid json
              fd.write(',')
              fd.write('\n')
              count = count + 1
        else:
          pathname_name = "%s pathname" % count
          size_name = "%s size" % count
          checked_name = "%s checked" % count
          sent_name = "%s sent" % count
          json.dump({pathname_name:os.path.realpath(os.path.join(root, name)), size_name:os.path.getsize(os.path.realpath(os.path.join(root, name))), checked_name:calendar.timegm(time.gmtime()), sent_name:0}, fd, indent=4)
          # json.dump() doesn't dump valid json
          fd.write(',')
          fd.write('\n')            
          count = count + 1
    # required clean up
    del files_list
  # add trailing ']'
  fd.write(']\n')
  fd.close()
  # clean up '\n]]\n' caused by running twice
  fd = open("deepsentry_records.json", "r")
  data = fd.read()
  if "]]" in data:
    data = data[:-2]
  else:
    data = data[:-1]
  # clean up invalid json '},\n]\n'
  data = re.sub(r'},\n]', '}\n]', data)
  fd.close()
  fd = open("deepsentry_records.json", "w")
  fd.write(data)
  fd.close()

# update record file with latest sizes of every file
def update_file_sizes():
  count = next_record_number()
  # open records file
  fd = open("deepsentry_records.json", "r")
  data = json.load(fd)
  fd.close()
  # use pathnames from json file to update sizes
  for counter in range(0, count-1):
    set = []
    set = data[counter]
    counter = counter + 1
    # get size of file from pathname
    key = "%s pathname" % counter
    value = set[key]
    size = os.path.getsize(value)
    # update size of file
    key = "%s size" % counter
    set[key] = size
    # update timestamp
    key = "%s checked" % counter
    set[key] = calendar.timegm(time.gmtime()) 
    counter = counter - 1
    # update data
    data[counter] = set
    del set
  # update data in json file
  fd = open("deepsentry_records.json", "w")
  fd.write(json.dumps(data, fd, indent=4))
  fd.close()
 
sys.exit()

