# Generated by Django 4.1.5 on 2023-01-21 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telebot', '0007_curses_delete_curs'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Curses',
            new_name='Exchange_rates',
        ),
    ]