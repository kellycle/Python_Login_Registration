from django.urls import path
from . import views

urlpatterns = [
    # Display
    path('', views.index),
    path('success', views.success),

    # Action
    path('register', views.register),
    path('login', views.login),
    path('logOut', views.log_out),
]