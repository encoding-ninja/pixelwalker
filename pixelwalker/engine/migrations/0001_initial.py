# Generated by Django 2.0 on 2017-12-11 21:11

from django.db import migrations, models
import django.db.models.deletion
import engine.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_library_path', models.CharField(max_length=200, null=True)),
                ('max_parallel_tasks', models.IntegerField(default=1)),
                ('worker_pulling_interval', models.IntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='unnamed assessment', max_length=200)),
                ('description', models.CharField(max_length=500, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='EncodingProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='unnamed encoding provider', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='unnamed media', max_length=200)),
                ('file', models.FileField(null=True, upload_to=engine.utils.get_upload_path)),
                ('width', models.IntegerField(null=True)),
                ('height', models.IntegerField(null=True)),
                ('average_bitrate', models.CharField(max_length=50, null=True)),
                ('video_codec', models.CharField(max_length=50, null=True)),
                ('framerate', models.IntegerField(null=True)),
                ('encoding_provider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='engine.EncodingProvider')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(0, 'Queued'), (1, 'Processing'), (2, 'Success'), (3, 'Error'), (4, 'Aborted')], default=0)),
                ('progress', models.IntegerField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_queued', models.DateTimeField(null=True, verbose_name='date queued')),
                ('date_started', models.DateTimeField(null=True, verbose_name='date started')),
                ('date_ended', models.DateTimeField(null=True, verbose_name='date ended')),
                ('assessment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='engine.Assessment')),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.Media')),
            ],
        ),
        migrations.CreateModel(
            name='TaskOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('file_path', models.CharField(max_length=200, null=True)),
                ('average', models.FloatField(null=True)),
                ('type', models.IntegerField(choices=[(0, 'ChartData'), (1, 'ChartLabels'), (2, 'Json'), (3, 'Plain'), (4, 'Media')], default=3)),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='engine.Task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='unnamed task type', max_length=200)),
                ('is_video_metric', models.BooleanField(default=False)),
                ('auto_submit_on_new_media', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engine.TaskType'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='encoded_media_list',
            field=models.ManyToManyField(related_name='encoded_media_list', to='engine.Media'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='reference_media',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='engine.Media'),
        ),
    ]
