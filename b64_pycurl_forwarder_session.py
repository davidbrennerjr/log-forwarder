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
  import pycurl
  import base64
except ImportError:
  print("FAILURE: Failed to import required modules for b64_pycurl_forwarder_session")
  sys.exit()

# import required globals
try:
  from b64_pycurl_forwarder_check import CLIENT_HTTPS_URL
  from b64_pycurl_forwarder_check import CLIENT_LOG_PATHNAME
  from b64_pycurl_forwarder_check import CLIENT_CA_BUNDLE
  from b64_pycurl_forwarder_check import CLIENT_TLS_CERT
  from b64_pycurl_forwarder_check import CLIENT_TLS_KEY
except NameError:
  print("FAILURE: Failed to import required globals from module b64_pycurl_forwarder_check")
  sys.exit()
  
# return next record number, highest numbered record plus one
def next_record_number():
  number = 0
  largest = 0
  fd = open("b64_pycurl_forwarder_records.json", "r")
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

# when server has certificate and key use HTTPS + TLS Certificate (client-side) + TLS Key (client-side).
# when client has only certificate, use HTTPS server-side encryption. 
def send_file_updates(path="", size=0, offset=0):
  fd = open(path, "rb")    
  fd.seek(offset, 1)
  fd_data = fd.read()
  fd_encoded = base64.b64encode(fd_data)
  # default: server-side encryption
  session = pycurl.Curl()
  session.setopt(session.VERBOSE, True)
  session.setopt(session.SSL_VERIFYPEER, 1)
  session.setopt(session.SSL_VERIFYHOST, 2)
  session.setopt(session.CAINFO, CLIENT_CA_BUNDLE)
  session.setopt(session.URL, CLIENT_HTTPS_URL)
  session.setopt(session.HTTPPOST, [(path,(session.FORM_BUFFERPTR,encoded,)),])
  # optional: client-side encryption
  if CLIENT_TLS_CERT != False and CLIENT_TLS_KEY != False:
    session.setopt(session.SSLCERTTYPE, "PEM")
    session.setopt(session.SSLCERT, CLIENT_TLS_CERT)
    session.setopt(session.SSLKEYTYPE, "PEM")
    session.setopt(session.SSLKEY, CLIENT_TLS_KEY)
  # run new session
  session.perform()    
  # check response
  if session.getinfo(session.RESPONSE_CODE) == 200:
    filesize_sent = size
  else:
    filesize_sent = 0
  session.close()
  fd.close()
  return(filesize_sent)
  
# if content sent is 0, send file. if size not equal to content sent, get
# starting position of diff then send diff. update data in json file.  
def file_updates():
  count = next_record_number()
  # get data from records file
  fd = open("b64_pycurl_forwarder_records.json", "r")
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
      size_sent = send_file_updates(path, size, 0)
    else:
      # determine offset as next position in file to be uploaded
      offset = sent+1
      size_sent = send_file_updates(path, size, offset)
    # check that content sent using sendfile() matches size of file, print error
    # message. update "sent" entry in JSON file with size_sent.
    if size_sent != size:
      syslog.syslog("ERROR: Couldn't upload file changes to server \"%s\" Attempted to send \"%d\" of file, but something went wrong." % (path, size_sent))
    else:
      key = "%s sent" % counter 
      set[key] = sent_size
    counter = counter - 1
    # update data
    data[counter] = set
    del set
  # update data in json file
  fd = open("b64_pycurl_forwarder_records.json", "w")
  fd.write(json.dumps(data, fd, indent=4))
  fd.close()
  
