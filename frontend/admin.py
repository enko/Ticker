from wapticker.frontend.models import Entry
from django.contrib import admin

#class EntryAdmin(admin.ModelAdmin):
#	fieldsets = [
#		(None,			{'fields': ['text', 'isPrivate']}),
#		('Eintragsdatum',	{'fields': ['published'], 'classes': ['collapse']}),
#	]

admin.site.register(Entry)

