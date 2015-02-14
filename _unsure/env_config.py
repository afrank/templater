#!/usr/bin/python

import ConfigParser
import sys
import os
import string

if len(sys.argv) < 3:
	print "must provide service and environment"
	exit(0)

service = sys.argv[1]
env = sys.argv[2]

config = ConfigParser.ConfigParser()
config.optionxform = str
config.read("environments.conf")

if not env in config._sections:
	print "Could not find your environment."
	exit(0)

res = config._sections[env]

if service in res:
	print string.replace(res[service],',',' ')
	exit(0)

if "defaults" in config._sections:
	keys = config._sections["defaults"].keys()
	for k in keys:
		svc_list = string.replace(config._sections["defaults"][k],' ','').split(',')
		if service in svc_list:
			print string.replace(res[k],',',' ')
			exit(0)

if "default" in res:
	print string.replace(res["default"],',',' ')
	exit(0)

print "Could not find any hosts in %s for %s" % (env,service)
exit(2)
