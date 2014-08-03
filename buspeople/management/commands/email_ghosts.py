from django.core.management.base import BaseCommand, CommandError
import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
import re
import json
from core.models import Person, Service
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string


class Command(BaseCommand):

   
    def handle(self, *args, **options):
        people = Person.objects.filter(lat = 0).filter(lng = 0)
        for p in people:
            print "Emailing %s" % p.user.username
            msg = render_to_string("email_ghosts.txt", 
                {'username' : p.user.username})
            send_mail('Trouble logging in at Aircooled Rescue?', msg, 'aircooledrescue@gmail.com',
            [p.user.email], fail_silently=False)  