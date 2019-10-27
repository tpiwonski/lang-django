from dataclasses import dataclass
from typing import List


@dataclass
class RecordingData(object):
    url: str


@dataclass
class ExampleData(object):
    text: str
    translation: str
    recording: RecordingData


@dataclass
class TranslationEntryData(object):
    text: str
    url: str


@dataclass
class TranslationData(object):
    language: str
    type: int
    entries: List[TranslationEntryData]
    recordings: List[RecordingData]
    examples: List[ExampleData]


@dataclass
class EntryData(object):
    text: str
    language: str
    type: int
    url: str
    translations: List[TranslationData]
    recordings: List[RecordingData]
