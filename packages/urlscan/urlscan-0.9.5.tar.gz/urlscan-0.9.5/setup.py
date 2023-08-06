#!/usr/bin/env python3

from setuptools import setup

setup(name="urlscan",
      version="0.9.5",
      description="View/select the URLs in an email message or file",
      author="Scott Hansen",
      author_email="firecat4153@gmail.com",
      url="https://github.com/firecat53/urlscan",
      download_url="https://github.com/firecat53/urlscan/archive/0.9.5.zip",
      packages=['urlscan'],
      scripts=['bin/urlscan'],
      package_data={'urlscan': ['assets/*']},
      data_files=[('share/doc/urlscan', ['README.rst', 'COPYING']),
                  ('share/man/man1', ['urlscan.1'])],
      license="GPLv2",
      install_requires=["urwid>=1.2.1"]
      )
