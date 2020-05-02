#!/usr/bin/python3

import csv
import sqlite3
import argparse
import random


def generate_password(length):
    """Generate a password of a desired length with numbers, symbols, upper
    and lowercase letters"""
    if length < 4:
        raise ValueError('length must be 4 or greater')

    lower_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                   'm', 'n', 'o', 'p',
                   'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    upper_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                   'M', 'N', 'O',
                   'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '_']
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    count = 0
    password = ""
    choices = ['lower', 'upper', 'symbols', 'digits']
    while count < length:
        if len(choices) == 0:
            choices = ['lower', 'upper', 'symbols', 'digits']

        current_char = random.choice(choices)

        if current_char == 'lower':
            password += random.choice(lower_chars)
            choices.remove('lower')
        elif current_char == 'upper':
            password += random.choice(upper_chars)
            choices.remove('upper')
        elif current_char == 'symbols':
            password += random.choice(symbols)
            choices.remove('symbols')
        elif current_char == 'digits':
            password += random.choice(digits)
            choices.remove('digits')
        count += 1

    return password


def generate_username(email):
    """Generate a username based on an email"""
    username = email.split('@')[0]

    return username


parser = argparse.ArgumentParser(
    description='''Given a CSV with usernames,
    email, first and last names, create two CSVs for bulk importing into
    courses in Moodle''')
parser.add_argument('users',
                    help='CSV containing user information')
parser.add_argument('course_name_prefix',
                    help='Prefix attached to generated course names')
parser.add_argument('category',
                    help='The moodle category these courses are created in')
parser.add_argument('--generate-passwords', action='store_true',
                    dest='passwords',
                    help='''Generate usernames and passwords in CSV
                    if you are also generating user accounts at the
                    same time''')

users = parser.parse_args()

# Create a temporary table in memory to store the CSV inputs
db = sqlite3.connect(":memory:")
cursor = db.cursor()
cursor.execute(
    '''CREATE TABLE users (username text, password text, email text,
    firstname text, lastname text)''')
db.commit()

# Insert the values from the input csv into the temporary database
with open(users.users) as csvfile:
    r = csv.reader(csvfile)
    rl = next(r)
    username_pos = rl.index('username')
    email_pos = rl.index('email')
    firstname_pos = rl.index('firstname')
    lastname_pos = rl.index('lastname')
    for row in r:
        if users.passwords:
            user_info = [generate_username(row[email_pos]),
                         generate_password(12), row[email_pos],
                         row[firstname_pos],
                         row[lastname_pos]]
        else:
            user_info = [row[username_pos], "",
                         row[email_pos],
                         row[firstname_pos],
                         row[lastname_pos]]
        cursor.execute('''INSERT INTO users VALUES(?,?,?,?,?)''', user_info)
    db.commit()


# Generate the courses.csv for import into Moodle
with open('courses.csv', 'w', newline='\n') as courses_csv:
    fields = ['fullname', 'shortname', 'category']
    writer = csv.DictWriter(courses_csv, fieldnames=fields)
    writer.writeheader()

    for row in cursor.execute('''SELECT firstname,lastname FROM users'''):

        course_name = users.course_name_prefix + "-" + row[0] + row[1]
        course_name = course_name.replace(" ", "")
        writer.writerow(
            {'fullname': course_name, 'shortname': course_name,
             'category': users.category})


# Generate the users.csv for import into Moodle
with open('enroll.csv', 'w', newline='\n') as enroll_csv:
    if users.passwords:
        fields = ['username', 'email', 'password', 'firstname',
                  'lastname', 'course1', 'role1']
    else:
        fields = ['username', 'course1', 'role1']
    writer = csv.DictWriter(enroll_csv, fieldnames=fields)
    writer.writeheader()
    for row in cursor.execute('''SELECT username,firstname,
                              lastname,email,password FROM users'''):
        course_name = users.course_name_prefix + "-" + row[1] + row[2]
        course_name = course_name.replace(" ", "")
        if users.passwords:
            writer.writerow(
                {'username': row[0], 'email': row[3], 'password': row[4],
                 'firstname':row[1],'lastname':row[2],'course1': course_name,
                 'role1': 'editingteacher'}
            )
        else:
            writer.writerow(
                {'username': row[0], 'course1': course_name,
                 'role1': 'editingteacher'})
