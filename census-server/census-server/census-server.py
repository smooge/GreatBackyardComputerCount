# -*- coding: utf-8 -*-

"""

This is the basic census server which gathers data from yum/dnf
clients querying from the internet. It then replies back a string of
mirrors that can be used to get the current repodata for the server.

"""

import logging
import geoip2.database
import geoip2.errors

from flask import Flask,request,abort

