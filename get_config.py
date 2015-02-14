#!/usr/bin/python

import ConfigParser
import sys
import os
import string
from glob import glob
from string import Template

if len(sys.argv) < 3:
	print "must provide config file and a comma-delimited list of inheretence keys"
	exit(0)

config_file = sys.argv[1]
keys = string.replace(sys.argv[2],' ','').split(',')

keys += ["default"]

config_base = 'template/configs'
template_base = 'template/templates'

ini = '%s.ini' % config_file
#template = '%s/%s.tmpl' % (template_base,config_file)
for tmpl in os.walk(template_base,topdown=False):
	if '%s.tmpl' % config_file in tmpl[2]:
		template = '%s/%s.tmpl' % (tmpl[0],config_file)
		break

if not os.path.isfile(template):
	print "I don't have a template for that config. Sorry."
	exit(0)

t = open(template,'r').read()
s = Template(t)

for p in os.walk(config_base,topdown=False):
	if config_file+'.ini' in p[2]:
		for key in keys:
			config = ConfigParser.ConfigParser()
			config.optionxform = str
			config.read("%s/%s.ini" % (p[0],config_file))
			if key in config._sections:
				t = s.safe_substitute(config._sections[key])
				s = Template(t)

print t

