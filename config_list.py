#!/usr/bin/python

import ConfigParser
import sys
import os
import string

def return_value (c, header, key):
	if header in c and key in c[header]:
		return c[header][key]
	elif "default" in c and key in c["default"]:
		return c["default"][key]
	else:
		return False


if len(sys.argv) < 2:
	print "must provide service"
	exit(0)

service = sys.argv[1]

config = ConfigParser.ConfigParser()
config.optionxform = str
config.read("template/manifest.conf")

if not service in config._sections and not "default" in config._sections:
	print "Could not find your service."
	exit(0)

config_list = return_value(config._sections,service,"config_list")
if config_list:
	config_list = string.replace(config_list,' ','').split(',')
else:
	print "could not get a config list"
	exit(0)

if return_value(config._sections,service,"context_config") == "true":
	config_list += ["%s.xml" % service]

if return_value(config._sections,service,"failover_hibernate_config") == "true":
	config_list += ["hibernate.cfg.xml.primary","hibernate.cfg.xml.secondary"]
elif return_value(config._sections,service,"hibernate_config") == "true":
	config_list += ["hibernate.cfg.xml"]

if return_value(config._sections,service,"failover_instance_config") == "true":
	config_list += ["instance.config.primary","instance.config.secondary"]
elif return_value(config._sections,service,"instance_config") == "true":
	config_list += ["instance.config"]

for c in config_list:
	alias = return_value(config._sections,c,"alias")
	if alias:
		name = alias
	else:
		name = c
	relpath = return_value(config._sections,c,"relpath")
	if relpath == '/':
		relpath = ''
	dest = "%s/%s" % (relpath,name)
	print dest

#print config_list
