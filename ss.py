import csv
import smtplib
import requests
import random
 
images = ['https://i.pinimg.com/originals/0e/f8/92/0ef892a916f750ba341f9c3ef6217bc3.gif','https://media.tenor.com/images/925e118b716ebb85cf2a8fdcb464df93/tenor.gif','http://gifimage.net/wp-content/uploads/2017/07/funny-christmas-gif-11.gif','https://i.pinimg.com/originals/f7/1b/53/f71b53a9c2b697ce26fcd9b7fc40e423.gif', 'https://media1.tenor.com/images/5f4cb062d34e5c4616b134c43ba7b55d/tenor.gif']


class Participant():
	recipient = ''
	email_text = ''
	sms_text = ''
	def __init__(self, name, enjoy, fav_holiday_snack, other, email, phone=None, holiday=None, preferred_shipping_addy=None):
		self.name = name
		self.enjoy = enjoy
		self.fav_holiday_snack = fav_holiday_snack
		self.holiday = holiday
		self.other = other
		self.phone = phone
		self.email = email
		self.preferred_shipping_addy = preferred_shipping_addy
		

def get_participants():
	participants = []
	f = open('ss.csv', 'rt')
	try:
		opened_file = csv.reader(f)
		for row in opened_file:
			if row[0] == 'Timestamp':
				continue
			name = str(row[1].encode("utf-8").decode("ascii","ignore"))
			enjoy = str(row[4].encode("utf-8").decode("ascii","ignore"))
			fav_holiday_snack = str(row[5].encode("utf-8").decode("ascii","ignore"))
			other = str(row[7].encode("utf-8").decode("ascii","ignore"))
			email = str(row[2].encode("utf-8").decode("ascii","ignore"))
			phone = str(row[3].encode("utf-8").decode("ascii","ignore"))
			holiday = str(row[6].encode("utf-8").decode("ascii","ignore"))
			preferred_shipping_addy = str(row[9].encode("utf-8").decode("ascii","ignore"))
			participants.append(Participant(name, enjoy, fav_holiday_snack, other, email, phone, holiday, preferred_shipping_addy))
			# print(name + " " + enjoy + " " + fav_holiday_snack + " " + holiday + " " + other)
	finally:
		f.close()
	return participants

def match_participants(participants):
	copy = []
	count = 0
	while (count < len(participants)):
		copy.append(count)
		count+=1
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

def print_participant(participant):
	print("Name: " + participant.name)
	print("Email: " + participant.email)
	print("Phone: " + participant.phone)
	print("Recipient: " + participant.recipient.name)
	print("Enjoy: " + participant.recipient.enjoy) 
	print("Fav Holiday Snack: " + participant.recipient.fav_holiday_snack)
	print("Other: " + participant.recipient.other)
	print("Preffered Shipping Address: " + participant.recipient.preferred_shipping_addy)


def generate_email(participants):
	text = ''
	for person in participants:
		text = 'Dear ' + str(person.name.split()[0]) + ',\n	Welcome to the 2017 GBL Secret Santa - Post Grad Edition!! Below you will find the details of your recipient...drumroll...' + str(person.recipient.name.upper()) + '!\n \n' + 'Name: ' + str(person.recipient.name) + '\n' + str(person.recipient.name) + ' enjoys: ' + str(person.recipient.enjoy) + '\n' + str(person.recipient.name) + '\'s Favorite Holiday Snack(s): ' + str(person.recipient.fav_holiday_snack) + '\n' + str(person.recipient.name) + 'Other: ' + str(person.recipient.other) + "\n\n" + 'Preffered Shipping Addres: ' + str(person.recipient.preferred_shipping_addy) + "\n\n\n" + random.choice(images) 
		person.email_text = text

def generate_text(participants):
	text = ''
	for person in participants:
		text = 'Hey ' + str(person.name.split()[0]) + ',\n 2017 GBL Secret Santa details have been sent out!! Please check your bmail! \n-Santa'	  
		person.sms_text = text

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
		print("Sending email to " + toaddrs, )
		server.sendmail(fromaddr, toaddrs, msg)
		server.quit()
		print("...Email sent!")
	except Exception as e:
		print('Error while logging into email!')
		print(e)


def send_text(txt, number):
	number = str(number).replace("(","")
	number = str(number).replace(")","")
	number = str(number).replace("-","")
	number = str(number).replace(" ","")
	data = {}
	data['message'] = txt
	data['subject'] = 'GBL Secret Santa'
	data['number'] = str(number)
	print("Sending text...")
	print(requests.post("http://textbelt.com/text#sthash.p87DHwdU.dpuf", data=data))

def run(test=True):
	participants = get_participants()
	match_participants(participants)

	generate_email(participants)
	generate_text(participants)
	print("Enter username/email")
	username = str(input())
	import getpass
	password = getpass.getpass('Password:')
	# return participants
	# print_matches(participants)
	for person in participants:
		send_email(person.name, person.email, "GBL Secret Santa 2017! - Post Grad Edition", person.email_text, username, password)
	try:
		for person in participants:
			send_text(person.sms_text, person.phone)
	except Exception as e:
		print(e)

a = run()