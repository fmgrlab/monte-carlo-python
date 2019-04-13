from django.urls import path

from mcarlo_app import views

urlpatterns = [
 path('', views.home),
 path('about', views.about),
 path('iteration', views.demo_iteration),
 path('volatility', views.demo_volatility),
 path('risk', views.demo_risk)
]