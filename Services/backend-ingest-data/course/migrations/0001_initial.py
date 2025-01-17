# Generated by Django 4.1.7 on 2023-03-07 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=8)),
                ('name', models.CharField(max_length=128)),
                ('credits', models.FloatField()),
                ('prereqs', models.TextField()),
                ('coreqs', models.TextField()),
                ('note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='InstructionMediums',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Instructors',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('campus', models.CharField(max_length=64)),
                ('building', models.CharField(max_length=64)),
                ('room', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('crn', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=16)),
                ('is_active', models.BooleanField(default=True)),
                ('is_lab', models.BooleanField(default=False)),
                ('enrolled', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('note', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.courses')),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.instructors')),
                ('medium', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.instructionmediums')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.terms')),
            ],
        ),
        migrations.CreateModel(
            name='Schedules',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('is_weekly', models.BooleanField(default=True)),
                ('weekday', models.CharField(max_length=1)),
                ('time_start', models.IntegerField()),
                ('time_end', models.IntegerField()),
                ('date_start', models.IntegerField()),
                ('date_end', models.IntegerField()),
                ('crn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.sections')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.locations')),
            ],
        ),
        migrations.AddField(
            model_name='courses',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.subjects'),
        ),
    ]
