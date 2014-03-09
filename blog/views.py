from django.shortcuts import render
from django.http import HttpResponse
from models import BlogPost, HeaderElement, ArcheryClass, ClassRegistration, BoardMember
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from datetime import date

import qrcode

def renderWithHeader(request, template, dict):
    if request.user.is_authenticated():
        dict["username"] = request.user.username
    header_list = HeaderElement.objects.order_by('order')
    dict["header_list"] = header_list
    return render(request, template, dict)

class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/")

def is_user_signed_up_for_class(some_user, some_class):
    return len(ClassRegistration.objects.filter(archery_class=some_class, user=some_user)) > 0

def classes(request):
    show_full_msg = request.GET.get("full") == "true"
    classes = ArcheryClass.objects.order_by('date')
    enrolled_classes_for_user = []
    if request.user.is_authenticated():
        for c in classes:
            if is_user_signed_up_for_class(request.user, c):
                enrolled_classes_for_user.append(c)
    return renderWithHeader(request, 'blog/classes.html', {
        'show_full_msg' : show_full_msg,
        'classes' : classes,
        'enrolled_classes': enrolled_classes_for_user})

def thanks(request):
    return renderWithHeader(request, 'blog/thanks.html', {})

def user_exists(request):
    form = RegisterForm()
    return renderWithHeader(request, 'blog/register.html', {'form' : form, 'userexists': True})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data["email"]
            if (len(User.objects.filter(email = new_email)) > 0):
                return HttpResponseRedirect("userexists/")
            user = User.objects.create_user(new_email, new_email, form.cleaned_data["password"])
            user.save()
            return HttpResponseRedirect("thanks/")
    else:
        form = RegisterForm()
        return renderWithHeader(request, 'blog/register.html', { 'form': form, 'userexists': False })

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            pwd = form.cleaned_data["password"]
            user = authenticate(username=username, password=pwd)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/")
            return HttpResponseRedirect("/blog/login_failed/")
    else:
        form = LoginForm()
        return renderWithHeader(request, 'blog/login.html', { 'form': form })


# Create your views here.
def index(request):
    blog_list = BlogPost.objects.order_by('-pub_date')
    context = {'blog_list': blog_list}
    return renderWithHeader(request, 'blog/index.html', context)

@login_required
def signup(request):
    class_id = request.GET.get("class_id")
    class_by_id = ArcheryClass.objects.filter(id = class_id)[0]
    if request.user:
        if (class_by_id.num_registered() < class_by_id.capacity):
            ClassRegistration.objects.create_class(class_by_id, request.user)
        else:
            HttpResponseRedirect("/blog/classes?full=true")
    return HttpResponseRedirect("/blog/classes/")

def about(request):
    return renderWithHeader(request, 'blog/about.html', {})

@login_required
def request_qr(request):
    user = request.user
    img = qrcode.make('%s/blog/check_user_classes?id=%s' % (request.get_host(), user.id))
    response = HttpResponse(mimetype="image/bmp")
    img.save(response, "BMP")
    return response

@login_required
def check_user_classes(request):
    user = request.user
    classes_for_user = ClassRegistration.objects.filter(user=user)
    upcoming_classes = []
    for c in classes_for_user:
        if c.archery_class.date.date() >= date.today():
            upcoming_classes.append(c)
    return renderWithHeader(request, 'blog/upcoming_classes.html', {
        'upcoming_classes':upcoming_classes,
        'today':date.today()
    })

@login_required
def deregister(request):
    class_id = request.GET.get("class_id")
    user = request.user
    archery_class = ArcheryClass.objects.filter(id = class_id)[0]
    ClassRegistration.objects.filter(archery_class=archery_class, user=user).delete()
    return classes(request)

def team(request):
    board_members = BoardMember.objects.order_by('id')
    return renderWithHeader(request, 'blog/team.html', {
        'board_members': board_members
    })