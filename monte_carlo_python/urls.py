

from mcarlo_app import views
from django.urls import path

urlpatterns = [
 path('iteration', views.demo_iteration),
 path('risk', views.demo_risk)
]


