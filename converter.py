#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import quopri
import sys
import os.path

filepath = ''
for arg in sys.argv:
	filepath = arg

if len(sys.argv)==1 or filepath=='':
	print "Please define the import file path"
	sys.exit()
elif not os.path.exists(filepath):
	print "Can't find the file to import"
	sys.exit()

file_name = filepath.split(".")

with open(filepath, "r") as myfile:
	data=myfile.read()

regex = re.compile('BEGIN:VCARD(.*?)END:VCARD', re.IGNORECASE|re.DOTALL)

f = open(file_name[0] + '.csv',"wb")
f.write('Name,E-mail 1 - Value,E-mail 2 - Value,Phone 1 - Value,Phone 1 - detail,Phone 2 - Value,Phone 2 - detail,,FacebookID,Facebook Status,Facebook-link,Favorite,poBox,extended address,street address,locality,region,postal code,country name\n')

converted_contact = {}
for match in re.finditer(regex, data):
	converted_contact["FN"] = ''
	converted_contact["EMAIL0"] = ''
	converted_contact["EMAIL1"] = ''
	converted_contact["PHONE0"] = ''
	converted_contact["PHONE1"] = ''
	contact = match.group(0)
	for everyInfo in contact.split("\n"):
		info = everyInfo.split(':')
		if info[0] == 'FN':
			#print "info1:" + info[1];
			if info[1].find('CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:') > 0:
				info[1] = info[1].replace('\r', '')
				info[1] = quopri.decodestring(info[1].replace('CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:', ''))
				converted_contact["FN"] = info[1].decode('utf-8')
			else:
				converted_contact["FN"] = info[1].replace('\r', '')
		elif info[0] == 'EMAIL' or info[0] == 'EMAIL;PREF':
			if converted_contact["EMAIL0"] == '':
				converted_contact["EMAIL0"] = info[1].replace('\r', '')
			elif converted_contact["EMAIL1"] == '':
				converted_contact["EMAIL1"] = info[1].replace('\r', '')
		elif info[0] == 'TEL' or info[0] == 'TEL;CELL':
			if converted_contact["PHONE0"] == '':
				converted_contact["PHONE0"] = info[1].replace('-', '').replace('\r', '')
			elif converted_contact["PHONE1"] == '':
				converted_contact["PHONE1"] = info[1].replace('-', '').replace('\r', '')
	if converted_contact["FN"] != '' and (converted_contact["EMAIL0"] != '' or converted_contact["PHONE0"] != ''):
		f.write(converted_contact["FN"] + ',' + converted_contact["EMAIL0"] + ',' + converted_contact["EMAIL1"] + ','  + converted_contact["PHONE0"] + ',,' + converted_contact["PHONE1"] + ',,,,,,,,,,,,,\n')

f.close()