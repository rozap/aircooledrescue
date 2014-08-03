from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_activation(person, activate):
	msg = render_to_string("email_activation.txt", 
		{'key' : activate.key, 'username' : person.user.username})
	send_mail('Your Aircooled Rescue Activation', msg, 'aircooledrescue@gmail.com',
		[person.email], fail_silently=False)  


def send_reset(user, reset):
	msg = render_to_string("email_reset.txt", 
		{'key' : reset.key, 'username' : user.username})
	send_mail('Your Aircooled Rescue Password Reset Link', msg, 'aircooledrescue@gmail.com',
		[user.email], fail_silently=False)  
