
from django.conf.urls import url,include

urlpatterns = [
 url(r'^mcarlo/', include('mcarlo_app.urls')),
]
