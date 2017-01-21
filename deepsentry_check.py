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
  print("FAILURE: Failed to import required modules deepsentry_check")
  sys.exit()

# globals
CLIENT_API_KEY = False
CLIENT_LOG_PATHNAME = False
CLIENT_TLS_CERTIFICATE = False

# try checking format of the required options, else throw errors then display
# failure message and exit.
def required_options():
  # check number of arguments
  try:
    if len(sys.argv) != 3:
      raise IOError
    else:
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
        # check format of api key
        elif sys.argv[i] == "--key":
          try:
            if re.match("[a-zA-Z1-9]{5}\-[a-zA-Z1-9]{5}\-[a-zA-Z1-9]{5}\-[a-zA-Z1-9]{5}\-[a-zA-Z1-9]{5}", sys.argv[i+1]):
              CLIENT_API_KEY = str(sys.argv[i+1])
            else:
              raise ValueError
          except ValueError:
            print("FAILURE: Invalid format for --interval %s" % sys.argv[i+1])
            sys.exit()
        # increment while loop
        i = i + 1
  except IOError:
    print("FAILURE: Invalid options for deepsentry_client.py")
    print("Usage: ./deepsentry_client.py --key XXXXX-XXXXX-XXXXX-XXXXX-XXXXX --path /path/to/log(s)")
    sys.exit() 

# if user specified a client.cert and client.key, set TLS_CERTIFICATE to true.
# else set TLS_CERTIFICATE to false to use only server-side encryption.
def optional_options():
  files_list = []
  # cert flags
  cert_exists = False
  key_exists = False
  i = 1
  while i < len(sys.argv):
    # check client TLS certificate exists
    if sys.argv[i] == "--certfile":
      try:
        if os.path.exists(sys.argv[i+1]):
          files_list.append(str(sys.argv[i+1]))
          cert_exists = True
        else:
          raise IOError
      except IOError:
        print("ERROR: Path to TLS Certificate not found %s" % sys.argv[i+1])
    # check client TLS certificate key exists
    if sys.argv[i] == "--certkey":
      try:
        if os.path.exists(sys.argv[i+1]):
          files_list.append(str(sys.argv[i+1]))
          key_exists = True
        else:
          raise IOError
      except IOError:
        print("ERROR: Path to TLS Certificate Key not found %s" % sys.argv[i+1])
    # increment while loop
    i = i + 1
  # update global
  if cert_exists == True and key_exists == True:
    CLIENT_TLS_CERTIFICATE = []
    CLIENT_TLS_CERTIFICATE = list(set(files_list))
  else:
    CLIENT_TLS_CERTIFICATE = False
  # required clean up
  del files_list
  sys.exit()

# remove code from Python runtime  
del required_options
del optional_options

