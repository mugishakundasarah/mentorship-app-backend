# Generated by Django 5.0.6 on 2024-05-16 17:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='mentor',
        ),
        migrations.RemoveField(
            model_name='review',
            name='mentee',
        ),
        migrations.AddField(
            model_name='review',
            name='mentorshipSession',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='mentorship.mentorshipsession'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='occupation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('mentor', 'Mentor'), ('mentee', 'Mentee'), ('admin', 'Admin')], max_length=10)),
                ('bio', models.TextField(blank=True, null=True)),
                ('expertise', models.CharField(blank=True, max_length=255, null=True)),
                ('occupation', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='mentorshipsession',
            name='mentor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship.profile'),
        ),
        migrations.DeleteModel(
            name='Mentor',
        ),
    ]
