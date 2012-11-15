import logging
import mapnik
import os
import random

from django.conf import settings

from lizard_map import coordinates
from lizard_map import workspace
from lizard_map.mapnik_helper import add_datasource_point
from lizard_map.models import ICON_ORIGINALS
from lizard_map.symbol_manager import SymbolManager

from lizard_datasource import properties
from lizard_datasource import datasource

logger = logging.getLogger(__name__)


def html_to_mapnik(color):
    r, g, b = color[0:2], color[2:4], color[4:6]
    rr, gg, bb = int(r, 16), int(g, 16), int(b, 16)

    return rr / 255.0, gg / 255.0, bb / 255.0, 1.0


def symbol_filename(color):
    symbol_manager = SymbolManager(
        ICON_ORIGINALS,
        os.path.join(settings.MEDIA_ROOT, 'generated_icons'))

    output_filename = symbol_manager.get_symbol_transformed(
        'meetpuntPeil.png', mask=('meetpuntPeil_mask.png',),
        color=color)
    output_filename_abs = os.path.join(
        settings.MEDIA_ROOT, 'generated_icons', output_filename)
    return output_filename_abs


class FancyLayersAdapter(workspace.WorkspaceItemAdapter):
    """Registered as adapter_fancylayers."""

    def __init__(self, *args, **kwargs):
        super(FancyLayersAdapter, self).__init__(*args, **kwargs)

        self.choices_made = datasource.ChoicesMade(
            json=self.layer_arguments['choices_made'])
        self.datasource = datasource.CombinedDataSource(
            choices_made=self.choices_made)

    def layer(self, layer_ids=None, webcolor=None, request=None):
        logger.debug("In lizard_fancylayers.layer")
        # We only do point layers right now
        if not self.datasource.has_property(properties.LAYER_POINTS):
            logger.debug("Datasource is not a point layer.")
            return [], {}

        layers = []
        styles = {}

        locations = list(self.datasource.locations())
        colors = {"default": html_to_mapnik('0000ff')}
        logger.debug("1")
        for location in locations:
            if 'color' in location:
                colors[location['color']] = html_to_mapnik(location['color'])

        style = mapnik.Style()
        logger.debug("2")

        for colorname, color in colors.iteritems():
            rule = mapnik.Rule()
            symbol = mapnik.PointSymbolizer(
                symbol_filename(color), 'png', 16, 16)
            symbol.allow_overlap = True
            rule.symbols.append(symbol)
            rule.filter = mapnik.Filter("[Color] = '{0}'".format(colorname))
            style.rules.append(rule)

        styles['trivialStyle'] = style
        logger.debug("3")

        layer = mapnik.Layer("Fancy Layers layer", coordinates.WGS84)
        layer.datasource = mapnik.PointDatasource()
        layer.styles.append('trivialStyle')
        logger.debug("4 - {0}".format(locations))

        for location in locations:
            color = location.get('color', 'default')
            logger.debug('{0}: {1}'.format(location, color))
            add_datasource_point(
                layer.datasource, location['longitude'],
                location['latitude'],
                'Color', str(location.get('color', 'default')))
        logger.debug("5")

        layers.append(layer)
        return layers, styles
