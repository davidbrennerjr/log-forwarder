# Base64 PyCURL Log Forwarder
Incrementally uploads files/logs as base64 encoded strings using PyCURL to a URL over HTTPS and optionally TLS Certs. Script does not run in the background. So, users must setup an external scheduler to run this script periodically.

# Usage
./b64_pycurl_forwarder_client.py --path  /path/to/file(s) 
                                 --url   https://www.example.com
                                 --ca    /path/to/ca/certificate/chain.crt
                                 --cert  /path/to/client.crt 
                                 --key   /path/to/client.key
# Required Options
--path  /path/to/file(s)
Specify the absolute path to a single file or a directory of files.

--url   https://www.example.com
Specify the HTTPS URL that PyCURL uses to upload your files. 

--ca    /path/to/ca/certificate/chain.crt
Specify the absolute path to CA certificates that PyCURL uses to verify HTTPS URLs. See https://serverfault.com/questions/485597/default-ca-cert-bundle-location

# Optional Options
--cert  /path/to/client.crt
Specify the absolute path to your TLS Certificate (PEM formatted type) that PyCURL uses to setup private TLS encryption over HTTPS.
 
--key   /path/to/client.key
Specify the absolute path to your TLS Key (PEM formatted type) that PyCURL uses to verify your TLS Certificate.
