from django.contrib import admin
from django.urls import path
import goolytics.views as goolytics


urlpatterns = [
    path('start', goolytics.startSession),
    path('track', goolytics.track),
    path('view/browser', goolytics.get_browser_data),
    path('view/activity', goolytics.get_site_activity),
]
