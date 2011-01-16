# coding=utf-8
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms.models import modelformset_factory
from Ticker.frontend.models import *
from datetime import datetime
from django.core import serializers
from django.utils.html import escape
import json


def index(request, pin=None):
	if (pin == None):
		entries = Entry.objects.filter(isPublic=1).order_by('-published')
	elif (pin == Config.objects.get(key='pin').value): 
		entries = Entry.objects.all().order_by('-published')
	elif (pin != Config.objects.get(key='pin').value):
		return redirect(index)
		
	paginator = Paginator(entries, 10)
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	
	try:
		entries = paginator.page(page)
	except (EmptyPage, InvalidPage):
		entries = paginator.page(paginator.num_pages)
	return render_to_response('ticker/index.html', {'entries': entries})

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect(request.POST['redirect'])
			else:
				return HttpResponse('Account gesperrt.')
		else:
			#Hier muesste noch eine Message rein, damit klar ist das das Login schief ging.
			return redirect(login)
		return render_to_response('ticker/profile.html')
	else:
		form = AuthenticationForm()
		if 'redirect' in request.GET:
			redirect = request.GET['redirect']
		else:
			redirect = '/'
		return render_to_response('ticker/login.html', {'form': form, 'redirect': redirect})

def logout(request):
	auth_logout(request)
	return HttpResponseRedirect('/')

@login_required(redirect_field_name='redirect')
def manage(request):
	if (request.method == 'POST'):
		if ('submit' in request.POST):
			if ('new_entry' in request.POST):
				entry_text = escape(request.POST["entry-text"])
				entry_published = datetime.now()
				entry_isPublic = int(request.POST["entry-is-public"])
				new_entry = Entry(text=entry_text, published=entry_published, isPublic=entry_isPublic)
				new_entry.save()
			elif ('new_pin' in request.POST):
				new_pin = Config.objects.get(key='pin')
				new_pin.value = request.POST['pin-value']
				new_pin.save()
			elif ('del_entry' in request.POST):
				entry_id = request.POST['entry-id']
				Entry.objects.filter(id=entry_id).delete()

	if (request.method == 'GET'):
		if ('format' in request.GET):
			format = request.GET['format']
		else:
			format = 'json'
			
		if ('function' in request.GET) and (format == 'json'):
			json_serializer = serializers.get_serializer("json")()
			if (request.GET['function'] == 'get_all_entries'):
				# ?format=json&function=get_all_entries
				all_entries = Entry.objects.all().order_by('-published')
				return HttpResponse(json_serializer.serialize(all_entries, ensure_ascii=False), mimetype="application/json")
			elif (request.GET['function'] == 'get_latest_entry'):
				latest_entry = Entry.objects.all().order_by('-published')[:1]
				return HttpResponse(json_serializer.serialize(latest_entry, ensure_ascii=False), mimetype="application/json")
			elif (request.GET['function'] == 'get_pin'):
				pin = Config.objects.filter(key='pin')
				return HttpResponse(json_serializer.serialize(pin, ensure_ascii=False), mimetype="application/json")
			else:
				not_defined_message = "This json function is not defined!"
				return HttpResponse(not_defined_message, mimetype="text/plain")
		elif ('function' in request.GET) and (format == 'plain'):
			if (request.GET['function'] == 'get_count'):
				count = len(Entry.objects.all())
				return HttpResponse(count, mimetype="text/plain")
			else:
				not_defined_message = "This plain function is not defined!"
				return HttpResponse(not_defined_message, mimetype="text/plain")
	
	return render_to_response('manage/index.html')
