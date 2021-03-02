from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('quotes', views.allquotes),
    path('delete/<int:idQuote>', views.deletequote),
    path("createquote", views.createquote),
    path("user/<int:idQuote>", views.userquotes),
    path("myaccount/<int:idUser>", views.editaccount),
    path("updateaccount/<int:idUser>", views.updateaccount),
    path("like/<int:idQuote>", views.like)
]