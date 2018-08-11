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

   6. To test that the 
