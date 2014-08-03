from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from buspeople.decorators import json_view
from models import Person, Service, Activation
from forms import LoginForm, RegisterForm, RetrieveForm, ResetForm
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from util import send_activation


def context(request):
	d = {}
	if request.user.is_authenticated():
		d['person'] = Person.objects.get(user = request.user)
	return RequestContext(request, d) 

def home(request):
	return render_to_response('home.html', 
		{
			'login' : LoginForm(),
			'register' : RegisterForm()
		},
		context(request))






def login(request):
	if request.method == 'POST':

		form = LoginForm(request)
		if form.is_valid():
			form.save()
			resp = render_to_string('forms/login.html',
				{'login' : form},
				context(request))
			return HttpResponse(resp)
		else:
			resp = render_to_string('forms/login.html', 
				{'login' : form},
				context(request))
			return HttpResponseForbidden(resp)
	
	return HttpResponseRedirect('/#logreg')


def logout(request):
	auth_logout(request)
	return HttpResponseRedirect('/')

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			(person, activate) = form.save()
			send_activation(person, activate)
			resp = render_to_string('forms/register.html',
				{'register' : form},
				context(request))
			return HttpResponse(resp)
		else:
			resp = render_to_string('forms/register.html', 
				{'register' : form},
				context(request))
			return HttpResponseForbidden(resp)
	
	return HttpResponseRedirect('/#logreg')


def activate(request, key):
	try:
		activate = Activation.objects.get(key = key)
		person = activate.person
		person.user.is_active = True
		person.save()
		activate.delete()
		success = True
	except Activation.DoesNotExist:
		success = False
	return render_to_response('activation.html',
		{'success' : success},
		 context(request))


def about(request):
	return render_to_response('about.html', context(request))

def retrieve(request):
	if request.method == 'GET':
		form = RetrieveForm()
	elif request.method == 'POST':
		form = RetrieveForm(request.POST)
		if form.is_valid():
			form.save()
			resp = render_to_string('forms/password_form.html', {'form' : form}, context(request))
			return HttpResponse(resp)
		else:
			resp = render_to_string('forms/password_form.html', {'form' : form}, context(request))
			return HttpResponseForbidden(resp)
	return render_to_response('retrieve.html', {'form' : form}, context(request))


def reset_password(request, key):
	if request.method == 'GET':
		form = ResetForm()
	elif request.method == 'POST':
		form = ResetForm(request.POST)
		if form.is_valid():
			form.save(key)
			resp = render_to_string('forms/reset_password_form.html', {'form' : form}, context(request))
			return HttpResponse(resp)
		else:
			resp = render_to_string('forms/reset_password_form.html', {'form' : form}, context(request))
			return HttpResponseForbidden(resp)
	return render_to_response('reset.html', {'form' : form}, context(request))
