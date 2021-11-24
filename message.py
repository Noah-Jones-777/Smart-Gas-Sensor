#Program to send text message alerts based on chemical levels from smoke detector
import os
from twilio.rest import Client	#to install 'pip install twilio'

"""To use this class you you simply create a message object.
   In the parameters you must supply the recipients number as well as the body of your message.
   You must have the number without any dashes
   Exameple:
   my_message = Message("Phone number", "Here is where I put what i want to send in the message")
   Next you must use the send function to acutally send your message
   Example:
   my_message.send()
"""

class Message():
	account_sid= "AC7acf1f747da81765297f74ae46a6b41e"
	auth_token="b3815e91b5dd8be62a3f3dd8421adefa"
	sender = "+13344328177"
	def __init__(self, number_to_go_to, the_message):
		self.receiver = str(number_to_go_to)
		self.body = str(the_message)
		client = Client(self.account_sid, self.auth_token)
		#creating the message
		self.message = client.messages.create(
			body=self.body,
			from_=self.sender,
			to=self.receiver)

	#this function sends the message
	def send(self):
		print(self.message.sid)




