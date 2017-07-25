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
#
# NOTES
# Does not run in the background. So, users must setup an external scheduler to
# run this script periodically.
#
# USAGE
# ./b64_pycurl_forwarder_client.py --path  /path/to/file(s) 
#                                  --url   https://www.example.com
#                                  --ca    /path/to/ca/certificate/chain.crt
#                                  --cert  /path/to/client.crt 
#                                  --key   /path/to/client.key
# REQUIRED OPTIONS
# --path  /path/to/file(s)
# Specify the absolute path to a single file or a directory of files.  
# 
# --url   https://www.example.com
# Specify the HTTPS URL that PyCURL uses to upload your files. 
#
# --ca    /path/to/ca/certificate/chain.crt
# Specify the absolute path to CA certificates that PyCURL uses to verify
# HTTPS URLs.
#
# See https://serverfault.com/questions/485597/default-ca-cert-bundle-location
#
# OPTIONAL OPTIONS
# --cert  /path/to/client.crt
# Specify the absolute path to your TLS Certificate (PEM formatted type) that
# PyCURL uses to setup private TLS encryption over HTTPS.    
# 
# --key   /path/to/client.key
# Specify the absolute path to your TLS Key (PEM formatted type) that PyCURL
# uses to verify your TLS Certificate.
################################################################################

# start of script
if __name__ == "__main__":
  # import required modules 
  try:
    import sys
    import b64_pycurl_forwarder_check
    import b64_pycurl_forwarder_records
    import b64_pycurl_forwarder_session
  except ImportError:
    print("FAILURE: Failed to import required library modules for b64_pycurl_forwarder_client")
    sys.exit()
  # call functions
  b64_pycurl_forwarder_check.required_options()
  b64_pycurl_forwarder_check.optional_options()
  b64_pycurl_forwarder_records.create_record_file()
  b64_pycurl_forwarder_records.create_records()
  b64_pycurl_forwarder_records.update_file_sizes()
  b64_pycurl_forwarder_session.file_updates()
  sys.exit()

