#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'modelmock',
  version = '0.1.0',
  description = 'A simple faked JSON generator',
  author = 'acegik',
  license = 'GPL-3.0',
  url = 'https://github.com/acegik/modelmock',
  download_url = 'https://github.com/acegik/modelmock/downloads',
  keywords = ['faker', 'json', 'jsonschema'],
  classifiers = [],
  install_requires = open("requirements.txt").readlines(),
  python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
  package_dir = {'':'lib'},
  packages = setuptools.find_packages('lib'),
)
