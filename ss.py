import csv
import smtplib
import requests
import random
import email
import emoji
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from clockwork import clockwork

class Participant():
	recipient = ''
	email_text = ''
	sms_text = ''
	def __init__(self, num, name, email, phone, preferred_shipping_addy, exemplifies, proud, emoji, movie_role, arrested, talk_to_yourself, pizza, socks, skips, other):
		self.num = num
		self.name = name
		self.email = email
		self.phone = phone
		self.preferred_shipping_addy = preferred_shipping_addy
		self.song_exemplifies = exemplifies
		self.proud_of_this_year = proud
		self.emoji = emoji
		self.movie_role = movie_role
		self.arrested = arrested
		self.talk_to_yourself = talk_to_yourself
		self.pizza = pizza
		self.socks = socks
		self.skips = skips
		self.other = other
		
def get_participants():
	participants = []
	f = open('ss.csv', 'rt')
	try:
		opened_file = csv.reader(f)
		for row in opened_file:
			if row[0] == 'Timestamp':
				continue
			num = str(row[1].encode("utf-8").decode("ascii","ignore"))
			name = str(row[2].encode("utf-8").decode("ascii","ignore"))
			email = str(row[3].encode("utf-8").decode("ascii","ignore"))
			phone = str(row[4].encode("utf-8").decode("ascii","ignore"))
			addy = str(row[5].encode("utf-8").decode("ascii","ignore"))
			
			song = str(row[6].encode("utf-8").decode("ascii","ignore"))
			proud = str(row[7].encode("utf-8").decode("ascii","ignore"))
			emoji_text = str(row[8])
			movie = str(row[9].encode("utf-8").decode("ascii","ignore"))
			arrested = str(row[10].encode("utf-8").decode("ascii","ignore"))
			talk = str(row[11].encode("utf-8").decode("ascii","ignore"))
			pizza = str(row[12].encode("utf-8").decode("ascii","ignore"))
			socks = str(row[13].encode("utf-8").decode("ascii","ignore"))
			skips = str(row[14].encode("utf-8").decode("ascii","ignore"))
			other = str(row[17].encode("utf-8").decode("ascii","ignore"))

			emoji_text = emoji.demojize(emoji.emojize(emoji_text))
			participants.append(Participant(num, name, email, phone, addy, song, proud, emoji_text, movie, arrested, talk, pizza, socks, skips, other))
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
		if person.recipient.num in person.skips:
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
	print("song_exemplifies: " + str(participant.song_exemplifies))
	print("proud_of_this_year: " + str(participant.proud_of_this_year))
	print("emoji: " + str(participant.emoji))
	print("movie_role: " + str(participant.movie_role))
	print("arrested: " + str(participant.arrested))
	print("talk_to_yourself: " + str(participant.talk_to_yourself))
	print("pizza: " + str(participant.pizza))
	print("socks: " + str(participant.socks))
	print("skips: " + str(participant.skips))
	print("other: " + str(participant.other))

def generate_email(participants):
	text = ''
	for person in participants:
		recipient = person.recipient

		text = '\nDear ' + str(person.name.split()[0]) + ',\n<br>	Welcome to the 2018 GBL Secret Santa!! Below you will find the details of your recipient ...' + "<b>" + str(recipient.name.upper()) + '</b>!\n \n<br>'
		text += "<br>Name: " + "<b>" + recipient.name + "</b><br>\n"
		text += "<br>Shipping Address: " + "<b>" + recipient.preferred_shipping_addy.replace("\n", " ") + "</b><br>\n"
		text += "<br>What song exemplifies 2018 for you?: " + "<b>" + recipient.song_exemplifies + "</b><br>\n"
		text += "<br>What is something you're proud of this year?: " + "<b>" + recipient.proud_of_this_year + "</b><br>\n"
		text += "<br>What is your most-used emoji?: " + "<b>" + recipient.emoji + "</b><br>\n"
		text += "<br>If someone were to play you in a movie, who would you want it to be and why?: " + "<b>" + recipient.movie_role + "</b><br>\n"
		text += "<br>If you were to be arrested with no explanation, what would your friends and family assume you had done?: " + "<b>" + recipient.arrested + "</b><br>\n"
		text += "<br>Do you ever talk to yourself when you're alone? What's the weirdest thing you've said to yourself?: " + "<b>" + recipient.talk_to_yourself + "</b><br>\n"
		text += "<br>Why do we get circular pizza in a square box when we eat pizza in triangular slices?: " + "<b>" + recipient.pizza + "</b><br>\n"	
		text += "<br>I enjoy the following types of socks and sock patterns...: " + "<b>" + recipient.socks + "</b><br>\n"
		text += "<br>What else you got on your mind? Best comment here wins a prize: " + "<b>" + recipient.other + "</b><br>\n"
		person.email_text = text

def generate_text(participants):
	text = ''
	for person in participants:
		text = 'Hey ' + str(person.name.split()[0]) + ',\n2018 GBL Secret Santa details have been sent out!! Please check your email! \n-Sir Santa'	  
		person.sms_text = text

def send_email(name, email, subject, text, username, password, server='smtp.gmail.com:587'):

	fromaddr = username
	toaddr = email
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject
	text = emoji.emojize(text)
	msg.attach(MIMEText(text.encode('utf-8'), _subtype='html', _charset="UTF-8"))

	try:
		server = smtplib.SMTP(server)
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
	data['subject'] = 'GBL Secret Santa'
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

	generate_email(participants)
	generate_text(participants)
	# print("Enter username/email")
	# username = str(input())
	# import getpass
	# password = getpass.getpass('Password:')

	# for person in participants:
		# send_email(person.name, person.email, "GBL Secret Santa 2018! - Post Grad Edition", person.email_text, username, password)
	try:
		for person in participants:
			send_text(person.sms_text, person.phone)
	except Exception as e:
		print(e)
a = run()