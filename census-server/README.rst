====================================
Great Backyard Computer Count Server
====================================

The Great Backyard Computer Count Server is a simple flask application
which runs in a WSGI service. The application will take a connection
from a client system, parse the GET arguments for validity and then
log to a file the follwoing data:

Data (ISO Format), Server IP Address, Client IP Address, \
Geolocation of client, OS, OS Variant, Arch, UUID

Because this may run on multiple servers without connections to a
central database, the data will just be logged to a flat file in CSV
format. The data can then be combined at a central data analysis
server which will insert the data into a database as needed.

The server returns a minimal repomd.xml that acts as a metalink for a
'null' repository.

Software Required
=================

python 2.7 or python 3.4+

certifi==2018.4.16
chardet==3.0.4
click==6.7
Flask==1.0.2
geoip2==2.9.0
idna==2.6
ipaddress==1.0.22
itsdangerous==0.24
Jinja2==2.10
MarkupSafe==1.0
maxminddb==1.4.0
requests==2.18.4
six==1.11.0
urllib3==1.22
Werkzeug==0.14.1
