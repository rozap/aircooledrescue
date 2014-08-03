from django.core.management.base import BaseCommand, CommandError
import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
import re
import json
from core.models import Person, Service
from django.db import transaction

class Command(BaseCommand):

   
    def handle(self, *args, **options):
        services = Service.objects.all()
        for s in services:
            s.name = self.first_letter_caps(s.name)
            s.save()

        peeps = Person.objects.all()
        for p in peeps:
            p.name = self.first_letter_caps(p.name)
            p.save()



    def first_letter_caps(self, word):
        word = word.strip()
        def repl(m):
            return m.group(0).upper()                                                                                     
        return re.sub('^[a-z]|\s[a-z]', repl, word.lower())