from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Users(models.Model):
    user_id = models.IntegerField(
        verbose_name='user_id',
        help_text='user_id',
        null=True,
        max_length=500
    )
    usd = models.IntegerField(
        verbose_name='USD',
        help_text='usd',
        null=True,
        max_length=10

    )
    aed = models.IntegerField(
        verbose_name='USD',
        help_text='aed',
        null=True,
        max_length=10
    )
    eur = models.IntegerField(
        verbose_name='USD',
        help_text='aed',
        null=True,
        max_length=10
    )


class Curs(models.Model):
    usd = models.IntegerField(
        verbose_name='USD',
        help_text='usd',
        null=68.1,
        max_length=20
    )
    aed = models.FloatField(
        verbose_name='USD',
        help_text='aed',
        null=18.1,
        max_length=20
    )
    eur = models.IntegerField(
        verbose_name='USD',
        help_text='aed',
        null=74.1,
        max_length=20
    )
