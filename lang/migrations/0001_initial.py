# Generated by Django 2.1.7 on 2019-05-12 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EntryData',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=255)),
                ('language', models.CharField(choices=[('pl', 'Polish'), ('en', 'English')], max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'dictionary_entry',
            },
        ),
        migrations.CreateModel(
            name='EntryRecordingData',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'dictionary_entry_recording',
            },
        ),
        migrations.CreateModel(
            name='RepeatedEntryData',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'repeated_entry',
            },
        ),
        migrations.CreateModel(
            name='RepetitionData',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'repetition',
            },
        ),
        migrations.CreateModel(
            name='TranslationData',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'dictionary_translation',
            },
        ),
        migrations.AlterUniqueTogether(
            name='entrydata',
            unique_together={('text', 'language')},
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('lang.entrydata',),
        ),
        migrations.CreateModel(
            name='RepeatedEntry',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('lang.repeatedentrydata',),
        ),
        migrations.CreateModel(
            name='Repetition',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('lang.repetitiondata',),
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('lang.translationdata',),
        ),
        migrations.AddField(
            model_name='translationdata',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='lang.Entry'),
        ),
        migrations.AddField(
            model_name='translationdata',
            name='translated',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translated', to='lang.Entry'),
        ),
        migrations.AddField(
            model_name='repeatedentrydata',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repeated_entries', to='lang.Entry'),
        ),
        migrations.AddField(
            model_name='repeatedentrydata',
            name='repetition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repeated_entries', to='lang.Repetition'),
        ),
        migrations.AddField(
            model_name='entryrecordingdata',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recordings', to='lang.Entry'),
        ),
        migrations.AlterUniqueTogether(
            name='translationdata',
            unique_together={('source', 'translated')},
        ),
    ]
