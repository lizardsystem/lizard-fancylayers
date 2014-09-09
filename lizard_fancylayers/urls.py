# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin
from django.views.i18n import javascript_catalog

from django.conf import settings

from lizard_ui.urls import debugmode_urlpatterns

from lizard_fancylayers import views

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^(([a-z0-9_]+-[a-zA-Z0-9-._]+/)*)$',
        views.HomepageView.as_view(),
        name="lizard_fancylayers.homepage",
        ),
    )

if getattr(settings, 'FANCYLAYERS_STANDALONE', False):
    urlpatterns += (
        url(r'^ui/', include('lizard_ui.urls')),
        url(r'^map/', include('lizard_map.urls')),
        url(r'^jsi18n/$', javascript_catalog, {
            'packages': ('lizard_fancylayers',)
            }),
    )
    urlpatterns += debugmode_urlpatterns()
