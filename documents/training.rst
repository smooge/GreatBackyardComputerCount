==============================================
 Great Backyard Computer Count Training Guide
==============================================

General Information
===================

1. Purpose
----------

   This document covers the general usage guide for running the Great
   Backyard Computer Count software to run as a stand alone network
   server or against existing Apache logs as produced by MirrorManager
   or similar software.

   The document is current as of the 0.5 version as tagged in the main
   github repository
   https://github.com/smooge/GreatBackyardComputerCount 

2. System Overview
------------------

   The software is run inside of Fedora Infrastructure and related
   organizations to allow for more accurate counting of systems
   getting updates for Fedora, EPEL, and CentOS operating systems. 

   The code is currently written in Python 2.7 and runs in a CentOS 7
   environment. Future versions will be rewritten to work with Python
   3.x as needed. In order to ensure that the installation and usage
   is able to be replicated, all minimum requirements for libraries
   are included in the requirements.txt file.

   The current software author and point of contact is Stephen Smoogen
   <smooge@fedoraproject.org> and tickets can be opened for feature
   requests or problems in the upstream source code repository.

3. Document References
----------------------

   * Great Backyard Computer Count (GBCC)
       https://github.com/smooge/GreatBackyardComputerCount/ 
   * Fedora Project https://getfedora.org/
   * CentOS Linux https://centos.org/
   * Fedora Infrastructure https://pagure.io/fedora-infrastructure/
   * Mirror manager https://github.com/fedora-infra/mirrormanager2/ 

4. Training Prerequisites
-------------------------

   For installation and maintenance of the software, a moderate
   knowledge of Python, databases, and how the site uses mirror
   manager or similar software to store existing files.

   For usage of the command line tool, all that is needed is to know
   where the related log files are.

   For viewing current data counts, the ability to use a web browser,
   a knowledge of where the GBCC server is running, and having proper
   access (accepted login/password) to that website.

5. Installation Training
------------------------

   We will go over how to install the software in a standalone testing
   mode. First you will need to have a Linux operating system with
   Python 2.7 installed on it. All testing was done on CentOS 7.5 so
   that will be the version used in the documentation.

   1. Install OS and set up basic user.
   2. Install the software packages git and set up python virtual
      environment.

```
   $ sudo -i 
   Password: <>
   # yum install epel-release
   # yum install git python-virtualenv python2-geoip2
   # exit
   $ virtualenv-2.7 GBCC_walkthrough
   $ source GBCC_walkthrough/bin/activate
   $ git clone https://github.com/smooge/GreatBackyardComputerCount.git

```
   3. Download a copy of the MaxmindDB geolocation database you want
      to use. Testing was done with a paid copy but the free version
      should also work:
 
      https://dev.maxmind.com/geoip/geoip2/geolite2/

   4. Edit the default configs to the appropriate directories for your
      site. 

```
   (GBCC_walkthrough) $ cd GreatBackyardComputerCount
   (GBCC_walkthrough) $ vi GreatBackyardComputerCount/config.py

```
   change the values of basedir and any other variables needed. It
   defaults to useing the basedir as the tree for logfiles and such.

   5. You can now set the working environment with pip

```
   (GBCC_walkthrough) $ pip install -r requirements.txt

```

   6. To test that the program will work, you can now test the
      operation of the basic log analysis tool:

```
(GBCC_walkthrough) $ python mirror-analysis.py -C -S test-data/test-data
usage: mirror-analysis.py [-h] [-v] (-C | -S) [-o OUTPUT] [-G]
                          files [files ...]
mirror-analysis.py: error: argument -S/--SQL: not allowed with argument -C/--CSV

(GBCC_walkthrough) $ python mirror-analysis.py -C test-data/test-data
(GBCC_walkthrough) $ ls ../*csv
../GBCC.csv
(GBCC_walkthrough) $ head ../GBCC.csv
"Date","IP","Country","UUID","OS","Variant","Release","Arch","ClientApp"
"2018-05-31 04:02:41","152.19.134.142","unknown","ffffffff-ffff-4fff-bfff-ffffffffffff","el","unknown","el07","x86_64","yum"
"2018-05-31 04:02:49","2604:1580:fe00:0:dead:beef:cafe:fed1","unknown","ffffffff-ffff-4fff-bfff-ffffffffffff","el","unknown","el07","x86_64","yum"
"2018-05-31 04:02:54","152.19.134.142","unknown","ffffffff-ffff-4fff-bfff-ffffffffffff","el","unknown","el07","x86_64","yum"
"2018-05-31 04:02:54","152.19.134.142","unknown","ffffffff-ffff-4fff-bfff-ffffffffffff","el","unknown","el07","x86_64","yum"
"2018-05-31 04:02:58","152.19.134.142","unknown","ffffffff-ffff-4fff-bfff-ffffffffffff","fedora","unknown","f27","x86_64","dnf"
"2018-05-31 04:03:02","8.43.85.67","unknown","ffffffff-ffff-4fff-bfff-ffffffffffff","el","unknown","el07","x86_64","yum"
"2018-05-31 04:03:04","152.19.134.142","unknown","ffffffff-ffff-4fff-bfff-ffffffffffff","el","unknown","el07","x86_64","yum"
"2018-05-31 04:03:17","2610:28:3090:3001:dead:beef:cafe:fed3","unknown","ffffffff-ffff-4fff-bfff-ffffffffffff","fed_mod","unknown","f28","x86_64","dnf"
"2018-05-31 04:03:40","8.43.85.67","unknown","ffffffff-ffff-4fff-bfff-ffffffffffff","el","unknown","el07","x86_64","yum"


```

   7. Next we initialize the databases. By default the system uses
      sqlite for its usage. Further work would be needed to make it
      works with postgres or mysql. 

```
(GBCC_walkthrough)$ python ./initialize_db.py

```

   8. Log data can now be imported into the data base. Data usually
      has the form the apache common log format with the important
      data being on entry 7: /mirrorlist?repo=epel-7&arch=x86_64

```
152.19.134.142 - - [31/May/2018:04:02:41 +0000] "GET /mirrorlist?repo=epel-7&arch=x86_64 HTTP/1.1" 200 2701 "-" "urlgrabber/3.10 yum/3.4.3"

```
      This says what kind of request was made (asked for mirrorlist
      versus metalink) What the repository was (repo=epel-7) and what
      the architecture of the data was (arch=x86_64).

      Other data is taken from the ip address, and the last area which
      is the string data of which client was used.

   9. Data can now be imported into the database using the
      mirror-analysis script

```
(GBCC_walkthrough)$ python ./mirror-analysis.py -S -G test-data/test-data

(GBCC_walkthrough)$ sqlite3 ../GBCC.db
SQLite version 3.7.17 2013-05-20 00:56:22
Enter ".help" for instructions
Enter SQL statements terminated with a ";"
sqlite> .tables
Events           LU_Country       LU_Release
LU_Architecture  LU_IPAddress     LU_UUID
LU_ClientApp     LU_OS            LU_Variant

sqlite> select * from Events LIMIT 30;
1|1970-01-02 01:00:00.000000|1|1|1|1|1|1|1|1
2|1970-01-02 01:00:01.000000|1|1|1|1|1|1|1|1
3|1970-01-02 01:00:02.000000|6|1|1|17|239|2|2|10
4|2018-05-31 04:02:41.000000|6|9|39|1|239|3|1|10
5|2018-05-31 04:02:49.000000|6|9|39|1|239|4|1|10
6|2018-05-31 04:02:54.000000|6|9|39|1|239|3|1|10
7|2018-05-31 04:02:58.000000|6|2|28|1|239|3|1|5
8|2018-05-31 04:03:02.000000|6|9|39|1|239|5|1|10
9|2018-05-31 04:03:04.000000|6|9|39|1|239|3|1|10
10|2018-05-31 04:03:17.000000|6|1|29|1|239|6|1|5
11|2018-05-31 04:03:40.000000|6|9|39|1|239|5|1|10
12|2018-05-31 04:03:47.000000|6|9|39|1|239|3|1|10
13|2018-05-31 04:04:38.000000|6|9|39|1|239|5|1|10
14|2018-05-31 04:04:47.000000|6|9|39|1|239|3|1|10
15|2018-05-31 04:05:15.000000|6|9|39|1|239|5|1|10
16|2018-05-31 04:05:27.000000|6|9|39|1|239|3|1|10
17|2018-05-31 04:05:28.000000|6|9|39|1|239|4|1|10
18|2018-05-31 04:05:40.000000|6|9|39|1|239|3|1|10
19|2018-05-31 04:05:56.000000|6|9|39|1|239|5|1|10
20|2018-05-31 04:06:04.000000|6|9|39|1|239|3|1|10
21|2018-05-31 04:06:18.000000|6|9|39|1|239|3|1|10
22|2018-05-31 04:06:29.000000|6|2|29|1|239|3|1|5
23|2018-05-31 04:06:42.000000|6|2|29|1|239|3|1|5
24|2018-05-31 04:07:53.000000|6|9|39|1|239|6|1|10
25|2018-05-31 04:08:11.000000|6|9|39|1|239|5|1|10
26|2018-05-31 04:08:35.000000|6|9|39|1|239|7|1|10
27|2018-05-31 04:08:56.000000|6|9|39|1|239|3|1|10
28|2018-05-31 04:09:06.000000|6|9|39|1|239|3|1|10
29|2018-05-31 04:09:28.000000|6|9|39|1|239|3|1|10
30|2018-05-31 04:09:58.000000|6|9|39|1|239|3|1|10


```
      Currently this can take a long time because of the combined
      slowness of sql lookup/inserts in SQL-lite and the GEOIP
      lookups. A 13 MB file can take 40 minutes to load. 


6. Application Running
----------------------

Once the application has been setup it can be run as a webserver using
the supplied command: runserver.py. This will use the python built in
webserver and look for requests on port 5000. This can now be checked
with a browser going to http://<ipaddress>:5000/data/ which will give
pages for what can be currently queried from the database. Checkins
can now also be done with clients using a yum repository file:

```

[census]
name=A Test URL for Census
mirrorlist=http://<ipaddress>:5000/census?os=$census_os&variant=$census_variant&release=$releasever&arch=$basearch&uuid=$census_uuid
enabled=1
skip_if_unavailable=true


```

This is not useful for more than testing and full scale implementation
will require using a proxy system which will relay data to the backend
server.

