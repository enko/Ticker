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


def index(request, pin=None):
	if pin == None:
		entries = Entry.objects.filter(isPublic=1).order_by('-published')
	elif pin == Config.objects.get(key='pin').value: 
		entries = Entry.objects.all().order_by('-published')
	elif pin != Config.objects.get(key='pin').value:
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
	entries = Entry.objects.all().order_by('-published')
	pin = Config.objects.get(key='pin')
	if request.method == 'POST':
		if 'newEntry' in request.POST:
			if len(request.POST["newEntry"]) > 140:
				return HttpResponse("Message too long!", mimetype="text/plain")
			else:
				entryText = escape(request.POST["newEntry"])
				publishTime = datetime.now()
				status = int(request.POST["isPublic"])
				newEntry = Entry(text=entryText, published=publishTime, isPublic=status)
				newEntry.save()
		elif 'pin' in request.POST:
			if len(request.POST["pin"]) < 6:
				return HttpResponse("At least six chars!", mimetype="text/plain")
			elif request.POST["pin"] == pin.value:
				return HttpResponse("This is the same pin, isn't it?", mimetype="text/plain")
			else:
				pin.value = request.POST["pin"]
				pin.save()
		elif 'deleteEntry' in request.POST:
			target = request.POST['deleteEntry']
			Entry.objects.filter(id=target).delete()
	if request.method == 'GET':
		if 'entries.json' in request.GET:
			newEntry = Entry.objects.all().order_by('-published')
			json_serializer = serializers.get_serializer("json")()
			return HttpResponse(json_serializer.serialize(newEntry, ensure_ascii=False))
		elif 'refresh.json' in request.GET:
			newEntry = Entry.objects.all().order_by('-published')[:2]
			json_serializer = serializers.get_serializer("json")()
			return HttpResponse(json_serializer.serialize(newEntry, ensure_ascii=False))
	return render_to_response('ticker/manage.html', {'entries': entries, 'pin': pin})
