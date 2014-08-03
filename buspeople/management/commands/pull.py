from django.core.management.base import BaseCommand, CommandError
import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
import re
import json
from core.models import Person, Service

class Command(BaseCommand):

    STATES = ['al', 'az', 'ak', 'ar', 'ca', 'ct', 'co', 'de',
     'fl', 'ga', 'hi', 'in', 'il', 'id', 'ia', 'ky', 'ks', 'la',
      'me', 'mn', 'ms', 'mi', 'mo', 'mt', 'ma', 'nm', 'ne', 'nd', 
      'nv', 'nh', 'nc', 'nj', 'ok', 'or', 'pa', 'ny', 'oh', 'sd', 
      'sc', 'md', 'tx', 'ri', 'tn', 'wa', 'wy', 'vt', 'ut', 'va', 
      'wy', 'wi']
    URL = 'http://www.type2.com/rescue/us/%s.html'

    def handle(self, *args, **options):
        print "Pulling"
        for s in self.STATES:
            resp = urllib2.urlopen(self.URL % s).read()
            soup = BeautifulSoup(resp)
            entries = soup.findAll('p', {'align' : 'center'})
            for e in entries:
                raw = str(e)
                content = e.text.lower()


                person = Person()

                beer = re.search('(?<=beer type:).*?(?=<)', raw, re.IGNORECASE+re.DOTALL)
                if beer:
                    person.beer = beer.group(0)

                name = re.search('[a-z ]+?(?=<)', raw, re.IGNORECASE)
                if name:
                    person.name = name.group(0)
                email = e.findAll('a')
                if email:
                    person.email = email[0]['href'].replace('mailto:', '')

                if 'emergency' in content:
                    person.ok_contact = 0

                phone = re.search('(?<=phone:)[ 0-9-]{7,14}', content)
                if phone:
                    person.phone = phone.group(0).strip()


                #Location stuff
                loc = ''
                location = re.search('(?<=crossroads:).*?(?=<)', raw, re.DOTALL+re.IGNORECASE)
                if location:
                    location = location.group(0)
                    location = location.replace('&nbsp;', '')
                    location = location.replace('&amp;', ' and ')
                    loc += location
                zipcode = re.search('[0-9]{5}', raw)
                if zipcode:
                    loc += ' ' + zipcode.group(0)
                loc = loc.strip()
                if len(loc) > 4:
                    loc += ' ' + s + ', USA'
                    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % loc
                    geocode = urllib2.urlopen(urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]")).read()
                    data = json.loads(geocode)
                    if data.get('results', False) and data['results'][0].get('geometry', False):
                        lat = data['results'][0]['geometry']['location']['lat']
                        lng = data['results'][0]['geometry']['location']['lng']
                        address = data['results'][0]['formatted_address']
                        person.lat = lat
                        person.lng = lng
                        person.address = address
                    if person.lat != 0 and person.lng != 0 and len(person.phone) > 6:
                        try:
                            Person.objects.get(lat = lat, lng = lng)
                            print "Skipping %s" % person.name
                        except Person.DoesNotExist:
                            print "Saving %s" % person.name
                            print "PHONE %s" % person.phone
                            print "EMAIL %s" % person.email
                            person.save()
                            services = re.search('(?<=services:).*?(?=camping:)', raw, re.DOTALL+re.IGNORECASE)
                            if services:
                                services = services.group(0)
                                services = services.split('<br />')
                                for s in services:
                                    service = re.search('[A-Za-z -&]+', s)
                                    if service and len(service.group(0)):
                                        name = service.group(0)
                                        try:
                                            srv = Service.objects.get(name__iexact = self.first_letter_caps(name))
                                            person.services.add(srv)
                                        except Service.DoesNotExist:
                                            ns = Service(name = self.first_letter_caps(name))
                                            ns.save()
                                            person.services.add(ns)

                            person.save()


    def first_letter_caps(self, word):
        word = word.strip()
        def repl(m):
            return m.group(0).upper()                                                                                     
        return re.sub('^[a-z]|\s[a-z]', repl, word.lower())