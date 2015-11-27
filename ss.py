import csv
import getpass
import smtplib
from twilio.rest import TwilioRestClient
import random
from underscore import _

# put your own credentials here
ACCOUNT_SID = "AC03b180bc661ab09945326c83cc118a0a"
AUTH_TOKEN = "861d6af22b6012fbf1a9e658c2c47428"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)


class Participant():
	recipient = ''
	email_text = ''
	sms_text = ''
	def __init__(self, name, enjoy, fav_holiday_snack, holiday, other, phone, email):
		self.name = name
		self.enjoy = enjoy
		self.fav_holiday_snack = fav_holiday_snack
		self.holiday = holiday
		self.other = other
		self.phone = phone
		self.email = email


def get_participants():
	participants = []
	f = open('ss.csv', 'rt')
	try:
		opened_file = csv.reader(f)
		for row in opened_file:
			if row[0] == 'Timestamp':
				continue
			name = str(row[1].encode("utf-8").decode("ascii","ignore"))
			enjoy = str(row[2].encode("utf-8").decode("ascii","ignore"))
			fav_holiday_snack = str(row[3].encode("utf-8").decode("ascii","ignore"))
			holiday = str(row[4].encode("utf-8").decode("ascii","ignore"))
			other = str(row[5].encode("utf-8").decode("ascii","ignore"))
			email = str(row[6].encode("utf-8").decode("ascii","ignore"))
			phone = str(row[7].encode("utf-8").decode("ascii","ignore"))
			participants.append(Participant(name, enjoy, fav_holiday_snack, holiday, other, phone, email))
			#print(name + " " + enjoy + " " + fav_holiday_snack + " " + holiday + " " + other)

	finally:
		f.close()

	return participants

def match_participants(participants):
	copy = []
	count = 0
	while (count < len(participants)):
		copy.append(count)
		count += 1
	random.shuffle(copy)

	count = 0
	while count < len(copy) - 1:
		if count == copy[count]:
			copy[count] = copy[count+1]
			copy[count+1] = count
		count+=1

	count = 0
	while (count < len(participants)):
		participants[count].recipient = participants[copy[count]]
		count+=1
	if not valid_match(participants):
		match_participants(participants)


def valid_match(participants):
	for person in participants:
		if person.recipient.name == person.name:
			return False
	return True

def check(participants, count=100):
	while(count >= 0):
		match_participants(participants)
		if not valid_match(participants):
			print_matches(participants)
			return False
		count -= 1
	return True

def print_matches(participants):
	for item in participants:
		print(item.name + ' --> ' + item.recipient.name)

def generate_email(participants):
	email_template = _.template('Dear <%= name %>,\n\r Welcome to this year\'s Secret Santa!! Below you will find the details of your chosen recipient. \n \n' + 'Name: <%= name %>\n\nThey enjoy <%= enjoy %>, their favorite holiday snack is <%= fav_holiday_snack %> and their preferred holiday if <%= holiday %>. \nTheir random other is <%= other %>')

	for person in participants:
		person.email_text = email_template(vars(person))

def generate_text(participants):
	sms_template = _.template('Hey <%= name %>,\n 2015 GBL Secret Santa details have been sent out. Please check your email! \n -Santa')
	for person in participants:
		person.sms_text = sms_template(vars(person))

def send_email(name, email, subject, text, username, password, server='smtp.gmail.com:587'):
	fromaddr = username
	toaddrs  = email
	msg = "\r\n".join([
	  "From: "+fromaddr,
	  "To: "+toaddrs,
	  "Subject: "+subject,
	  "",
	  text
	  ])

	try:
		server = smtplib.SMTP(server)
		server.ehlo()
		server.starttls()
		server.login(username,password)
		print("Sending email to " + toaddrs)
		server.sendmail(fromaddr, toaddrs, msg)
		server.quit()
		print("Email sent!")
	except Exception as e:
		print('Error while logging into email!')
		print(e)


def send_text(name, number, text):
	client.messages.create(
		to="+1"+number,
		from_="+15622731468",
		body=text,
	)

	print('Sent text message to ' + name)

def run(test=True):
	participants = get_participants()
	match_participants(participants)
	generate_email(participants)
	generate_text(participants)

	print("Enter username/email")
	username = str(input())
	password = getpass.getpass('Password:')

	# Run Loop
	for person in participants:
		if test:
			send_email(person.name, username, "GBL Secret Santa 2015!", person.email_text, username, password)
			send_text(person.name, '5626863998', person.sms_text)
		else:
			send_email(person.name, person.email, "GBL Secret Santa 2015!", person.email_text, username, password)
			send_text(person.name, person.number, person.sms_text)

run()
