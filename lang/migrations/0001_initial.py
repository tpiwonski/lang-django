# Generated by Django 2.1.7 on 2019-08-22 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EntryModel',
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
            name='ExampleModel',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'dictionary_example',
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
            name='TranslationExampleModel',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'dictionary_translation_example',
            },
        ),
        migrations.CreateModel(
            name='TranslationModel',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'dictionary_translation',
            },
        ),
        migrations.AlterUniqueTogether(
            name='entrymodel',
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
            bases=('lang.entrymodel',),
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('lang.examplemodel',),
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
            bases=('lang.translationmodel',),
        ),
        migrations.CreateModel(
            name='TranslationExample',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('lang.translationexamplemodel',),
        ),
        migrations.AddField(
            model_name='translationmodel',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_subjects', to='lang.Entry'),
        ),
        migrations.AddField(
            model_name='translationmodel',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_objects', to='lang.Entry'),
        ),
        migrations.AddField(
            model_name='translationexamplemodel',
            name='example',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='example_translations', to='lang.Example'),
        ),
        migrations.AddField(
            model_name='translationexamplemodel',
            name='translation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translation_examples', to='lang.Translation'),
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
            model_name='examplemodel',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='example_subjects', to='lang.Entry'),
        ),
        migrations.AddField(
            model_name='examplemodel',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='example_objects', to='lang.Entry'),
        ),
        migrations.AddField(
            model_name='entryrecordingdata',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recordings', to='lang.Entry'),
        ),
        migrations.AlterUniqueTogether(
            name='translationmodel',
            unique_together={('object', 'subject')},
        ),
    ]
