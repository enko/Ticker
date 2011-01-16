import re

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from frontend.models import *

class EntryHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE')
    fields = ('id', 'text','published','isPublic')
    exclude = (re.compile(r'^private_'))
    model = Entry

    @classmethod
    def content_size(self, entry):
        return len(entry.content)

    def read(self, request, id):
        if (id == '0'):
            entries = Entry.objects.all()
            return entries
        else:
            entries = Entry.objects.get(id=id)
            return entries

    @throttle(5, 10*60) # allow 5 times in 10 minutes
    def update(self, request, id):
        entries = Entry.objects.get(id=id)

        entries.title = request.PUT.get('title')
        entries.save()

        return entries

    def delete(self, request, id):
        entries = Entry.objects.get(id=id)

        if not request.user == entries.author:
            return rc.FORBIDDEN # returns HTTP 401

        entries.delete()

        return rc.DELETED # returns HTTP 204

class ArbitraryDataHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request, username, data):
        user = User.objects.get(username=username)

        return { 'user': user, 'data_length': len(data) }
