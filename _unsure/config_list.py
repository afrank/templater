#!/usr/bin/python

import ConfigParser
import sys
import os
import string

def return_value (c, header, key, header_2 = ""):
	if header in c and key in c[header]:
		return c[header][key]
	elif header_2 and header_2 in c and key in c[header_2]:
		return c[header_2][key]
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
config.read("manifest.conf")

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
	config_list += ["/contexts/%s.xml" % service]

if return_value(config._sections,service,"failover_hibernate_config") == "true":
	config_list += ["hibernate.cfg.xml.primary","hibernate.cfg.xml.secondary"]
elif return_value(config._sections,service,"hibernate_config") == "true":
	config_list += ["hibernate.cfg.xml"]

if return_value(config._sections,service,"failover_instance_config") == "true":
	config_list += ["%s.config.primary" % service,"%s.config.secondary" % service]
elif return_value(config._sections,service,"instance_config") == "true":
	config_list += ["%s.config" % service]

if return_value(config._sections,service,"init_scripts") == "true":
	# this is such a sad and sorry way of doing this
	config_list += ["startService.sh","stopService.sh","../../../../etc/init.d/flurry_%s" % service]

for c in config_list:
	alias = return_value(config._sections,c,"alias")
	if alias:
		name = alias
	else:
		name = c
	relpath = return_value(config._sections,c,"relpath",service)
	if relpath == '/':
		relpath = ''
	dest = "%s/%s" % (relpath,name)
	print dest

#print config_list
