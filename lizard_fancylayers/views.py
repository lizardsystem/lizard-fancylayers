# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals

import logging

from django.core.urlresolvers import reverse

from lizard_map.views import AppView
from lizard_datasource import datasource

logger = logging.getLogger(__name__)


class FancyLayersView(AppView):
    # Placeholder for our own utils later
    pass


class HomepageView(FancyLayersView):
    template_name = 'lizard_fancylayers/homepage.html'

    def make_url(self, choices_made):
        options = "".join("{0}-{1}/".format(
                item[0], item[1]) for item in choices_made.items())
        return reverse("lizard_fancylayers.homepage", args=(options,))

    def dispatch(self, request, choices, *args):
        self.choices_made = self.make_choices_made(choices)
        return super(HomepageView, self).dispatch(request)

    def make_choices_made(self, choices):
        choicelist = choices.split('/')[:-1]
        logger.debug("CHOICES: {0}".format(choicelist))

        choicedict = {}
        for choice in choicelist:
            identifier, value = choice.split('-')
            choicedict[identifier] = value

        return datasource.ChoicesMade(dict=choicedict)

    @property
    def datasource(self):
        if not hasattr(self, '_datasource'):
            self._datasource = datasource.CombinedDataSource(self.choices_made)
        return self._datasource

    def chooseable_criteria(self):
        try:
            criteria = self.datasource.chooseable_criteria()
            for criterion in criteria:
                for value in criterion['values']:
                    # Suppose we chose this value
                    new_choices_made = self.choices_made.add(
                        criterion['criterion'].identifier,
                        value['identifier'])
                    # Could we draw it on the map then?
                    if self.datasource.is_drawable(new_choices_made):
                        # Make it a workspace-acceptable
                        value['workspace_acceptable'] = True
                    else:
                        # Give it a URL that makes it choosable
                        value['url'] = self.make_url(new_choices_made)

            return criteria
        except Exception, e:
            logger.debug("Caught exception in chooseable_criteria: {0}".
                         format(e))

    def forgettable_criteria(self):
        forgettable_criteria = []
        for criterion in self.datasource.criteria():
            if criterion.identifier not in self.choices_made:
                continue
            forgettable_criteria.append({
                    'identifier': criterion.identifier,
                    'description': criterion.description,
                    'url': self.make_url(
                        self.choices_made.forget(criterion.identifier))
                    })

        return forgettable_criteria
