# Create your views here.
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.db import transaction
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from buspeople.decorators import json_view, cacheable
from django.contrib.auth.decorators import login_required
from core.models import Person, Service, Karma, Flag
import json
from decimal import Decimal
from util import is_phone, is_email

@cacheable
@json_view
def people(request):
    peeps = Person.objects.all()
    return {'people' : peeps}

@json_view
def person(request, id):
    if request.method == 'GET':
        try:
            person = Person.objects.get(id = id)
        except Person.DoesNotExist:
            return HttpResponseNotFound("Bad Id")
    return {'person' : person }

@cacheable
@json_view
def services(request):
    return {'services' : Service.objects.all()}

@json_view
def profile(request, id):
    try:
        person = Person.objects.get(id = id)
    except Person.DoesNotExist:
        return HttpResponseNotFound("Bad Id")
    if request.user.id != person.user.id:
        return HttpResponseForbidden('Not for your eyes')
    if request.method == 'GET':
        return {'person' : person, 'services' : Service.objects.all()}
    elif request.method == 'PUT':
        errors = {}
        try:
            with transaction.commit_on_success():
                data = json.loads(request.raw_post_data)
                if int(data['id']) != person.id:
                    return HttpResponseForbidden('Not for your eyes')
                #Save the info
                updated = data['person']
                person.description = updated['description']
                person.name = updated['name']
                person.ok_contact = updated['ok_contact']
                em = updated['email']
                if not is_email(em):
                    errors['email'] = 'Enter a valid email'
                else:
                    person.user.email = em
                ph = updated['phone']
                if not is_phone(ph):
                    errors['phone'] = 'Enter a valid phone number (xxx-xxx-xxxx)'
                else:
                    person.phone = ph
                person.beer = updated['beer']
            
                person.lat = Decimal(updated['lat'])
                person.lng = Decimal(updated['lng'])

                existing_services = set([s.name for s in person.services.all()])
                updated_services = set([s['name'] for s in updated['services']])

                to_add = updated_services - existing_services
                to_delete = existing_services - updated_services                
                for a in to_add:
                    try:
                        person.services.add(Service.objects.get(name = a))
                    except Service.DoesNotExist:
                        pass
                for d in to_delete:
                    try:
                        person.services.remove(Service.objects.get(name = d))
                    except Service.DoesNotExist:
                        pass
                person.save()
                person.user.save()
        except ValueError:
            pass

        
        return {'person' : person, 'services' : Service.objects.all(), 'errors' : errors}

@cacheable
@json_view
def karma(request, id):
    if request.method == 'POST' and request.user.is_authenticated():
        data = json.loads(request.raw_post_data)
        if data['person'] == int(id):
            try:
                person = Person.objects.get(id = data['person'])
                creator = Person.objects.get(user = request.user)
                description = data['description']
                karma = Karma(person = person, creator = creator, description = description)
                karma.save()
            except Person.DoesNotExist:
                pass
            except KeyError:
                pass
    karmas = Karma.objects.filter(person__id = id)
    return {'karma' : karmas}

@cacheable
@json_view
def flags(request, id):
    if request.method == 'POST' and request.user.is_authenticated():
        data = json.loads(request.raw_post_data)
        if data['person'] == int(id):
            try:
                person = Person.objects.get(id = data['person'])
                creator = Person.objects.get(user = request.user)
                description = data['description']
                flag = Flag(person = person, creator = creator, description = description)
                flag.save()
            except Person.DoesNotExist:
                pass
            except KeyError:
                pass
    flags = Flag.objects.filter(person__id = id)
    return {'flags' : flags}