from django.urls import path
from . import views

urlpatterns = [
    # Template views
    path('login/', views.login_view, name='login'),
    path('login/submit/', views.login_submit, name='login_submit'),
    #path('register/company/', views.company_registration_view, name='company_registration'),
    #path('register/user/', views.user_registration_view, name='user_registration'),

    # API endpoints
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    #path('api/register/company/', views.api_company_registration, name='api_company_registration'),
    #path('api/register/user/', views.api_user_registration, name='api_user_registration'),
]
