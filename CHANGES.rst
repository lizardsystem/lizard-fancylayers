Changelog of lizard-fancylayers
===================================================


0.11 (unreleased)
-----------------

- Move to mapnik 2.2.0.
- Remove nested 'ui' and 'map' urls when not running standalone.


0.10 (2013-06-06)
-----------------

- Use new lizard-datasource method to show labels and y-axes.


0.9 (2013-04-23)
----------------

- Fix bug with configured default icons -- Mapnik can't handle Unicode
  filenames.


0.8 (2013-04-11)
----------------

- Let the standard color and standard icon be configured using
 lizard-map's Settings (FANCYLAYERS_DEFAULT_COLOR,
 FANCYLAYERS_DEFAULT_SYMBOL_NAME and FANCYLAYERS_DEFAULT_SYMBOL_MASK)

- Show first graph in normal color, next graph lines in green

- Work with latest datasource timeseries API

- Get graph legend correct, from timeseries' column names


0.7 (2013-04-10)
----------------

- Make it possible to show several timeseries from one location in one
  graph. Doesn't look nice yet.


0.6 (2013-03-19)
----------------

- Hiding the legend if there's no proper legend to be found.

- Fixed icon before popup graph title.


0.5 (2013-02-12)
----------------

- Implement a legend() function using lizard-datasource's
  location_annotations.


0.4 (2013-01-16)
----------------

- Added a values() method to the adapter, so that CSV files with
  values can be downloaded.

- Show a unit in the popup.

0.3 (2013-01-03)
----------------

- If a popup is shown for several identifiers at once, they are now
  shown as separate graphs, instead of all timeseries in the same
  graph. Mainly because the combined graphs got very messy once
  percentiles were involved.


0.2 (2012-12-20)
----------------

- Add support for percentiles, colors.


0.1 (2012-11-15)
----------------

Not really working yet, but making a release for test purposes.
