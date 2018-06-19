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

See requirements.txt for the versions this was built and tested with.
