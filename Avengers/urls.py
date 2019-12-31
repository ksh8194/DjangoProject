
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
import Avengers
from Avengers import views


urlpatterns = [
   
    path('selected', views.SelectedFunc),
    path('register1', views.RegisterFunc1),
    path('login',views.LoginFunc),
    path('register2',views.RegisterFunc2),
    path('logout',views.LogoutFunc),
    path('calendar',views.CalendarFunc),
    path('delete',views.DeleteFunc),
    path('insert1',views.InsertFunc1),
    path('insert2',views.InsertFunc2),
]
