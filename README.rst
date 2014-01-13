lizard-fancylayers
==========================================

Lizard-fancylayers is an app that tries to be relatively simple (it's
a prototype, not a full fledged app) that visualizes data coming from
lizard-datasource.


Installation notes
------------------

There are a few dependencies that you also need to add to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'lizard_fancylayers',
        'lizard_datasource',
        'colorful',
        ...
        )

In case FEWS JDBC is used as a datasource (the only option as of the
time of writing), there is also a script that runs every minute, to
see if there are new latest values in it. It is run through supervisor.

To the [supervisor] part in Buildout (usually in server.cfg), a line like::

      40 cache_latest_values (autostart=false autorestart=false startsecs=0) ${buildout:bin-directory}/django [cache_latest_values]

should be added. This line makes sure that a command
"bin/supervisorctl start cache_latest_values" is available, which in
turn makes sure that there is always at most one copy of the script
running.

Then, a cronjob that calls that should also be added, and it should
run _every minute_ (almost all the time, the script will immediately
conclude it has nothing to do and exit). E.g.::

    [latest-values-cronjob]
    recipe = z3c.recipe.usercrontab
    times = * * * * *
    command = ${buildout:bin-directory}/supervisorctl start cache_latest_values > /dev/null

Don't forget to add it to parts too, for instance in production.cfg.

Finally, add lizard-fancylayers to the site's urls.py. It's usually
under /fancy/, and that will be used below, but of course that's not
necessary.


Configuration
-------------

As of the time of writing, lizard-fancylayers is usually used to take
some layer defined in FEWS JDBC, and add colors, extra graph lines or
percentiles to it. Here is how to do that.

1. Go to http://yoursitesurl.lizard.net/fancy/

   This searches for available datasources, and as a side effect saves a
   config object that can be edited in the admin for each of them.

2. Create an augmented datasource. The augmented source is the thing
we want to add things to; if you want to add to the FEWS JDBC source
with slug "some_slug", choose "'some_slug' from app 'lizard_fewsjdbc'".

3. Go to /admin/lizard_datasource/datasourcemodel/ . Make the
augmented datasource visible, and all other datasources invisible. Run
the cache_latest_values script on it (it's an action in the "Action"
pulldown at the top).

4. Go to /fancy/ again -- you should now see data coming from FEWS, a
tree of filters to choose from.

5. Go to the datasource layers in the admin, and find all the layers
you want to do something with. If some combination of
slug/filter/parameter occurs more than once, pick the one belonging to
your augmented datasource model. Give the layers you want to use for
something a nickname.
