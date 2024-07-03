
from django.urls import path
from crur import views

urlpatterns = [
    path('', views.index, name="crur"),
    path('open', views.crur_open, name='open_request'),
    path('term', views.crur_term, name="term"),
    path('check', views.crur_check, name='check'),
    path('check/<str:term>', views.crur_check, name='check_term'),
    path('painel', views.crur_response, name='painel'),
    path('response', views.crur_response, name='response'),
    path('response/<str:term>', views.crur_response, name='response'),
    path('authorize/<str:pk>', views.authorizar, name="authorize"),
    path('register', views.register, name='register'),
    path('login', views.login_view, name="crur_login"),
    path('archives/<int:pk>', views.archives, name="archives")

]
