from django.urls import path
from code_rate.views import rate
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('rate/', rate),
] + static(settings.STATIC_URL)

urlpatterns += staticfiles_urlpatterns()
