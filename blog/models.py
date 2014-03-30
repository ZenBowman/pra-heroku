from django.db import models
from django.contrib.auth.models import User
import markdown

class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField('Blog content')
    pub_date = models.DateTimeField('Date published')
    image = models.TextField('Image', null=True, blank=True)

    def markdown(self):
        return markdown.markdown(self.content)

    def __unicode__(self):
        return "%s:%s" % (self.pub_date, self.title)


class HeaderElement(models.Model):
    name = models.CharField(max_length=50)
    link = models.TextField(max_length=100)
    order = models.IntegerField()

    def __unicode__(self):
        return "%s:%s" % (self.order, self.name)


class ArcheryClassType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class ArcheryClass(models.Model):
    date = models.DateTimeField("Date of class")
    type = models.ForeignKey(ArcheryClassType)
    capacity = models.IntegerField(default=50)

    def num_registered(self):
        return len(ClassRegistration.objects.filter(archery_class = self))

    def __unicode__(self):
        return "%s @ %s" % (self.type, self.date.date())

class ClassRegistrationManager(models.Manager):
    def create_class(self, archery_class, user):
        a_class = self.create(archery_class=archery_class, user=user)
        return a_class

class ClassRegistration(models.Model):
    archery_class = models.ForeignKey(ArcheryClass)
    user = models.ForeignKey(User)

    objects = ClassRegistrationManager()

class BoardMember(models.Model):
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __unicode__(self):
        return "%s - %s" % (self.name, self.title)

class ClassDescription(models.Model):
    class_title = models.CharField(max_length=256)
    target_participants = models.TextField(max_length=2048)
    time_desc = models.TextField(max_length=2048)
    location = models.TextField(max_length=2048)
    cost = models.CharField(max_length=256)

    def __unicode__(self):
        return self.class_title
