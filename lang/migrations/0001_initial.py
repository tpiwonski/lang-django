# Generated by Django 2.1.7 on 2019-06-05 21:05

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
            name='ExampleData',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=255)),
                ('translation', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'dictionary_example',
            },
        ),
        migrations.CreateModel(
            name='RelationData',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('kind', models.IntegerField(choices=[(1, 'Translation'), (2, 'Synonym')])),
            ],
            options={
                'db_table': 'dictionary_relation',
            },
        ),
        migrations.CreateModel(
            name='RelationExampleData',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'dictionary_relation_example',
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
            name='Example',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('lang.exampledata',),
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('lang.relationdata',),
        ),
        migrations.CreateModel(
            name='RelationExample',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('lang.relationexampledata',),
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
            model_name='relationexampledata',
            name='example',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='example_relations', to='lang.Example'),
        ),
        migrations.AddField(
            model_name='relationexampledata',
            name='relation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relation_examples', to='lang.Relation'),
        ),
        migrations.AddField(
            model_name='relationdata',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_subjects', to='lang.Entry'),
        ),
        migrations.AddField(
            model_name='relationdata',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_objects', to='lang.Entry'),
        ),
        migrations.AddField(
            model_name='entryrecordingdata',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recordings', to='lang.Entry'),
        ),
        migrations.AlterUniqueTogether(
            name='relationdata',
            unique_together={('object', 'subject', 'kind')},
        ),
    ]
