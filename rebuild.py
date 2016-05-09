#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import csv, os, re, urllib3, requests, time, random, string, sys, sqlite3
from bs4 import BeautifulSoup

conn = sqlite3.connect('example.db')
c = conn.cursor()

c.execute('''DROP TABLE defendant''')
c.execute('''DROP TABLE court_case''')
c.execute('''DROP TABLE charges''')
c.execute('''DROP TABLE sentence''')
c.execute('''DROP TABLE bonds''')
c.execute('''DROP TABLE roa''')


c.execute('''CREATE TABLE defendant (defendant_id integer primary key, Name text, Language text, Mailing_Address text, Race text, Sex text, Height text, DOB text, Weight text, Hair text, Eyes text)''')
c.execute('''CREATE TABLE court_case (Case_Number text, Attorney text, Firm text, Attorney_Phone text, Judge text, defendant_id integer, foreign key (defendant_id) REFERENCES defendant(defendant_id))''')
c.execute('''CREATE TABLE charges (charges_id integer primary key, 
	Case_Number text,
	Offense_Date text,
	Date_Closed text,
	Offense text,
	Disposition text,
	Disposition_Date text, foreign key (Case_Number) REFERENCES court_case(Case_Number))''')
c.execute('''CREATE TABLE sentence (sentence_id integer primary key, Case_Number text, Fines text, Jail_Days text, Probation text, Balance_Due text, foreign key (Case_Number) REFERENCES court_case(Case_Number))''')
c.execute('''CREATE TABLE bonds (bonds_id integer primary key, Case_Number text, Date_Issued text, Type text, Amount text, Posted_Date text, foreign key (Case_Number) REFERENCES court_case(Case_Number))''')
c.execute('''CREATE TABLE roa (roa_id integer primary key, Date_Issued text, Action text, Judge text, Case_Number text, foreign key (Case_Number) REFERENCES court_case(Case_Number))''')

conn.commit()

#os.system("cd /d D:/grcourt-master/DataMob/")
print("We are in the right spot")
#os.system("del criminal_out.csv")

#Our source
gr_url = 'http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1'
nmax = 891429

#Get Cookie
r = requests.get('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=1')
cookies = r.cookies

#Initialize opener add cookie
# opener = urllib3.build_opener()
# opener.addheaders.append(('Cookie', headers))

#Initialize 
# criminal_out = open("criminal_out.csv", 'ab')
# with criminal_out as csvfile:
	# writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
	# writer.writerow(["Defendant", "Case Number", "Language", "Mailing Address", "Race", "Sex", "Height", "DOB", "Weight", "Hair", "Eyes", "Attorney", "Firm", "Attorney Phone", "Judge", "OffenseDate", "DateClosed", "OffenseDescription", "Disposition", "DispositionDate", "Fines", "Jail Days", "Probation", "Balance Due", "Bench Warrant Issued", "DateIssued", "Type", "Amount", "PostedDate"])

count = 1

def stable_table(regex_return, sec_list):		
	for item in regex_return:
		item = item.replace('\xa0', '')
		item = item.replace('\xc2', '')
		table_soup = BeautifulSoup(item)
		for x in table_soup.find_all(class_="medium"):
			for td_tag in x.find_all("td"):
				sec_list.append(str(td_tag.get_text(strip=True)))
		return sec_list

def stable_table_address(regex_return, sec_list):		
	for item in regex_return:
		item = item.replace('<br/>', ' ')
		table_soup = BeautifulSoup(item)
		for x in table_soup.find_all(class_="medium"):
			for td_tag in x.find_all("td"):
				sec_list.append(str(td_tag.get_text(strip=True)))
		return sec_list			
				
def handle_mult(section_inf, next_list, fields):
	numb = int(len(section_inf)/fields)
	s_index = 0
	e_index = fields
	next_list = []
	for case in range(numb):
		next_list.append(tuple(section_inf[s_index:e_index]))
		s_index += fields
		e_index += fields
	return next_list				
		
while count < 100000:
	print('On Case #:', count)
	#criminal_out = open("criminal_out.csv", 'ab')
	#Request Page
	r = requests.get('http://grcourt.org/CourtPayments/loadCase.do?caseSequence=' + str(count), cookies=cookies)
	bsoup = BeautifulSoup(r.text)
	#global problems
	#problems = []
	#Storing the first b tag inside body to data_ccsort 
	data_ccsort = bsoup.body.b
	
	#If statement that sorts out civil cases 
	if data_ccsort.string == u'Civil Case View':
		print("Civil Case Continue..." )
		count +=1
		print("ZZZZZZZ...")
		time.sleep(2.5)
	elif data_ccsort.string == 'Unable to load case data':
		print("Unable to load case data")
		count +=1
		print("ZZZZZZZ...")
		time.sleep(2.5)
	else:
		print("Criminal Case")
	
	#Run Parser Function here
		#Possible Solution for clearing &nbsp
		#soup = soup.prettify(formatter=lambda s: s.replace(u'\xa0', ' '))
		#soup = soup.prettify(formatter=lambda s: s.replace(u'\xc2', ''))
	
		data_medium = bsoup.find_all(class_="medium")
		data_XLheader = bsoup.find_all(class_="extralarge")
		data_ccsort = bsoup.body.b
		print(data_ccsort.string)
		
		print("+++++++++DEFENDANT+++++++++++++++"		)
		def_list = []
		regex_defendant = re.compile(r'.*<!-- DEFENDANT -->(.*)<!-- CHARGES -->.*', re.DOTALL)
		sec_defendant = regex_defendant.findall(str(bsoup))
		section_defendant = stable_table_address(sec_defendant, def_list)
		str_def = str(section_defendant[3]).replace('\n', ' ')
		section_defendant[3] = ' '.join(str_def.split())
		sdef_t = (None, section_defendant[0], section_defendant[2], section_defendant[3], section_defendant[4], section_defendant[5], section_defendant[6], section_defendant[7], section_defendant[8], section_defendant[9], section_defendant[10])
		sdef_t2 = (None, section_defendant[1], section_defendant[11], section_defendant[12], section_defendant[13], section_defendant[14])
		print(section_defendant, '\n')
		section_defendant
		
		print("TUPLE ---- **********CHARGES******************** ---- TUPLE")
		charge_list = []
		regex_charges = re.compile(r'.*<!-- CHARGES -->(.*)<!-- SENTENCE -->.*', re.DOTALL)
		sec_charges = regex_charges.findall(str(bsoup))
		section_charges = stable_table(sec_charges, charge_list)
		section_charges = handle_mult(section_charges, [], 5)
		print(section_charges, '\n')
		
			
		
		print("+++++++++++++++++SENTENCE+++++++++++++++")
		sen_list = []
		regex_sentence = re.compile(r'.*<!-- SENTENCE -->(.*)<!-- BONDS -->.*', re.DOTALL)
		sec_sentence = regex_sentence.findall(str(bsoup))
		section_sentence = stable_table(sec_sentence, sen_list)
		count_fields = 0
		for x in section_sentence:
			x = str(x).replace('\n', ' ')
			x = ' '.join(x.split())
			section_sentence[count_fields] = x
			count_fields += 1
		print(section_sentence, '\n'	)
		
		print("TUPLE ---- +++++++++++++BONDS+++++++++++++++++++++ ---- TUPLE")
		bonds_list = []
		regex_bonds = re.compile(r'.*<!-- BONDS -->(.*)<!-- Register of Actions -->.*', re.DOTALL)
		sec_bonds = regex_bonds.findall(str(bsoup))
		section_bonds = stable_table(sec_bonds, bonds_list)
		count_fields = 0
		for x in section_bonds:
			x = str(x).replace('\n', ' ')
			x = ' '.join(x.split())
			section_bonds[count_fields] = x
			count_fields += 1
		section_bonds = handle_mult(section_bonds, [], 4)
		print(handle_mult(section_bonds, [], 4), '\n')
		
		#print "TUPLE ---- ++++++++++++++++ROA+++++++++++++++++++++ ---- TUPLE"
		roa_list = []
		regex_roa = re.compile(r'.*<!-- Register of Actions -->(.*)<!-- Case History -->.*', re.DOTALL)
		sec_roa = regex_roa.findall(str(bsoup))
		section_roa = stable_table(sec_roa, roa_list)
		section_roa = handle_mult(section_roa, [], 3)
		#print handle_mult(section_roa, [], 3), '\n'

		print("TUPLE ---- +++++++++++++Case History+++++++++++++++++++++ ---- TUPLE")
		case_list = []
		regex_casehist = re.compile(r'.*<!-- Case History -->(.*)<!-- END Main -->.*', re.DOTALL)
		sec_casehist = regex_casehist.findall(str(bsoup))
		section_casehist = stable_table(sec_casehist, case_list)
		section_casehist = handle_mult(section_casehist, [], 4)
		print(section_casehist, '\n')
		
		# with criminal_out as csvfile:
			# writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
			# try: 
		
		# run select defendant_id from defendant based on Defendant name, addr, dob
		# store id in a variable
		# if id var not > 0
		# insert into
		# get the id from insert and store in id variable
		
		c.execute('INSERT INTO defendant VALUES (?,?,?,?,?,?,?,?,?,?,?)', sdef_t)
		c.execute('INSERT INTO court_case VALUES (?,?,?,?,?,?)', sdef_t2)
		for tpl in section_charges: 
			scha_t = (None, section_defendant[1], tpl[0], tpl[1], tpl[2], tpl[3], tpl[4]) 
			#print(scha_t)
			c.execute('INSERT INTO charges VALUES (?,?,?,?,?,?,?)', (scha_t))
		ssen_t = (None, section_defendant[1], section_sentence[0], section_sentence[1], section_sentence[2], section_sentence[3])
		c.execute('INSERT INTO sentence VALUES (?,?,?,?,?,?)', (ssen_t))
		for tpl in section_bonds:
			sbon_t = (None, section_defendant[1], tpl[0], tpl[1], tpl[2], tpl[3])
			c.execute('INSERT INTO bonds VALUES (?,?,?,?,?,?)', sbon_t)
		for tpl in section_roa:
			sroa_t = (None, section_defendant[1], tpl[0], tpl[1], tpl[2])
			print(sroa_t)
			c.execute('INSERT INTO roa VALUES (?,?,?,?,?)', sroa_t)
		conn.commit()
		count += 1
		
		print(count)
		time.sleep(2.5)
#print(problems, "Problem child?")
criminal_out.close()
