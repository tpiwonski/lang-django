from dataclasses import dataclass
from typing import List


@dataclass
class RecordingData(object):
    audio_url: str


@dataclass
class ExampleData(object):
    text: str
    translation: str
    recording: RecordingData


@dataclass
class TranslationEntryData(object):
    text: str
    source_url: str
    usage_notes: str


@dataclass
class TranslationData(object):
    language: str
    type: int
    entries: List[TranslationEntryData]
    recordings: List[RecordingData]
    examples: List[ExampleData]


@dataclass
class HeadwordData:
    text: str
    source_url: str
    recordings: List[RecordingData]


@dataclass
class EntryData(object):
    language: str
    headwords: List[HeadwordData]
    translations: List[TranslationData]
