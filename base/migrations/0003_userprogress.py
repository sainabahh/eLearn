# Generated by Django 5.1.1 on 2024-12-07 06:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_video_description_video_is_locked_alter_video_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_watched', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.logintable')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.video')),
            ],
        ),
    ]
