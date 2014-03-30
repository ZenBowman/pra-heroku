from django.contrib import admin
from django import forms
from blog.models import *

admin.site.register(BlogPost)
admin.site.register(ArcheryClassType)
admin.site.register(ArcheryClass)
admin.site.register(ClassRegistration)
admin.site.register(BoardMember)
admin.site.register(ClassDescription)


