#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'jsonfaker',
  version = '0.0.1',
  description = 'A simple faked JSON generator',
  author = 'acegik',
  license = 'GPL-3.0',
  url = 'https://github.com/acegik/jsonfaker',
  download_url = 'https://github.com/acegik/jsonfaker/downloads',
  keywords = ['sysops', 'devops', 'tools'],
  classifiers = [],
  install_requires = open("requirements.txt").readlines(),
  python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
  package_dir = {'':'lib'},
  packages = setuptools.find_packages('lib'),
)
