#!/usr/bin/env python
# encoding: utf-8

"""
Flask-SQLAlchemy-Historify
--------------------------

Flask-SQLAlchemy-Historify is a Flask plugin that provides full
accountability/change logs for SQLAlchemy database models.
"""

setup(
    name                 = 'Flask-SQLAlchemy-Historify',
    version              = '1.0',
    url                  = 'https://github.com/d0c-s4vage/flask_sqlalchemy_historify',
    license              = 'MIT',
    author               = 'James "d0c-s4vage" Johnson',
    author_email         = 'd0c.s4vage@gmail.com',
    description          = 'A decorator for SQLAlchemy models that records a full changelog',
    long_description     = __doc__,
    py_modules           = ['flask_sqlalchemy_historify'],
    zip_safe             = False,
    include_package_data = True,
    platforms            = 'any',
    install_requires     = [
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Login'
    ],
    classifiers          = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
