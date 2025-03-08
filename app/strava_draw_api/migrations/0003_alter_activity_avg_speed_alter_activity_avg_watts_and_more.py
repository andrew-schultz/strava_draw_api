# Generated by Django 5.1.6 on 2025-03-07 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strava_draw_api', '0002_activity_name_activity_start_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='avg_speed',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='avg_watts',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='distance',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='elev_gain',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='polyline',
            field=models.CharField(blank=True, help_text='comes from an activities map.summary_polyline attribute', null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='work_done',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
