#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re

from distutils.core import setup


rel_file = lambda *args: os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

def get_version():
    initfile = open(rel_file("src", "django_factory", "__init__.py")).read()
    return re.search(r"__version__ = \"([^\"]+)\"", initfile).group(1)


setup(
    name="django-factory",
    version=get_version(),
    author="Daniel Quinn",
    author_email="code@danielquinn.org",
    url="http://github.com/danielquinn/django-factory",
    description="Class factories for Django",
    packages=("django_factory",),
    package_dir={"": "src"},
    requires=("django (>=1.2)",),
    classifiers=[
	"Development Status :: 3 - Alpha",
	"Framework :: Django",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: GNU Affero General Public License v3",
	"Natural Language :: English",
	"Programming Language :: Python :: 2.5",
	"Programming Language :: Python :: 2.6",
	"Programming Language :: Python :: 2.7"
    ],
)
