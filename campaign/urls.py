from django.urls import path
from . import views

urlpatterns = [
    path('redirect/<str:ref_code>/', views.redirect_and_track, name='redirect_and_track_emails'),
    path('dashboard-test-not-functional/', views.dashboard_non_functional, name='dashboard_non_functional'),
    path('dashboard/', views.beta_dashboard, name='beta_dashboard'),
]
