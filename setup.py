from setuptools import setup

version = '0.9.dev0'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django',
    'django-extensions',
    'django-nose',
    'lizard-ui >= 4.0',
    'lizard-map >= 4.0',
    'lizard-datasource >= 0.7'
    ],

tests_require = [
    ]

setup(name='lizard-fancylayers',
      version=version,
      description="TODO",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='Remco Gerlich',
      author_email='remco.gerlich@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['lizard_fancylayers'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
          ],
          'lizard_map.adapter_class': [
          'adapter_fancylayers = lizard_fancylayers.layers:FancyLayersAdapter'
            ],
          }
      )
