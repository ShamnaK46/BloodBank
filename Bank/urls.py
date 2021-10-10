from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('', views.home, name='home'),
    path('display', views.display, name='display'),
    path('logout', views.logout, name='logout'),
    path('add-donor', views.adddonor, name ='adddonor')
]