# Generated by Django 4.2.2 on 2023-06-12 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('type', models.CharField(choices=[('focus', 'focus'), ('team', 'team'), ('conference', 'conference')], max_length=11, verbose_name='Type')),
                ('capacity', models.IntegerField(verbose_name='Capacity')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Added Time')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
            ],
        ),
    ]