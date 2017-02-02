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
  import requests
except ImportError:
  print("FAILURE: Failed to import required modules for deepsentry_session")
  sys.exit()

# import required globals
try:
  from deepsentry_check import CLIENT_API_KEY
  from deepsentry_check import CLIENT_LOG_PATHNAME
  from deepsentry_check import CLIENT_TLS_CERTIFICATE
except NameError:
  print("FAILURE: Failed to import required globals from module deepsentry_check")
  sys.exit()
  
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

# FIXME: when client has certificate and key use HTTPS and Allowed IP Address
# (server-side) + TLS Certificate and TLS Key (client-side). when client isn't
# using a certificate or the certificate/key is invalid, use only server-side
# encryption. 
def send_file_updates(path="", size=0, offset=0):
  # Requests may attempt to provide the Content-Length header for you, and if it
  # does this value will be set to the number of bytes in the file. Errors may
  # occur if you open the file in text mode.
  fd = open(path, "rb") 
  fd.seek(offset, 1)
  fd.read()
  # FIXME: can't use httplib/urllib (too buggy, platform dependent). can't use requests
  # (too buggy, requires req/res be JSON formatted). Use PyCURL?
  session = requests.session()
  #url = "https://www.deepsentry.com/rest/logs/save?id=%s" % CLIENT_API_KEY
  url = "https://192.168.1.109/save?id=%s" % CLIENT_API_KEY
  certfile = ""
  certkey = ""
  # check for certificate and key
  if CLIENT_TLS_CERTIFICATE != False:
    for path in CLIENT_TLS_CERTIFICATE:
      if ".cert" in path:
        certfile = path
      if ".key" in path:
        certkey = path
    req = requests.request('PUT', url, files=fd, cert=(certfile, certkey), allow_redirects=False)
    content = req.prepare()
    res = session.send(content, verify=True)  
  else: 
    print("ok") 
    req = requests.request('PUT', url, files=fd, allow_redirects=False)
    content = req.prepare()
    res = session.send(content, verify=False)
  # check response
  if res.status_code == requests.codes.ok:
    length = size
  else:
    length = 0
  fd.close()
  return(length)
  
# if content sent is 0, send file. if size not equal to content sent, get
# starting position of diff then send diff. update data in json file.  
def file_updates():
  count = next_record_number()
  # get data from records file
  fd = open("deepsentry_records.json", "r")
  data = json.load(fd)
  fd.close()
  # loop through records: if sent content is 0, send entire file. if sent
  # content is not 0, send deltas.   
  for counter in range(0, count-1):
    set = []
    set = data[counter]
    counter = counter + 1
    # get pathname
    key = "%s pathname" % counter
    path = set[key]
    # get size. controls how much data is actually sent via sendfile().
    key = "%s size" % counter
    size = set[key]
    size = int(size)
    # get content sent. normally size will always be larger than sent (unless size
    # equals sent therfore file hasn't changed since last upload).
    key = "%s sent" % counter
    sent = set[key]
    sent = int(sent)
    # if content sent is 0, send file. else send delta.
    if sent is 0:
      length = send_file_updates(path, size, 0)
    else:
      # determine offset as next position in file to be uploaded
      offset = sent+1
      length = send_file_updates(path, size, offset)
    # check that content sent using sendfile() matches size of file, print error
    # message. update "sent" entry in JSON file with length.
    if length != size:
      syslog.syslog("ERROR: Couldn't upload file changes to server \"%s\" Attempted to send \"%d\" of file, but something went wrong." % (path, length))
    else:
      key = "%s sent" % counter 
      set[key] = length
    counter = counter - 1
    # update data
    data[counter] = set
    del set
  # update data in json file
  fd = open("deepsentry_records.json", "w")
  fd.write(json.dumps(data, fd, indent=4))
  fd.close()
  

