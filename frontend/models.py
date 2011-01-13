# coding=utf-8
from django import forms
from django.db import models
from django.forms import ModelForm 

STATUS = (
	('1', 'public'),
	('0', 'private'),
)

class Entry(models.Model):
	id = models.AutoField(primary_key=True)
	text = models.CharField(max_length=140)
	published = models.DateTimeField(auto_now=True)
	isPublic = models.CharField(max_length=1, default=0, choices=STATUS)

	def __unicode__(self):
		return self.text

class Config(models.Model):
	key = models.CharField(max_length=50,primary_key=True)
	value = models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.key
		
class ConfigForm(ModelForm):
	class Meta:
		model = Config
