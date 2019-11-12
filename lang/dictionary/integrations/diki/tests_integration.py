# -*- coding: utf-8 -*-
import re

import pytest

from .client import HtmlClient, HtmlParser
from .service import TranslationService


def test_translate():
    # client = HtmlClient()
    # results = client.translate('home')
    # pass
    service = TranslationService()
    results = service.translate('chilling')
    pass
