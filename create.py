#!/usr/bin/python3

import csv
import sys
import sqlite3

users = sys.argv[1]

db = sqlite3.connect(":memory:")
cursor = db.cursor()
cursor.execute('''CREATE TABLE users (id text, email text, firstname text, lastname text)''')
db.commit()

with open(users) as csvfile:
	r = csv.reader(csvfile)
	for row in r:
		cursor.execute('''INSERT INTO users VALUES(?,?,?,?)''', row)
	db.commit()

with open('courses.csv','w', newline='\n') as courses_csv:
	fields = ['fullname','shortname','category']
	writer = csv.DictWriter(courses_csv, fieldnames=fields)
	writer.writeheader()
	for row in cursor.execute('''SELECT * FROM users'''):
		course_name = "OTLSandbox-" + row[2] + row[3]
		writer.writerow({'fullname':course_name,'shortname':course_name,'category':'23'})

with open('enroll.csv','w', newline='\n') as enroll_csv:
	fields = ['username','course1','role1']
	writer = csv.DictWriter(enroll_csv, fieldnames=fields)
	writer.writeheader()
	for row in cursor.execute('''SELECT * FROM users'''):
		course_name = "OTLSandbox-" + row[2] + row[3]
		writer.writerow({'username':row[0],'course1':course_name,'role1':'editingteacher'})