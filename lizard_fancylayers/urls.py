# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin
from lizard_ui.urls import debugmode_urlpatterns

from lizard_fancylayers import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^ui/', include('lizard_ui.urls')),
    url(r'^map/', include('lizard_map.urls')),

    url(r'^(([a-z0-9_]+-[a-zA-Z0-9-._]+/)*)$',
        views.HomepageView.as_view(),
        name="lizard_fancylayers.homepage",
        ),
    )

urlpatterns += debugmode_urlpatterns()
