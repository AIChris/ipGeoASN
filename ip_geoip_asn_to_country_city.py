# -*- coding: utf-8 -*-
import re
import sys
import datetime
import os
import socket

try:
	import geoip2.database
except Exception, e:
	print "\nerror import on geoip2.database --> "
	print str(e)
	print "\nsudo pip install geoip2"
	print "try this, ..."
	print "I do exit"
	sys.exit(1)

APP_PATH = os.path.dirname(os.path.abspath(__file__))
FOLDER = str("GeoLite2")

#FILE_CITY 	= str("GeoLite2-City.mmdb")
#FILE_AS 	= str("GeoLite2-ASN.mmdb")

CITY_DB  	= APP_PATH +str("/") +  FOLDER + str("/") + str("GeoLite2-City.mmdb")
AS_DB 		= APP_PATH  +str("/") +  FOLDER + str("/") + str("GeoLite2-ASN.mmdb")
DEBUG 		= False # True

def get_asn_name(ip):
	try:
		response = asn_open.asn(ip)
		as_name = response.autonomous_system_organization if response.autonomous_system_organization else "-"
		return as_name
	except Exception, e:
		if DEBUG:
			print "[Error-5] get_asn_name " + str(ip)
		return "N/A NAME"

def get_asn_num(ip):
	try:
		response = asn_open.asn(ip)
		as_num = response.autonomous_system_number if response.autonomous_system_number else "-"
		as_name = response.autonomous_system_organization if response.autonomous_system_organization else "-"
		return as_num
	except Exception, e:
		if DEBUG:
			print "[Error-4] get_asn_num " + str(ip)
		return "N/A AS"

def get_CC_country_code(ip):
	try:	
		response = city_open.city(ip)
		iso_code = response.country.iso_code if response.country.iso_code else "**"
		return iso_code
	except Exception, e:
		if DEBUG:
			print "[Error-9] get_CC_country_code " + str(ip)
		return "**"

def get_CC_country_code_city_name(ip): 
	try:
		response = city_open.city(ip)
		city_name = response.city.name if response.city.name else "City N/A in DB..."
		return city_name
	except Exception, e:
		if DEBUG:
			print "[Error-8] get_CC_country_code_city_name " + str(ip)
			print "[Error-8-a] get_CC_country_code_city_name " + str(e)
		return "N/A City"

def load_url(arg1):
	f = open( arg1, 'rb')
	print "ASN\t| IP\t\t    | CC | ASN Name \t\t\t  | CC_CITY"
	for line in f.readlines():
		if len(line.rstrip())  > 1:
			if check_valid_ip(line.rstrip()):
				AS_NUM = get_asn_num(line.rstrip())
				IP = '{:18s}'.format(line.strip())
				BGP = " N/A Imp...BGP"
				CC_COUNTRYCODE = get_CC_country_code(line.rstrip())
				REGISTRY = " N/A Imp.REGY"
				ALLOCATED = " N/A ALLOCA"
				try:
					AS_NAME = '{:30s}'.format(get_asn_name(line.rstrip()))
				except Exception, e:
					AS_NAME = "ErrorParse"

				CC_COUNTRYCODE_CITY = get_CC_country_code_city_name(line.rstrip())
				if len(str(AS_NUM)) <= 3:
					print ""  + str(AS_NUM) + str("\t\t| ")+ str(IP) + str("| ")  + str(CC_COUNTRYCODE) + str(" | ")  + AS_NAME.encode('utf-8')[0:30] + str(" | ") +CC_COUNTRYCODE_CITY.encode('utf-8')
				else:
					print ""  + str(AS_NUM) + str("\t| ")+ str(IP) + str("| ")  + str(CC_COUNTRYCODE) + str(" | ")  + AS_NAME.encode('utf-8')[0:30] + str(" | ") +CC_COUNTRYCODE_CITY.encode('utf-8')
			else:
				if DEBUG:
					print "[Error-3] " + str(arg1)

def check_valid_ip(ip):
	# todo support for https://tools.ietf.org/html/rfc1918 
	try:
		socket.inet_aton(ip)
		return True
	except socket.error:
		if DEBUG:
			print "[Error-1] not valid ip| " + str(ip)
		return False

if __name__ == '__main__':

	if not os.path.exists(FOLDER):
		print "[Error ] Sorry i dont see " + str (FOLDER)
		print "pleas create " + str (FOLDER) + str ( "and download GeoLite2-ASN.mmdb in that folder...")
		print "Hint get the file from https://dev.maxmind.com/geoip/geoip2/geolite2/ \n"
		sys.exit(-1)

	if not os.path.isfile(CITY_DB):
		print "[Error ] Sorry i do not see " + str (CITY_DB)
		print "Hint get the file from https://dev.maxmind.com/geoip/geoip2/geolite2/ \n"		
		sys.exit(-1)

	if not os.path.isfile(AS_DB):
		print "[Error ] Sorry i do not see " + str (CITY_DB)
		print "Hint get the file from https://dev.maxmind.com/geoip/geoip2/geolite2/ \n"		
		sys.exit(-1)


	city_open = geoip2.database.Reader(CITY_DB)
	asn_open = geoip2.database.Reader(AS_DB)


	if (len(sys.argv) == 1):
		print "plead provide input file... contain IP adress"

	if (len(sys.argv) != 1):
		
		if not os.path.isfile(sys.argv[1]):
			print "[Error] Sorry not implementet 100% yet..." 
			sys.exit(-1)
			if check_valid_ip(sys.argv[1]):

				country = get_CC_country_code(sys.argv[1])
				AS = get_asn_name(sys.argv[1])
				AS_NUM = get_asn_num(sys.argv[1])
				IP = '{:18s}'.format(sys.argv[1])
				print "ASN      | IP               | BGP Prefix          | CC | Registry | Allocated  | AS Name"
				print str(AS_NUM)   + str("\t| ") + str(sys.argv[1])
		else:
			if not os.path.isfile(sys.argv[1]):
				print "sorry retry I dont see you " + str (sys.argv[1])
				sys.exit(-1)
			load_url(sys.argv[1])
	city_open.close()
	asn_open.close()

#	print "END ..."
