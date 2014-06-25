#Imports
import os
import imaplib
import smtplib
import pygame
import time
from threading import Timer

global msgList, msgReadBy, newMsg
newMsg = False
msgReadBy = 'N/A'
msgList = []

#Clear Screen
def clr():
	os.system('clear')

clr()

def notify():
	pygame.mixer.init()
	pygame.mixer.music.load("DWillNotify.mp3")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
		continue

def showMsg():
	clr()
	if not msgList:
		print('There are no messages to display.')
	else:
		print('----------------------------------------\nMessage From Dr. Williams:\n' + msgList[0] + '\n----------------------------------------')

def grabEmails():
	global msgList, newMsg
	try:
		M = imaplib.IMAP4_SSL('imap.gmail.com',993)
		M.login('email@email.com','password')
		M.select()
		typ, data = M.search(None, 'UNSEEN')
		for num in data[0].split():
			typ, data = M.fetch(num, '(UID BODY[TEXT])')
			gmailSignature = '\r\n--\r\nSent using SMS-to-email. Reply to this email to text the sender back and  \r\nsave on SMS fees.\r\nhttps://www.google.com/voice/\r\n'
			msg =  str(data[0][1])
			msg = msg.replace(gmailSignature, '')
			if msg not in msgList:
				msgList.append(msg)
				newMsg = True
		if newMsg:
			notify()
			newMsg = False
		M.close()
		M.logout()
	except e:
		pass

def markRead(readBy):
	global msgReadBy
	smtpServer=smtplib.SMTP('smtp.gmail.com:587')
	smtpServer.starttls()
	smtpServer.login("email@email.com","password")
	returnMsg = msgList[0] + '\nRead By: ' + readBy
	smtpServer.sendmail("email@email.com","emailphone",returnMsg)
	#smtpServer.sendmail("email@email.com","emailphone",returnMsg)
	smtpServer.quit()
	msgList.pop(0)
	if not msgList:
		showMsg()

def grabNew():
	grabEmails()
	Timer(5, grabNew, ()).start()

print('There are no messages to display.')

grabNew()

while True:
	if msgList:
		showMsg()
		msgReadBy = raw_input('Once you have finished reading this, please type your name\nbelow and hit ENTER indicating that you have read and communicated this message\nto everyone in your room.\nName> ')
		markRead(msgReadBy)

