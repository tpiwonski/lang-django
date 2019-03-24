import attr

from dictionary.models import Word


@attr.s
class WordData(object):
    word = attr.ib(type=Word)


@attr.s
class FindByWordData(object):
    results = attr.ib(type=WordData, factory=list)


@attr.s
class GetWordsData(object):
    results = attr.ib(type=WordData, factory=list)
