import uuid

from lang.repetitions.db.repetition import RepetitionData, RepeatedEntryData


class Repetition(RepetitionData):

    class Meta:
        proxy = True


    def add_entry(self, entry):
        repeated_entry = RepeatedEntry(id=uuid.uuid4(), repetition=self, entry=entry)
        self._repeated_entries.append(repeated_entry)


class RepeatedEntry(RepeatedEntryData):

    class Meta:
        proxy = True
