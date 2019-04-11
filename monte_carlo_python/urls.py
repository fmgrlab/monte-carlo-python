

from mcarlo_app import views
from django.urls import path

urlpatterns = [
 path('', views.home),
 path('about', views.about),
 path('iteration', views.demo_iteration),
path('volatility', views.demo_volatility),
 path('risk', views.demo_risk)
]



handler404 = views.handler404
handler500 = views.handler500
handler505 = views.handler504