# Generated by Django 4.2.17 on 2025-01-03 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filemanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('children', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='filemanager.folder')),
            ],
        ),
    ]
