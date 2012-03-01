from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.geo.index',
      version=version,
      description="spatialindex for collective.geo",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://plone.org/products/collective.geo.index/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.geo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Products.CMFPlone',
          'shapely',
          'Rtree',
          'collective.geo.contentlocations',
          'collective.geo.mapwidget',
          'collective.geo.kml',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
