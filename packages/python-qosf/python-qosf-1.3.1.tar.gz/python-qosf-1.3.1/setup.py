#!/usr/bin/env python

import QOpenScienceFramework
from setuptools import setup

setup(
	name="python-qosf",
	version=QOpenScienceFramework.__version__,
	description="Qt widgets for the Open Science Framework",
	author=QOpenScienceFramework.__author__,
	author_email="dschreij@gmail.com",
	url="https://github.com/dschreij/QOpenScienceFramework",
	classifiers=[
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'Environment :: MacOS X',
		'Environment :: Win32 (MS Windows)',
		'Environment :: X11 Applications',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
	install_requires=[
		'qtpy',
		'arrow',
		'humanize',
		'python-fileinspector',
		'requests-oauthlib>=0.6',
		'qtawesome>=0.5.7',
		'python-dotenv'
	],
	include_package_data=True,
	packages = ['QOpenScienceFramework'],
)
