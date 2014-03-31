from django.conf.urls import patterns, url

from blog import views

urlpatterns = patterns(
    '',
    url(r'team/', views.team, name='team'),
    url(r'deregister', views.deregister, name='deregister'),
    url(r'^check_user_classes/', views.check_user_classes, name='check_user_classes'),
    url(r'^sendqr/', views.request_qr, name='request_qr'),
    url(r'^about/', views.about, name='about'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^contentpage/', views.contentpage),
    url(r'^classes/upcoming', views.upcoming_classes, name='upcoming_classes'),
    url(r'^classes', views.classes, name='classes'),
    url(r'^logout/', views.logout_page, name='logout'),
    url(r'^login/', views.login_page, name='login'),
    url(r'^register/userexists', views.user_exists, name='user_exists'),
    url(r'^register/thanks', views.thanks, name='thanks'),
    url(r'^register', views.register, name='register'),
    url(r'^$', views.index, name='index')
)
