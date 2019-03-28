"""monte_carlo_python URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from mcarlo_app import views
from django.urls import path


urlpatterns = [

    path('', views.home),
    path('demo/iteration', views.demo_iteration),
    path('demo/volatility', views.demo_volatility, name='demo-volatilily'),
    path('demo/risk', views.demo_risk, name='demo-risk'),

    path('api/iteration', views.api_iteration, name='api-iteration'),
    path('api/volatility', views.api_iteration, name='api-volatilily'),
    path('api/risk', views.api_iteration, name='api-risk'),
]
