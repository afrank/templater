import ConfigParser
import sys
import os
import string
from glob import glob
from string import Template

if len(sys.argv) < 3:
	print "must provide service and environment"
	exit(0)

service = sys.argv[1]
env = sys.argv[2]
sub_env = None
if len(sys.argv) == 4:
	sub_env = sys.argv[3]

# get a list of the template files to use
for tf in glob('templates/*.tmpl'):
	basename = os.path.basename(tf)
	basename = string.replace(basename,'.tmpl','')
	t = open(tf,'r').read()
	s = Template(t)
	# discover the inheretence tree

	# if sub_env is defined, check that directory
	if sub_env is not None and os.path.isdir('configs/%s/%s' % (env,sub_env)):
		#print "[%s] configs/%s/%s exists and I'm going to try and parse it" % (basename,env,sub_env)
		# 1. check for a service-level config, which trumps all else
		if os.path.isfile('configs/%s/%s/%s.ini' % (env,sub_env,service)):
			#print "[%s] configs/%s/%s/%s.ini exists and I'm going to try and parse it" % (basename,env,sub_env,service)
			config = ConfigParser.ConfigParser()
			config.optionxform = str
			config.read('configs/%s/%s/%s.ini' % (env,sub_env,service))
			if basename in config._sections:
				t = s.safe_substitute(config._sections[basename])
				s = Template(t)
			if 'all' in config._sections:
				t = s.safe_substitute(config._sections['all'])
				s = Template(t)
		# 2. check for a config-level config
		if os.path.isfile('configs/%s/%s/%s.ini' % (env,sub_env,basename)):
			#print "[%s] configs/%s/%s/%s.ini exists and I'm going to try and parse it" % (basename,env,sub_env,basename)
			config = ConfigParser.ConfigParser()
			config.optionxform = str
			config.read('configs/%s/%s/%s.ini' % (env,sub_env,basename))
			if service in config._sections:
				t = s.safe_substitute(config._sections[service])
				s = Template(t)
			if 'all' in config._sections:
				t = s.safe_substitute(config._sections['all'])
				s = Template(t)
	# 3. check for a service-level config
	if os.path.isfile('configs/%s/%s.ini' % (env,service)):
		#print "[%s] configs/%s/%s.ini exists and I'm going to try and parse it" % (basename,env,service)
		config = ConfigParser.ConfigParser()
		config.optionxform = str
		config.read('configs/%s/%s.ini' % (env,service))
		if basename in config._sections:
			t = s.safe_substitute(config._sections[basename])
			s = Template(t)
		if 'all' in config._sections:
			t = s.safe_substitute(config._sections['all'])
			s = Template(t)
	# 4. check for a config-level config
	if os.path.isfile('configs/%s/%s.ini' % (env,basename)):
		#print "[%s] configs/%s/%s.ini exists and I'm going to try and parse it" % (basename,env,basename)
		config = ConfigParser.ConfigParser()
		config.optionxform = str
		config.read('configs/%s/%s.ini' % (env,basename))
		if service in config._sections:
			t = s.safe_substitute(config._sections[service])
			s = Template(t)
		if 'all' in config._sections:
			t = s.safe_substitute(config._sections['all'])
			s = Template(t)
	# 3. check for a service-level config
	if os.path.isfile('configs/%s.ini' % (service)):
		#print "[%s] configs/%s/%s.ini exists and I'm going to try and parse it" % (basename,env,service)
		config = ConfigParser.ConfigParser()
		config.optionxform = str
		config.read('configs/%s.ini' % (service))
		if basename in config._sections:
			t = s.safe_substitute(config._sections[basename])
			s = Template(t)
		if 'all' in config._sections:
			t = s.safe_substitute(config._sections['all'])
			s = Template(t)
	# 4. check for a config-level config
	if os.path.isfile('configs/%s.ini' % (basename)):
		#print "[%s] configs/%s/%s.ini exists and I'm going to try and parse it" % (basename,env,basename)
		config = ConfigParser.ConfigParser()
		config.optionxform = str
		config.read('configs/%s.ini' % (basename))
		if service in config._sections:
			t = s.safe_substitute(config._sections[service])
			s = Template(t)
		if 'all' in config._sections:
			t = s.safe_substitute(config._sections['all'])
			s = Template(t)


	# do a final string replace for some proprietary keys
	t = string.replace(t,'__SERVICE__',service)
	t = string.replace(t,'__ENV__',env)
	if sub_env is not None:
		t = string.replace(t,'__SUBENV__',sub_env)

	print "Writing output/%s/%s" % (service,basename)
	w = open('output/%s/%s' % (service,basename),'w')
	w.write(t)

