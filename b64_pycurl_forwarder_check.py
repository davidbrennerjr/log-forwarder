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
  import sys
  import os
  import re
except ImportError:
  print("FAILURE: Failed to import required modules b64_pycurl_forwarder_check")
  sys.exit()

# globals
CLIENT_HTTPS_URL = False
CLIENT_LOG_PATHNAME = False
CLIENT_CA_BUNDLE = False
CLIENT_TLS_CERT = False
CLIENT_TLS_KEY = False

# try checking format of the required options, else throw errors then display
# failure message and exit.
def required_options():
  # check number of arguments
  try:
    i = 1
    while i < len(sys.argv):
      # check path to log(s) exists
      if sys.argv[i] == "--path":
        try:
          if os.path.exists(sys.argv[i+1]):
            CLIENT_LOG_PATHNAME = str(sys.argv[i+1])
          else:
            raise IOError
        except IOError:
          print("FAILURE: Path to log(s) not found %s" % sys.argv[i+1])
          sys.exit()  
      # check path to ca bundle
      elif sys.argv[i] == "--ca":
        try:
          if os.path.exists(sys.argv[i+1]):
            CLIENT_CA_BUNDLE = str(sys.argv[i+1])
          else:
            raise IOError
        except IOError:
          print("FAILURE: Path to HTTPS CA Bundle not found %s" % sys.argv[i+1])
          sys.exit()        
      elif sys.argv[i] == "--url":
        CLIENT_HTTPS_URL = str(sys.argv[i+1])
      # increment while loop
      i = i + 1
  except IOError:
    print("FAILURE: Invalid options for b64_pycurl_forwarder_client.py")
    print("Usage: ./b64_pycurl_forwarder_client.py --url https://www.example.com --path /path/to/log(s) --ca /path/to/ca/certificate/chain.crt --cert /path/to/client.crt --key /path/to/client.key")
    sys.exit() 

# if user specified a client.crt and client.key, set TLS_CERT and TLS_KEY to true.
# else check for whether or not to use only server-side encryption.
def optional_options():
  i = 1
  while i < len(sys.argv):
    # check client TLS certificate exists
    if sys.argv[i] == "--cert":
      try:
        if os.path.exists(sys.argv[i+1]):
          CLIENT_TLS_CERT = str(sys.argv[i+1])
        else:
          raise IOError
      except IOError:
        print("ERROR: Path to TLS Certificate not found %s" % sys.argv[i+1])
    # check client TLS certificate key exists
    if sys.argv[i] == "--key":
      try:
        if os.path.exists(sys.argv[i+1]):
          CLIENT_TLS_KEY = str(sys.argv[i+1])
        else:
          raise IOError
      except IOError:
        print("ERROR: Path to TLS Certificate Key not found %s" % sys.argv[i+1])
    # increment while loop
    i = i + 1

# remove code from Python runtime  
del required_options
del optional_options

