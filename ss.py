import csv
import smtplib
import requests
import random
import email
import emoji
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Participant():
	recipient = ''
	email_text = ''
	sms_text = ''
	def __init__(self, name, email, phone, preferred_shipping_addy, skips):
		self.name = name
		self.email = email
		self.phone = phone
		self.preferred_shipping_addy = preferred_shipping_addy
		self.skips = skips.split(",")
		
def get_participants():
	participants = []
	f = open('ss.csv', 'rt')
	try:
		opened_file = csv.reader(f)
		for row in opened_file:
			if row[0] == 'Timestamp':
				continue
			name = str(row[1].encode("utf-8").decode("ascii","ignore"))
			email = str(row[2].encode("utf-8").decode("ascii","ignore"))
			phone = str(row[3].encode("utf-8").decode("ascii","ignore"))
			addy = str(row[4].encode("utf-8").decode("ascii","ignore"))
			skips = str(row[5].encode("utf-8").decode("ascii","ignore"))

			participants.append(Participant(name, email, phone, addy, skips))
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
		if person.recipient.name in person.skips:
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
	print("name: " + str(participant.name))
	print("email: " + str(participant.email))
	print("phone: " + str(participant.phone))
	print("preferred_shipping_addy: " + str(participant.preferred_shipping_addy))
	print("skips: " + str(participant.skips))

def generate_email(participants):
	text = ''
	for person in participants:
		recipient = person.recipient

		text = '\nDear ' + str(person.name.split()[0]) + ',\n<br>	Welcome to the 2020 GBL Secret Santa!! Below you will find the details of your recipient...' + "<b>" + str(recipient.name.upper()) + '</b>!\n \n<br>'
		text += "<br>Name: " + "<b>" + recipient.name + "</b><br>\n"
		text += "<br>Shipping Address: " + "<b>" + recipient.preferred_shipping_addy.replace("\n", " ") + "</b><br>\n</b><br>\n"

		text += "<br>Happy Holidays!" + "</b><br></b><br>\n"
		text += "<img src='https://media0.giphy.com/media/RJKHjCAdsAfQPn03qQ/200.gif'></img>"
		text += "<br>Please do NOT respond to this email. It will reveal to me your recipient.</b>\n"
		person.email_text = text

def generate_text(participants):
	text = ''
	for person in participants:
		text = 'Hey ' + str(person.name.split()[0]) + ',\n2019 GBL Secret Santa details have been sent out!! Please check your email! \n-Sir Santa'	  
		person.sms_text = text

def send_email(name, email, subject, text, username, password):

	fromaddr = username
	toaddr = email
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject
	text = emoji.emojize(text)
	msg.attach(MIMEText(text.encode('utf-8'), _subtype='html', _charset="UTF-8"))

	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(username,password)
		print("Sending email to " + toaddr, )
		server.sendmail(fromaddr, toaddr, msg.as_string())
		server.quit()
		print("...Email sent!")
	except Exception as e:
		print("Error sending email to " + name + " : " + str(email))
		print(text)
		print(e)

def send_text(txt, number):
	number = str(number).replace("(","")
	number = str(number).replace(")","")
	number = str(number).replace("-","")
	number = str(number).replace(" ","")
	data = {}
	data['message'] = txt
	data['subject'] = '2019 GBL Secret Santa'
	data['number'] = str(number)
	npa = number[:3]
	exchange = number[3:6]
	num = number[6:]
	print("Sending text...")
	url = "http://www.txtdrop.com/"

	payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"emailfrom\"\r\n\r\ndubash.kurush@gmail.com\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"npa\"\r\n\r\n"+npa+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"exchange\"\r\n\r\n"+exchange+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"number\"\r\n\r\n"+num+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"body\"\r\n\r\n" + txt + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"submit\"\r\n\r\nSend\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"submitted\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
	headers = {
		'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
		'cache-control': "no-cache",
		'Postman-Token': "da3c0437-d60c-4517-9a4d-ca1254c98cee"
		}
	try:
		response = requests.request("POST", url, data=payload, headers=headers)
	except Exception as e:
		print("Failed to send text for " + str(number))
		print(e)

def run(test=True):
	participants = get_participants()
	match_participants(participants)
	# print_matches(participants)

	generate_email(participants)
	generate_text(participants)

	username = "dubash.kurush@gmail.com"
	pass = "" #gmail app pass
	for person in participants:
		send_email(person.name, person.email, "GBL Secret Santa 2019!", person.email_text, username, )
a = run()
