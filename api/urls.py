from django.urls import path

from . import views

urlpatterns = [
    path('optimize/', views.optimize, name='optimize'),

]
