from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class NiceObject( models.Model ):

    class Meta:
        abstract = True






# Create your models here.
class Person( NiceObject ):
    user = models.ForeignKey( User , default = None, null = True)
    name = models.CharField( max_length = 255 )
    description = models.TextField( default = '' )
    phone = models.CharField(max_length = 32, default = '')
    email = models.CharField( default = '', max_length=255)
    services = models.ManyToManyField( 'Service')
    verified = models.BooleanField(default = False)
    lat = models.DecimalField(default = 0, max_digits=14, decimal_places=10)
    lng = models.DecimalField(default = 0, max_digits=14, decimal_places=10)
    address = models.CharField(default = '', max_length = 512)
    ok_contact = models.IntegerField(default = 1)
    beer = models.CharField(default = '', max_length = 255)
    

    def shallow(self):
        d = {}
        d['id'] = self.id
        d['username'] = self.user.username if self.user else None 
        d['name'] = self.name
        d['description'] = self.description
        d['phone'] = self.phone
        d['email'] = self.user.email if self.user else self.email
        d['verified'] = self.verified
        d['lat'] = self.lat
        d['lng'] = self.lng
        d['ok_contact'] = self.ok_contact
        d['beer'] = self.beer
        return d

    def deep(self):
        d = self.shallow()
        d['services'] = list(self.services.all())
        d['karma'] = list(Karma.objects.filter(person = self))
        d['flags'] = list(Flag.objects.filter(person = self))
        return d

    #Because of the shitty half users imported from the old type2 rescue site, this is the solution :(
    def get_email(self):
        if self.verified:
            return user.email
        else:
            return email

    def get_name(self):
        if self.verified:
            return self.user.first_name + " " + self.user.last_name
        else:
            return self.name



class Service( NiceObject):
    name = models.CharField(default = '', max_length = 512)

    def shallow(self):
        return self.deep()

    def deep(self):
        d = {}
        d['name'] = self.name
        return d

class Activation( models.Model ):
    key = models.CharField(max_length = 512)
    person = models.ForeignKey('Person')


class PasswordReset( models.Model ):
    key = models.CharField(max_length = 512)
    user = models.ForeignKey(User)


class Interaction(NiceObject):

    class Meta:
        abstract = True

    def shallow(self):
        d = {}
        d['description'] = self.description
        d['person'] = self.person.id
        d['creator'] = self.creator.id
        d['creator_name'] = self.creator.name
        d['date'] = self.date.strftime('%Y-%m-%dT%H:%M:%S')
        return d

    def deep(self):
        d = self.shallow()
        return d


class Karma( Interaction ):
    description = models.TextField( default = '' )
    person = models.ForeignKey(Person, related_name = 'karma_person')
    creator = models.ForeignKey(Person, related_name = 'karma_creator')
    date = models.DateTimeField(auto_now_add = True, default = datetime.now())


class Flag( Interaction ):
    description = models.TextField( default = '' )
    person = models.ForeignKey(Person, related_name = 'flag_person')
    creator = models.ForeignKey(Person, related_name = 'flag_creator')
    date = models.DateTimeField(auto_now_add = True, default = datetime.now())

   