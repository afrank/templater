#!/usr/bin/python

import ConfigParser
import sys
import os
import string

if len(sys.argv) < 3:
	print "must provide service and key"
	exit(0)

service = sys.argv[1]
key = sys.argv[2]

config = ConfigParser.ConfigParser()
config.optionxform = str
config.read("manifest.conf")

if not service in config._sections and not "default" in config._sections:
	print "Could not find your service."
	exit(0)

if service in config._sections:
	res = config._sections[service]
elif "default" in config._sections:
	res = config._sections["default"]
else:
	print "Could not find your service."
	exit(0)

if service in config._sections and key in config._sections[service]:
	print string.replace(config._sections[service][key],',','')
elif "default" in config._sections and key in config._sections["default"]:
	print string.replace(config._sections["default"][key],',','')
else:
	print "Could not find a key for %s %s" % (service,key)

