# -*- coding: utf-8 -*-
__version__ = '0.2.0'
__author__ = 'Ramiro Gómez <code@ramiro.org>'
__name__ = 'wcap'
__description__ = 'Capture web pages as images using Selenium and the FireFox webdriver.'
__all__ = ['get_browser', 'capture']


from .wcap import get_browser, capture