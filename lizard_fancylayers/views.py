# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals

from lizard_map.views import AppView
from lizard_datasource import datasource


class FancyLayersView(AppView):
    # Placeholder for our own utils later
    pass


class HomepageView(FancyLayersView):
    template_name = 'lizard_fancylayers/homepage.html'

    def datasource(self):
        return datasource.CombinedDataSource()
