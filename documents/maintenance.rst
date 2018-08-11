==================================================
Great Backyard Computer Count Maintenance and Todo
==================================================

This document covers items which must be completed for the product to
go from 0.5 to 1.0 release. 

1. SQL speedups. Currently the software is very slow on inserts due to
   the multiple lookups which are being done before this. The easiest
   solution will be to load each of the lookup pages into hash table
   with the name as the key and the pkid as the datum. This would cut
   down the number of lookups to the DB down by 5 (uuid and ip address
   will need to still be looked up or created). Another solution
   would be to put the insert into a store procedure which then
   requires that it is linked to the type of database used (aka mysql
   vs postgres vs...) Other speedups may be possible due to the data
   layout.

2. SQL Table updates (maintenance). Currently the database has no idea
   of which version it is running against. It will need to be
   refactored to use alembic versions so that future updates and
   changes to the database can be automated with outside scripts.

3. Adding lookups. Currently the SQL lookup tables require additional
   entries when new releases, architectures or other regular
   expressions are added. This will be something that needs to be
   added every several releases.

4. Database size maintenance. Currently we store every event in a log
   file as a seperate event. This means that our entire database would
   have around 146 billion events stored in the main table. That is
   incredibly unweildy and will need a way to either archive off or
   store only the data needed per day. Originally this was going to be
   a 'count' stat for the tuple (date, ip, uuid, arch, repo, variant,
   client) so that if that showed up 20 times it would only have 1
   record with a 20 in it. [This would cover the majority of duplicate
   records] However the speed to lookup and then update the record was
   slower than adding another record so we are doing a straight dump
   and then will do queries to cut out noise.

5. Graphing. Currently the data reports that are given are incredibly
   weak. Built in reports using specific queries and feeding to a
   javascript UI in the client fell out of scope for the initial
   timeline and will need to be implemented in the next section.

6. Testing. Currently all testing is done manually with limited
   failure modes. The next task will be to reimplement all code with a
   wrapper set of testunits on each routine. 

Date: 2018-08-11
Proposed 1.0 release date: 2018-12-11.
