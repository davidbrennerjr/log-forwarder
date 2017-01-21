#!/usr/bin/python3.5

################################################################################
# deepsentry-client.py - Send deltas of file(s) over TLS to server 
#  
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
# Notes
# Deepsentry-client does not run in the background. So, users must setup an
# external scheduler to run this script periodically.
#
# Usage
# ./deepsentry-client.py options --key generated_api_key --path /path/to/log(s)
# --certfile /path/to/client.crt --certkey /path/to/client.key
################################################################################

# start of script
if __name__ == "__main__":
  # import required modules 
  try:
    import sys
    import deepsentry_check
    import deepsentry_records
    import deepsentry_session
  except ImportError:
    print("FAILURE: Failed to import required library modules for deepsentry_client")
    sys.exit()
  # call functions
  deepsentry_check.required_options()
  deepsentry_check.optional_options()
  deepsentry_records.create_record_file()
  deepsentry_records.create_records()
  deepsentry_records.update_file_sizes()
  deepsentry_session.file_updates()
  sys.exit()

