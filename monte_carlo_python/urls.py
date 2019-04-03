
from django.conf.urls import url,include
from mcarlo_app import views
urlpatterns = [
 url(r'^mcarlo/', include('mcarlo_app.urls')),
]

handler404 = views.handler404
handler500 = views.handler500
handler505 = views.handler504