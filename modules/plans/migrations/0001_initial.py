# Generated by Django 3.2.4 on 2021-07-09 06:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('A', 'ACTIVE'), ('I', 'INACTIVE')], default='A', max_length=8)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=256)),
                ('price', models.FloatField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
