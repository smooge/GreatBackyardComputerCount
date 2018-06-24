=============================
Great Backyard Computer Count
=============================
.. image:: ./images/Bearguins.jpg
    :scale: 50%
    :align: center
    :alt: Bearguins on a beach. 

Art created by Sarah Richter <info@sarah-richter-illustration.de>. Licensed under Creative Commons 3 Share-Alike.


The Great Backyard Computer Count is a project to improve the ways
that the Fedora Project counts its users.

Background
==========

In order for a community to know which products it should invest in,
it needs to have an understanding of which ones are being used and
where. The Fedora Project gathers its usage statistics using IP
address hits from the update tool. This masks when multiple servers
are behind a proxy or when a host moves from ip address to another due
to network changes. The data is then placed in flat files which can
take days to reanalyze old data in order to make new queries of “what
country is growing”, “what architecture and release are shrinking”, or
“what are the combined trends of that data”. Finally the data is
massaged further to draw graphs of usage via shell scripts.

The Great Backyard Computer Count (GBCC) is meant to address these
concerns and some others. First by adding a UUID plugin to the system
update utility, users can be better counted. Second by moving most of
the data into an SQL database, better queries can be done ‘on the fly’
as they are needed. Also new architectures can be found and added to
the database as needed without needing to reprocess old data. Finally
by automating some of the graphing and data collection, the data can
be shown in a web interface to the people needing access.

Current Software Methodology
============================

Currently the software system is broken into several different chunks:

Mirror System
~~~~~~~~~~~~~

1. The Fedora Project generates a release which is put onto various
   HTTP servers around the world. 
2. This is then mirrored by volunteer websites around the world which
   register with the Fedora Project’s mirrormanager service. 
3. The end-consumers download and install the Fedora Project or the
   CentOS Project operating systems. 
4. The end-consumer’s system checks for updates or additional packages
   needed using one of the following utilities: yum, dnf, or
   PackageKit. 
5. These utilities ask the website ‘mirrors.fedoraproject.org’ where
   the nearest mirror is to get updates. This is a series of proxy
   systems around the world which may have limited access to the
   central Fedora Project but get regular updates on which sub-mirrors
   are ‘up2date’. 
6. The mirror looks up the IP address of the user, checks to see what
   network mirrors are probably closest, and then gives a list of
   mirrors that the end-consumer should check 
7. The mirror’s httpd process logs this to a log file using standard
   Apache log format. The data stored is the date, IP address,
   hardware architecture, and repository version requested by the
   consumers command. 

Data Analysis System
~~~~~~~~~~~~~~~~~~~~

1. Daily each proxy is checked to see if its daily logs are available
   and are then copied over to a central log server.
2. The log server then consolidates these logs into a central file on
   a Network File System (NFS) which is mounted by other systems to do
   further analysis. 
3. One of the systems does a set of analysis via awstats and a set of
   perl/python/awk scripts which give a crude count of what systems
   are checking in per day. 

Proposed Software Methodology
=============================
The Great Backyard Computer Count will add some data to the Mirror
System and alter the Data Analysis steps greatly.

Mirror System
~~~~~~~~~~~~~

1. A repository will be made available which will count as a census
   tool. This repository will have a script which determines what the
   OS, variant, uuid of the system is and puts them as variables that
   can be relayed to a mirror server.

2. The proxy systems will log the two additional data points in
   standard Apache format.

Backend Data Analysis
~~~~~~~~~~~~~~~~~~~~~

1. For the first version of GBCC, data will be still gathered and
   consolidated in the same method as before. Adding in ways to
   centralize and make real time data reports is a later goal.
2. The data analysis scripts will do an analysis of the last days logs
   a. It will go through each line and validate the content for known
      releases, variants, architectures, and UUIDs 
   b. It will insert into the tables a count of the times that a UUID
      checked in per day.
   c. It will update counts for other data as needed for reports.
3. Because logs can grow to large amounts, a garbage collection will
   be done where after N months, old tables will be archived and
   dropped. These can be either rerun later or recovered from backup
   as needed.

Front End Tools
~~~~~~~~~~~~~~~

1. An administrative tool will be made available to add new
   architectures, releases, and variants to the database as needed.

2. Because new data may need to be added to deal with old logs, an
   administrative tool to rerun the data-analysis on old logs will be
   made. This will ‘flush’ existing data after some set time, and then
   rerun the data-analysis on those days.

3. A reporting tool will be made available which will give the
   following graphs:
   a. Total count for each arch 
   b. Total count for each version
   c. Total count for each variant
   d. Total count per country
   e. Reports crossing the above data (count for arch && country,
      count for arch && version, etc).
